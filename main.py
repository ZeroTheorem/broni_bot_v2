import time
from random import choice
import sqlalchemy as sa
from telebot import TeleBot
from init_db import broni
from messages_and_stickers import eror_message, displayed_message, hello_message, stickers_happy, stickers_angry


engine = sa.create_engine('sqlite:///broni.db')
bot = TeleBot("5881448051:AAGnJFe2NRnfochJ91PRw6NW73Fu4ufbXrk")


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id, hello_message)


@bot.message_handler(commands=["guide"])
def get_guide(message):
    msg = ''
    with open("guide.txt", "rt") as f:
        for row in f:
            msg += row
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=["get"])
def get_information_from_bd(message):
    with engine.connect() as conn:
        msg = ''
        select_reqst = sa.select(broni).where(broni.c.value != "N/A")
        result = conn.execute(select_reqst)
        rows = result.fetchall()
        for row in rows:
            msg += displayed_message.format(row[0], row[1], row[2])

        try:
            bot.send_message(message.chat.id, msg)
        except:
            bot.send_message(message.chat.id, "Броней больше нет")
            bot.send_sticker(message.chat.id, choice(stickers_happy))


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
    bot.send_sticker(message.chat.id, choice(stickers_happy))


@bot.message_handler(commands=["write"])
def write_to_file(message):
    msg = ''
    with (engine.connect() as conn, open("broni.txt", "wt") as f):
        select_reqst = sa.select(broni).where(broni.c.value != "N/A")
        result = conn.execute(select_reqst)
        rows = result.fetchall()
        for row in rows:
            msg += displayed_message.format(row[0], row[1], row[2])

        f.write(msg)
    bot.send_message(message.chat.id, "Брони успешно записанны, мастер!")


@bot.message_handler(content_types=["text"])
def send_information_to_bd(message):
    msg = message.text
    actual_time = time.strftime("%H:%M", time.localtime())
    if "/" in msg:
        msg = msg.split(" / ")
        msg = (el.split() for el in msg)
    else:
        msg = (msg.split(), )
    with engine.connect() as conn:
        for el in msg:
            update_reqst = sa.update(broni).where(
                broni.c.id == el[0]).values(value=el[1], actual_time=actual_time)
            conn.execute(update_reqst)
            conn.commit()
    bot.send_sticker(message.chat.id, choice(stickers_angry))


if __name__ == "__main__":
    bot.polling(non_stop=True)
