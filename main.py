from telebot import TeleBot
import sqlalchemy as sa
from init_db import broni
import time
from test import hello_string

engine = sa.create_engine('sqlite:///broni.db')
bot = TeleBot("5881448051:AAGnJFe2NRnfochJ91PRw6NW73Fu4ufbXrk")


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, hello_string)


@bot.message_handler(commands=["get"])
def get(message):
    with engine.connect() as conn:
        msg = ''
        result = conn.execute(sa.select(broni).where(broni.c.value != "N/A"))
        for x in result.fetchall():
            msg += f'{x[0]} - {x[1]} ___ {x[2]}\n'
        bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=["del"])
def delete_record(message):
    msg = bot.send_message(message.chat.id, "Введи номер компьютера")
    bot.register_next_step_handler(msg, next_step_del)


def next_step_del(message):
    with engine.connect() as conn:
        msg = message.text.split()
        for x in msg:
            conn.execute(sa.update(broni).where(
                broni.c.id == x).values(value="N/A"))
            conn.commit()


@bot.message_handler(commands=["write_to_file"])
def write_to_file(message):
    msg = ''
    with (engine.connect() as conn, open("broni.txt", "wt") as f):
        result = conn.execute(sa.select(broni).where(broni.c.value != "N/A"))
        for x in result.fetchall():
            msg += f'{x[0]} - {x[1]} ___ {x[2]}\n'
        f.write(msg)


@bot.message_handler(content_types=["text"])
def create_bron(message):
    msg = message.text.split()
    if len(msg) > 2:
        bot.send_message(message.chat.id, "you are idiot")
    elif int(msg[0]) < 0 or int(msg[0]) > 28:
        bot.send_message(message.chat.id, "you are idiot 29")
    else:
        now_time = time.strftime("%H:%M", time.localtime())
        with engine.connect() as conn:
            conn.execute(sa.update(broni).where(
                broni.c.id == msg[0]).values(value=msg[1], actual_time=now_time))
            conn.commit()
            bot.send_message(message.chat.id, "Все прошло успешно")


if __name__ == "__main__":
    bot.polling()
