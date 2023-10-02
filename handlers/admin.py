import asyncio
import random
import time

from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

import TEXTS
import config
from config import bot
from database import sqlite_db
from keyboards import admin_kb


class SendUserMessage(StatesGroup):
    GetUserID = State()
    GetMessageForUser = State()


def is_admin(message):
    return message.chat.id in config.ADMINS


async def start_cmd(message: types.Message):
    sqlite_db.cur.execute(
        f"SELECT chatid FROM users WHERE chatid = '{message.chat.id}'")
    if sqlite_db.cur.fetchone() is None:
        await sqlite_db.sql_add_user_cmd(message)
        await bot.send_message(message.chat.id, "Hello! \nList of commands /help.")
        for ids in config.ADMINS:

            await bot.send_message(ids,
                                   f"Новый пользователь:\n"
                                   f"Логин: @{message.from_user.username} \n"
                                   f"Имя: {message.from_user.first_name} \n"
                                   f"Фамилия: {message.from_user.last_name} \n"
                                   f"id: `{message.chat.id}`", parse_mode="MarkdownV2"
                                   )
            ids += 1
    else:
        await bot.send_message(message.chat.id, "Hello! \nList of commands /help.")


async def help_cmd(message: types.Message):
    await bot.send_message(message.chat.id, 'Use keyboard buttons or type:\n'
                                            '\n'
                                            'howto\n'
                                            'download\n'
                                            'certificate\n'
                                            'password',
                           reply_markup=admin_kb.keyboard)

    await bot.send_video(message.chat.id, open("./file_0.mp4", "rb"), caption='See tutorial')
    await bot.send_message(message.chat.id, TEXTS.HELPMESSAGE.get('1'))
    # await send_message_and_delete(bot, message.chat.id, TEXTS.HELPMESSAGE.get('1'))


async def send_menu_text(message: types.Message):
    if message.text.lower() == 'password':
        x = str(time.time() + random.random())
        password = 'https://www.vpnbook.com/password.php?t=' + x
        await bot.send_photo(message.chat.id, password, caption='login: vpnbook', disable_notification=True)
    elif message.text.lower() == 'certificate':
        await bot.send_message(message.chat.id, text="Which one?", reply_markup=admin_kb.markup_cert)
    elif message.text.lower() == 'howto':
        await bot.send_message(message.chat.id, text='Choose your OS', reply_markup=admin_kb.markup_howto)
    elif message.text.lower() == 'download':
        await bot.send_message(message.chat.id, '[Download](https://openvpn.net/community-downloads/)',
                               parse_mode='Markdown')
    elif message.text.lower() == 'users':
        await sqlite_db.show_users(message)
    else:
        await bot.send_message(message.chat.id, 'I recorded the message')
        await sqlite_db.save_message_to_db(message)
        for ids in config.ADMINS:
            await bot.send_message(ids,
                                   f"Сообщение от пользователя: \n"
                                   f"{message.text} \n"
                                   f"Логин: @{message.from_user.username} \n"
                                   f"Имя: {message.from_user.first_name} \n"
                                   f"Фамилия: {message.from_user.last_name} \n"
                                   f"id = {str(message.from_user.id)} \n"
                                   )


async def query_handler(call: types.CallbackQuery):
    await bot.answer_callback_query(callback_query_id=call.id, text='Great choise!')
    answer = 'NONE'
    if call.data in TEXTS.CALLS.keys():
        answer = TEXTS.CALLS.get(call.data)

    await bot.send_message(call.message.chat.id, answer, parse_mode="Markdown")
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)


async def send_message_to_user(message: types.Message):
    if is_admin(message):
        await message.answer("Введите ID пользователя:", reply_markup=admin_kb.cancel_menu_kb)
        await SendUserMessage.GetUserID.set()


# ---- STATE CANCEL START ------------ #
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    if is_admin(message):
        await message.reply('ok', reply_markup=admin_kb.keyboard)
    else:
        await message.reply('ok', reply_markup=admin_kb.keyboard)
# ---- STATE CANCEL END ------------ #


async def process_get_user_ID_step(message: types.Message, state: FSMContext):
    user_id = message.text
    await message.answer("Введите сообщение:")
    await state.update_data(user_id=user_id)
    await SendUserMessage.GetMessageForUser.set()


async def process_get_message_for_user_step(message: types.Message, state: FSMContext):
    message_for_user = message.text
    data = await state.get_data()
    user_id = data.get('user_id')
    await bot.send_message(user_id, message_for_user)
    await message.answer('Отправлено!')
    await state.finish()


async def send_message_and_delete(bot, chat_id, message):
    sent_message = await bot.send_message(chat_id, message)
    await asyncio.sleep(30)
    await sent_message.delete()
