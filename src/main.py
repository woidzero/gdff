import os

import telebot
from telebot import types
from telebot.async_telebot import AsyncTeleBot

from db import Database
from config import Config
from utils import create_form

from PIL import Image


bot = AsyncTeleBot(Config.TOKEN)

user_ids = {}


@bot.message_handler(commands=["help", "start"])
def welcome(message) -> None:
    user_ids.update({message.chat.id: 0})

    view_forms_btn = types.KeyboardButton("👥 Посмотреть анкеты")
    create_form = types.KeyboardButton("📝 Моя анкета")
    info_btn = types.KeyboardButton("📍 Информация")

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(create_form, view_forms_btn, info_btn)

    bot.reply_to(
        message, "Добро пожаловать! Пора создать анкету.", reply_markup=keyboard
    )


@bot.message_handler(content_types=["text"])
def handle_message(message) -> None:
    if message.text == "Создать анкету":
        talking = types.KeyboardButton("Общение")
        creator = types.KeyboardButton("Креатор")
        slayer = types.KeyboardButton("Слеер")
        host = types.KeyboardButton("Хост")

        start_btn = types.KeyboardButton("Вернутся")

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(talking, creator, slayer, host, start_btn)

        bot.reply_to(message, "Кто вы?", reply_markup=keyboard)
    elif message.text == "Общение":
        create_form(message, 1, "Расскажи о себе.")
    elif message.text == "Креатор":
        create_form(message, 2, "Расскажи о себе.")
    elif message.text == "Слеер":
        create_form(message, 3, "Расскажи о себе, о достижениях и хардесте.")
    elif message.text == "Хост":
        create_form(message, 4, "Что за коллаб?")
    elif message.text == "Просмотреть анкеты":
        view_form(message)
    elif message.text == "Удалить анкету":
        remove_form(message)
    elif message.text == "🔙 К началу":
        welcome(message)
    elif message.text == "🔴 Скип":
        user_ids[message.chat.id] += 2
        try:
            view_form(message)
        except IndexError:
            user_ids[message.chat.id] -= 2
            view_form(message)
    elif message.text == "Предыдущий":
        if user_ids[message.chat.id] > 0:
            user_ids[message.chat.id] -= 2

        view_form(message)


def process_description_step(message):
    path = find_user_path(message.from_user.username)[0]
    with open(path, "a", encoding="utf-8") as user_file:
        if len(message.text) < 1000:
            user_file.write(message.text)
        else:
            bot.reply_to(message, "Слишком длинное сообщение!")
            return

        blocked_names = [
            "К началу",
            "Креатор",
            "Общение",
            "Хост",
        ]

        if message.text not in blocked_names:
            bot.reply_to(
                message, "Анкета успешно создана! Вот как ее будут видеть остальные:"
            )
        else:
            user_file.close()
            os.remove(path)
            welcome(message)

            return

        form = f"""
@{message.from_user.username}

{message.text}
		"""

        try:
            photos = bot.get_user_profile_photos(message.from_user.id)
            bot.send_photo(message.chat.id, photos.photos[0][2].file_id)

            with open(path + ".png", "wb") as avatar:
                file_info = bot.get_file(photos.photos[0][2].file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                avatar.write(downloaded_file)
        except:
            pass

        view_forms_btn = types.KeyboardButton(text="Просмотреть анкеты")

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(view_forms_btn)

        bot.send_message(message.chat.id, form, reply_markup=keyboard)


def send_form(message, folder):
    next_btn = types.KeyboardButton(text="Следующий")
    previous_btn = types.KeyboardButton(text="Предыдущий")
    start_btn = types.KeyboardButton(text="К началу")

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(next_btn, previous_btn, start_btn)

    user = os.listdir("users/" + folder + "/")[user_ids[message.chat.id]]
    user = "users/" + folder + "/" + user
    user = user.replace(".png", "")

    with open(user, "r", encoding="utf-8") as user_file:
        data = user_file.read().split(":")
        form = f"""
@{data[0]}

{data[1]}
		"""

    try:
        avatar = Image.open(user + ".png")
        avatar = avatar.resize((128, 128))
        bot.send_photo(message.chat.id, avatar)
    except:
        pass

    bot.send_message(message.chat.id, form, reply_markup=keyboard)
    return


def remove_form(message):
    try:
        path = find_user_path(message.from_user.username)
        os.remove(path[0])

        bot.reply_to(message, "Вы успешно удалили вашу анкету!")
    except:
        bot.reply_to(message, "У вас не создана анкета!")
        return


def view_form(message):
    try:
        path = find_user_path(message.from_user.username)[0]
    except:
        bot.reply_to(message, "У вас не создана анкета!")
        return

    if "hostsgp" in path:
        send_form(message, "gp")
    if "hostsdeco" in path:
        send_form(message, "deco")
    if "gp" in path:
        send_form(message, "hostsgp")
    if "deco" in path:
        send_form(message, "hostsdeco")
    if "talking" in path:
        send_form(message, "talking")


def find_user_path(name):
    users = []
    for user_folder in os.listdir("users"):
        for user in os.listdir("users/" + user_folder):
            if ".png" in user:
                continue

            with open(
                f"users/{user_folder}/{user}", "r", encoding="utf-8"
            ) as user_file:
                data = user_file.read().split(":")
                if data[0] == name:
                    users.append(f"users/{user_folder}/{user}")

    return users


if __name__ == "__main__":
    bot.infinity_polling()
