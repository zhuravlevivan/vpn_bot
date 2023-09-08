from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import BotCommand
from TEXTS import COMMANDS
from config import Bot


markup_cert = InlineKeyboardMarkup()
btn1 = InlineKeyboardButton(text='PL', callback_data='1')
btn2 = InlineKeyboardButton(text='DE', callback_data='2')
btn3 = InlineKeyboardButton(text='US1', callback_data='3')
btn4 = InlineKeyboardButton(text='CA222', callback_data='4')
btn5 = InlineKeyboardButton(text='CA198', callback_data='5')
btn6 = InlineKeyboardButton(text='FR1', callback_data='6')
btn7 = InlineKeyboardButton(text='FR8', callback_data='7')

markup_cert.row(btn4, btn5)
markup_cert.row(btn1, btn2, btn3)
markup_cert.row(btn6, btn7)


markup_howto = InlineKeyboardMarkup()
btn1 = InlineKeyboardButton(text='Windows 10/11', callback_data='11')
btn2 = InlineKeyboardButton(text='Windows 7', callback_data='12')
btn3 = InlineKeyboardButton(text='Mac OS X', callback_data='13')
btn4 = InlineKeyboardButton(text='Ubuntu', callback_data='14')
btn5 = InlineKeyboardButton(text='iOS/iPad', callback_data='15')
btn6 = InlineKeyboardButton(text='Android', callback_data='16')
btn7 = InlineKeyboardButton(text='Windows XP', callback_data='17')

markup_howto.row(btn1, btn2)
markup_howto.row(btn3, btn4)
markup_howto.row(btn5, btn6)
markup_howto.row(btn7)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard.row('howto', 'download', 'certificate', 'password')


# ------------ CANCEL KB START ------------ #
cancel_menu_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
cm_kb1 = KeyboardButton('cancel')
cancel_menu_kb.row(cm_kb1)
# ------------ CANCEL KB END ------------ #

adm_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
key_1 = KeyboardButton('users')
key_2 = KeyboardButton('sendm')




async def set_main_menu(bot: Bot):
    main_menu_commands = [BotCommand(
        command=command,
        description=description
    ) for command,
        description in COMMANDS.items()]
    await bot.set_my_commands(main_menu_commands)


