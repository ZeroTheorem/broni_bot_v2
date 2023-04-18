from telebot import TeleBot
import sqlalchemy as sa
from init_db import broni
import time
from messages_and_sticers import eror_message


engine = sa.create_engine('sqlite:///broni.db')
bot = TeleBot("5881448051:AAGnJFe2NRnfochJ91PRw6NW73Fu4ufbXrk")


@bot.message_handler(commands=["start"])
def start(message):
    msg = ''
    with open("hello_message.txt", "rt") as f:
        for x in f:
            msg += x
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=["guide"])
def start(message):
    msg = ''
    with open("hello_message.txt", "rt") as f:
        for x in f:
            msg += x
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=["get"])
def get_information_from_bd(message):
    with engine.connect() as conn:
        msg = ''
        select_reqst = sa.select(broni).where(broni.c.value != "N/A")
        result = conn.execute(select_reqst)
        rows = result.fetchall()
        for row in rows:
            msg += f'{row[0]} - {row[1]} ___ {row[2]}\n'

        try:
            bot.send_message(message.chat.id, msg)
        except:
            bot.send_message(message.chat.id, "Броней больше нет")


@bot.message_handler(commands=["del"])
def initiate_return_to_default_value(message):
    msg = bot.send_message(message.chat.id, "Введи номер компьютера")
    bot.register_next_step_handler(msg, return_to_default_value)


def return_to_default_value(message):
    msg = message.text.split()
    with engine.connect() as conn:
        for el in msg:
            update_reqst = sa.update(broni).where(
                broni.c.id == el).values(value="N/A")
            conn.execute(update_reqst)
            conn.commit()


@bot.message_handler(commands=["write"])
def write_to_file(message):
    msg = ''
    with (engine.connect() as conn, open("broni.txt", "wt") as f):
        select_reqst = sa.select(broni).where(broni.c.value != "N/A")
        result = conn.execute(select_reqst)
        rows = result.fetchall()
        for row in rows:
            msg += f'{row[0]} - {row[1]} ___ {row[2]}\n'

        f.write(msg)


@bot.message_handler(content_types=["text"])
def send_information_to_bd(message):
    msg = message.text.split()
    if len(msg) > 2:
        bot.send_message(message.chat.id, eror_message.format(message.text))
    else:
        actual_time = time.strftime("%H:%M", time.localtime())
        with engine.connect() as conn:
            update_reqst = sa.update(broni).where(
                broni.c.id == msg[0]).values(value=msg[1], actual_time=actual_time)
            conn.execute(update_reqst)
            conn.commit()
            bot.send_message(message.chat.id, "Все прошло успешно")
            # bot.send_stickers()


if __name__ == "__main__":
    bot.polling()
