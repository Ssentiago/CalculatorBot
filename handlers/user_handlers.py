from aiogram.filters import Command, CommandStart
from aiogram import F, Router
import logging
from inline_keyboard.keyboard import keyboard as inl_keyboard
from aiogram.types import Message, CallbackQuery
from service.service import calculate

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command(commands=['start']))
async def start_command(message: Message):
    await message.answer(text='0', reply_markup=inl_keyboard)


@router.callback_query(F.data == 'С')
async def process_C(callback: CallbackQuery):
    await callback.message.edit_text(
        text='0',
        reply_markup=inl_keyboard
    )


@router.callback_query(F.data.in_('%÷+^×-.'))
async def add_sym(callback: CallbackQuery):
    if callback.message.text != '0':
        await callback.message.edit_text(
            text=callback.message.text + callback.data,
            reply_markup=inl_keyboard)
    else:
        await  callback.answer('Неправильная операция!')


@router.callback_query(F.data.in_('0123456789'))
async def add_other_sym(callback: CallbackQuery):
    await callback.message.edit_text(
        text=(callback.message.text != '0' and callback.message.text or '') + callback.data,
        reply_markup=inl_keyboard
    )


@router.callback_query(F.data.in_('()'))
async def brack(callback: CallbackQuery):
    cb = callback.message.text
    if cb == '0' and callback.data == '(':
        await callback.message.edit_text(
            text=callback.data,
            reply_markup=inl_keyboard
        )
    elif cb != '0' and callback.data in '()':
        await  callback.message.edit_text(
            text=cb + callback.data,
            reply_markup=inl_keyboard
        )
    else:
        await callback.answer('Неправильная операция!')


@router.callback_query(F.data == '⌫')
async def del_sym(callback: CallbackQuery):
    if len(callback.message.text) == 1:
        await  callback.message.edit_text(text='0', reply_markup=inl_keyboard)
    else:
        if '!' in callback.message.text:
            await callback.message.edit_text(
                text='0',
                reply_markup=inl_keyboard
            )
        else:
            await callback.message.edit_text(text=callback.message.text[:-1], reply_markup=inl_keyboard)


@router.callback_query(F.data == '=')
async def caclculate(callback: CallbackQuery):
    try:
        await  callback.message.edit_text(
            text=callback.message.text + '=' + calculate(callback.message.text),
            reply_markup=inl_keyboard
        )
    except Exception as e:
        await  callback.answer(text='Неправильная операция!')


@router.callback_query(F.data == '√')
async def root(callback: CallbackQuery):
    await callback.message.edit_text(text=(callback.message.text != '0' and callback.message.text or '') + callback.data,
                                     reply_markup=inl_keyboard)
    await callback.answer(
        'Убедитесь, что следующим символом вы введёте значение корня, а затем в квадратных скобках подкоренное выражение')


@router.callback_query(F.data == '!')
async def fact(callback: CallbackQuery):
    await callback.answer('Убедитесь, что вы ввели факториальное выражение в скобках прямиком перед знаком факториала')
    await callback.message.edit_text(
        text=(callback.message.text != '0' and callback.message.text or '') + callback.data,
        reply_markup=inl_keyboard
    )
