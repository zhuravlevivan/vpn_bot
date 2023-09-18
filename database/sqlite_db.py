import sqlite3 as sq

from config import bot
from handlers.admin import is_admin

base = None
cur = None


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
