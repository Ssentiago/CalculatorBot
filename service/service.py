import regex
from functools import partial
from decimal import Decimal

operations = {
    '+': lambda operand1, operand2: operand1 + operand2,
    '-': lambda operand1, operand2: operand1 - operand2,
    '×': lambda operand1, operand2: operand1 * operand2,
    '÷': lambda operand1, operand2: operand1 / operand2 if operand2 != 0 else 'На ноль делить нельзя!',
    '^': lambda operand1, operand2: operand1 ** operand2,
    '√': lambda operand1, operand2: operand1 ** (1 / operand2),
    '%': lambda operand1, operand2: operand1 * (operand2 / 100),
    '!': lambda operand: factorial(operand)
}
operator_priority = ('+', '-', '×', '÷', '%', '^', '√', '!')
check_brackets = regex.compile(r'\(((?>[^()])*)\)')
check_brackets_recursive = regex.compile(r"[0-9+×/%^√2√n!-]*\((?>[^()]|(?R))*\)[0-9+×/%^√√n!-]*")

pattern_fact = partial(regex.sub, r'(?P<ev>\(.*?\))(?P<sign>!)',
                       lambda x: str(operations[x['sign']](Decimal(_rec_evaluate(x['ev'].strip('()'))))))
pattern_root = partial(regex.sub, r'(?P<sign>√)(?P<deg>\d)(?P<ev>\(.+?\))',
                       lambda x: str(operations[x['sign']](Decimal(_rec_evaluate(str(x['ev'].strip('()')))), Decimal(x['deg']))))


def factorial(n):
    if n in (0, 1):
        return n
    return n * factorial(n - 1)


def _rec_evaluate(parsed_line: str):
    if '!' in parsed_line:
        parsed_line = pattern_fact(parsed_line)
    if '√' in parsed_line:
        parsed_line = pattern_root(parsed_line)

    while '(' in parsed_line and ')' in parsed_line:
        parsed_line = check_brackets.sub(lambda x: _rec_evaluate(x[1]), parsed_line)

    if parsed_line.isdigit():
        return Decimal(parsed_line)
    if '.' in parsed_line:
        check = parsed_line.split('.', 1)
        if check[0].isdigit() and check[1].isdigit():
            return Decimal(parsed_line)

    for op in operator_priority:
        if op in str(parsed_line):
            if parsed_line.split('-')[0] != '':
                parsed_line = str(parsed_line).split(op, 1)
                left = _rec_evaluate(parsed_line[0])
                operator = op
                right = _rec_evaluate(parsed_line[1])

                if right == 'На ноль делить нельзя!' or left == 'На ноль делить нельзя!':
                    raise ValueError('На ноль делить нельзя!')

                parsed_line = str(operations[operator](Decimal(left), Decimal(right)))

    return (parsed_line)


def calculate(math_evaluation):
    if not '(' in math_evaluation and not ')' in math_evaluation:
        return normalize_result(_rec_evaluate(math_evaluation))
    else:
        if check_brackets_recursive.fullmatch(math_evaluation):
            return normalize_result(_rec_evaluate(math_evaluation))
        else:
            raise ValueError('Что-то пошло не так.. Проверьте скобки')


def normalize_result(n: Decimal):
    return all(x == '0' for x in str(n).split('.')[-1]) and str(int(Decimal(n))) or str(n)

