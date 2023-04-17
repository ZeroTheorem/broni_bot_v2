from telebot import TeleBot
import sqlalchemy as sa
from init_db import Broni


engine = sa.create_engine('sqlite:///Broni.db')
bot = TeleBot("5881448051:AAGnJFe2NRnfochJ91PRw6NW73Fu4ufbXrk")


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Hello")


@bot.message_handler(commands=["get"])
def get(message):
    with engine.connect() as conn:
        result = conn.execute(sa.select(Broni).where(Broni.c.value != "N/A"))
        bot.send_message(message.chat.id, f'{result.fetchall()}')


@bot.message_handler(commands=["del"])
def delete(message):
    msg = bot.send_message(message.chat.id, "Введи номер компьютера")
    bot.register_next_step_handler(msg, next_step_del)


def next_step_del(message):
    with engine.connect() as conn:
        msg = message.text.split()
        for x in msg:
            conn.execute(sa.update(Broni).where(
                Broni.c.id == x).values(value="N/A"))
            conn.commit()


@bot.message_handler(content_types=["text"])
def create_bron(message):
    msg = message.text.split()
    with engine.connect() as conn:
        conn.execute(sa.update(Broni).where(
            Broni.c.id == msg[0]).values(value=msg[1]))
        conn.commit()
        result = conn.execute(sa.select(Broni).where(Broni.c.id == msg[0]))
        bot.send_message(message.chat.id, f'{result.fetchone()}')


if __name__ == "__main__":
    bot.polling()
