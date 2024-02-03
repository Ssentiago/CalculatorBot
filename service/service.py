import regex

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
check_brackets = regex.compile(r'\((?>[^()])*\)')
check_brackets_recursive = regex.compile(r"[0-9+×/%^√2√n!-]*\((?>[^()]|(?R))*\)[0-9+×/%^√√n!-]*")
check_last = regex.compile(r'.*?(?:\d|\)|!|\()$')

find_root = regex.compile(r'√\d')
find_fact = regex.compile(r'!')
find_fact_content = regex.compile(r'\(\d+\)(?=\!)')


def __rec_parse_line(parsed_line: str | None = None):
    while (check := find_fact.search(parsed_line)):
        fact_content = find_fact_content.search(parsed_line)
        left = parsed_line[:fact_content.start()]
        right = parsed_line[check.end():]

        value = __rec_parse_line(fact_content[0])
        if type(value) == float:
            value = str(operations['!'](int(value)))
        parsed_line = left + value + right

    while (check := find_root.search(parsed_line)):
        left = parsed_line[:check.start()]
        value = check_brackets.search(parsed_line, pos=check.start())
        right = parsed_line[value.end():]

        value = str(calculate(value[0]))
        op, root = check[0][0], check[0][1]
        parsed_line = left + str(operations[op](float(value), float(root))) + right

    while '(' in parsed_line and ')' in parsed_line:
        find = regex.search(check_brackets, parsed_line)
        left = parsed_line[:find.start()]
        mid = str(__rec_calculate(__rec_parse_line(find.group().strip('()'))))
        right = parsed_line[find.end():]

        parsed_line = left + mid + right
    if not parsed_line.isdigit():
        for op in operator_priority:
            if op in parsed_line:
                line = parsed_line.split(op, 1)
                return [__rec_parse_line(line[0])] + [op] + [__rec_parse_line(line[1])]

    return parsed_line != '' and float(parsed_line) or ''


def __rec_calculate(parsed_line):
    if isinstance(parsed_line, (str, float)):
        return parsed_line

    operator = parsed_line[1]
    left = __rec_calculate(parsed_line[0])
    right = __rec_calculate(parsed_line[2])

    if right == 'На ноль делить нельзя!' or left == 'На ноль делить нельзя!':
        raise ValueError('На ноль делить нельзя!')
    x = filter(None, [left, right])
    return operations[operator](*x)


def calculate(math_evaluation):
    if not '(' in math_evaluation and not ')' in math_evaluation:
        return str(__rec_calculate(__rec_parse_line(math_evaluation)))
    else:
        if check_brackets_recursive.fullmatch(math_evaluation):
            return str(__rec_calculate(__rec_parse_line(math_evaluation)))
        else:
            raise ValueError('Что-то пошло не так.. Проверьте скобки')


def factorial(n):
    if n in (0, 1):
        return n
    return n * factorial(n - 1)
