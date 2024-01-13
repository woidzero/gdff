import telebot
from db import Database
from telebot import types

db = Database()


def get_photo_bitmap(bot: telebot.TeleBot, user_id: int) -> None:
    photos = bot.get_user_profile_photos(user_id)
    return photos.photos[0][2].file_id


async def create_form(bot: telebot.TeleBot, message: types.Message, category: int, details: str) -> int:
    uid = message.from_user.id
    name = message.from_user.full_name
    profile_picture = get_photo_bitmap(bot, message)

    if await db.fetch_user(uid):
        return -1
    await db.new_user(uid, name, category, details, profile_picture)
    return 1

    # мне лень дописывать
    #
    # description = bot.reply_to(message, text)
    # bot.register_next_step_handler(description, process_description_step)
