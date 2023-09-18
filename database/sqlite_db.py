import sqlite3 as sq
import gspread

from datetime import datetime

from config import bot, google_json, tab_name
from handlers.admin import is_admin

base = None
cur = None

gc = gspread.service_account(filename=google_json)
sh = gc.open(tab_name)
worksheet = sh.get_worksheet(0)
worksheet2 = sh.get_worksheet(1)


def sql_start():
    global base, cur
    base = sq.connect('vpn_users.db', check_same_thread=False)
    cur = base.cursor()
    if base:
        print('Database Connect OK!')
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                   chatid varchar(255),
                   login varchar(255),
                   name varchar(255),
                   lname varchar(255)
                )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS messages(
                       chatid varchar(255),
                       login varchar(255),
                       message varchar(255)
                )""")
    base.commit()


def backupdb():
    b_conn = sq.connect("backup.db")
    sq.connect('vpn_users.db').backup(b_conn)
    b_conn.close()


async def sql_add_user_cmd(message):
    global base, cur
    base = sq.connect('vpn_users.db', check_same_thread=False)
    cur = base.cursor()
    cur.execute(f"INSERT INTO users VALUES(?,?,?,?)", (message.chat.id,
                                                       message.from_user.username,
                                                       message.from_user.first_name,
                                                       message.from_user.last_name
                                                       ))
    base.commit()
    await add_users_to_sheets(message.chat.id,
                              message.from_user.username,
                              message.from_user.first_name,
                              message.from_user.last_name)


async def show_users(message):
    global base, cur
    base = sq.connect('vpn_users.db', check_same_thread=False)
    cur = base.cursor()
    if is_admin(message):
        for value in cur.execute("SELECT * FROM users").fetchall():
            await bot.send_message(message.chat.id,
                                   f"<code>{value[0]}</code> @{value[1]} {value[2]} {value[3]}", parse_mode="html")


async def save_message_to_db(message):
    global base, cur
    base = sq.connect('vpn_users.db', check_same_thread=False)
    cur = base.cursor()
    cur.execute(f"INSERT INTO messages VALUES(?,?,?)", (message.chat.id,
                                                        f"@{message.from_user.username}",
                                                        message.text
                                                        ))
    base.commit()
    await add_message_from_user_to_sheets(message.chat.id, message.from_user.username, message.text)


async def add_users_to_sheets(user_id, u_name, f_name, l_name):
    date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    raw_data = [user_id, f'@{u_name}', f_name, l_name, date]
    clean_data = []
    for item in raw_data:
        if item is None:
            item = '___'
        clean_data.append(item)
    worksheet.append_row(clean_data)


async def add_message_from_user_to_sheets(user_id, u_name, message):
    date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    raw_data = [user_id, f'@{u_name}', message, date]
    clean_data = []
    for item in raw_data:
        if item is None:
            item = '___'
        clean_data.append(item)
    worksheet2.append_row(clean_data)
