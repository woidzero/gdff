from typing import Final

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.database.methods import get_random_user_id, get_user
from bot.keyboards import KbButtons

router: Final[Router] = Router(name=__name__)


@router.message(F.text == KbButtons.main["my_servey"])
@router.message(Command("my_profile"))
async def cmd_my_profile(message: Message) -> None:
    await show_survey(message=message, user_id=message.from_user.id, mention_user=True)


async def show_survey(message: Message, user_id: int, mention_user: bool = True) -> None:
    user = await get_user(user_id)
    name = user.mention if mention_user else user.name
    category_type = KbButtons.category_to_id.get_key(user.category)
    category = KbButtons.category_select.get_value(category_type)
    await message.answer(f"👤 {name}\n📝 {category}\n\n{user.description}")


@router.message(F.text == KbButtons.main["check_surveys"])
@router.message(Command("random_profile"))
async def cmd_show_survey(message: Message) -> None:
    user_id = await get_random_user_id(exclude_user_id=message.from_user.id)
    await show_survey(message=message, user_id=user_id)
