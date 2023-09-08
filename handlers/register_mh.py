from aiogram.dispatcher.filters import Text

from config import Dispatcher
from database import sqlite_db
from handlers.admin import (start_cmd, help_cmd, send_menu_text, query_handler,
                            send_message_to_user, process_get_user_ID_step, process_get_message_for_user_step,
                            cancel_handler, SendUserMessage)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(start_cmd, commands=['start'])
    dp.register_message_handler(help_cmd, commands=['help'])

    dp.register_callback_query_handler(query_handler, lambda x: x.data)
    dp.register_message_handler(sqlite_db.show_users, Text(equals='users', ignore_case=True))

    dp.register_message_handler(send_message_to_user, Text(equals='sendm', ignore_case=True), state=None)
    dp.register_message_handler(cancel_handler, Text(equals='cancel', ignore_case=True), state='*')
    dp.register_message_handler(process_get_user_ID_step, state=SendUserMessage.GetUserID)
    dp.register_message_handler(process_get_message_for_user_step, state=SendUserMessage.GetMessageForUser)
    dp.register_message_handler(send_menu_text, content_types=['text'])
