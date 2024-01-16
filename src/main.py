import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from config import Config
from keyboards import common_keyboard
from PIL import Image
from utils import create_form

from src import fsm, handlers
from src.database.base import register_models
from src.fsm import category_keyboard_buttons

dp = Dispatcher(storage=MemoryStorage())

dp.include_router(fsm.router)
dp.include_router(handlers.router)

user_ids = {}

main_keyboard_buttons = [
    "👥 Посмотреть анкеты",
    "📝 Моя анкета",
    "📍 Информация",
]


# @dp.message_handler(content_types=["text"])
# @dp.message(lambda message: message.text in main_keyboard_buttons + list(category_keyboard_buttons.values()))
def handle_message(message: Message) -> None:
    text = message.text
    if text == main_keyboard_buttons[2]:
        category_keyboard = common_keyboard(*category_keyboard_buttons)
        message.answer("Кем вы являтесь и кого хотите найти?", reply_markup=category_keyboard)
    elif text in category_keyboard_buttons:
        message.answer("Расскажи о себе.")
        create_form(
            message,
            1,
        )
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
    # elif message.text == "🔙 К началу":
    #     welcome(message)
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
            message.reply("Слишком длинное сообщение!")
            return

        blocked_names = [
            "К началу",
            "Креатор",
            "Общение",
            "Хост",
        ]

        if message.text not in blocked_names:
            message.reply("Анкета успешно создана! Вот как ее будут видеть остальные:")
        else:
            user_file.close()
            os.remove(path)
            # welcome(message)

            return

        form = f"""
@{message.from_user.username}

{message.text}
		"""

        # try:
        # photos = bot.get_user_profile_photos(message.from_user.id)
        # bot.send_photo(message.chat.id, photos.photos[0][2].file_id)

        #     with open(path + ".png", "wb") as avatar:
        #         file_info = bot.get_file(photos.photos[0][2].file_id)
        #         downloaded_file = bot.download_file(file_info.file_path)
        #         avatar.write(downloaded_file)
        # except:
        #     pass

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
        f"""
@{data[0]}

{data[1]}
		"""

    try:
        avatar = Image.open(user + ".png")
        avatar = avatar.resize((128, 128))
        # bot.send_photo(message.chat.id, avatar)
    except:
        pass

    # bot.send_message(message.chat.id, form, reply_markup=keyboard)
    return


def remove_form(message):
    try:
        path = find_user_path(message.from_user.username)
        os.remove(path[0])

        message.reply("Вы успешно удалили вашу анкету!")
    except:
        message.reply("У вас не создана анкета!")
        return


def view_form(message):
    try:
        path = find_user_path(message.from_user.username)[0]
    except:
        message.reply("У вас не создана анкета!")
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

            with open(f"users/{user_folder}/{user}", "r", encoding="utf-8") as user_file:
                data = user_file.read().split(":")
                if data[0] == name:
                    users.append(f"users/{user_folder}/{user}")

    return users


async def on_startup() -> None:
    await register_models()


async def main() -> None:
    bot = Bot(Config.TOKEN, parse_mode=ParseMode.HTML)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
