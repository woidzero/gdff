from typing import Final

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from bot.database.methods import delete_user_profile, get_random_user_id, get_user
from bot.handlers.other import cmd_start

from bot.keyboards.main import CategorySelectButtons, ConfirmationButtons, MainMenuButtons
from bot.states.registration import Unregistration

router: Final[Router] = Router(name=__name__)


@router.message(F.text == MainMenuButtons.MY_SURVEY.value)
@router.message(Command("my_profile"))
async def cmd_my_profile(message: Message) -> None:
    await show_survey(message=message, user_id=message.from_user.id, mention_user=True)


async def show_survey(message: Message, user_id: int, mention_user: bool = True) -> None:
    user = await get_user(user_id)
    if user.is_registered is False:
        return

    name = user.mention if mention_user else user.name
    category = CategorySelectButtons.get_name_by_id(user.category)
    await message.answer(
        f"👤 {name}, 💠️ {category} — {user.description}", reply_markup=MainMenuButtons.markup()
    )


@router.message(F.text == MainMenuButtons.CHECK_SURVEYS.value)
@router.message(Command("random_profile"))
async def cmd_show_survey(message: Message) -> None:
    user_id = await get_random_user_id(exclude_user_id=message.from_user.id)
    if user_id:
        await show_survey(message=message, user_id=user_id)
    else:
        await message.answer("Другие анкеты не найдены!", reply_markup=MainMenuButtons.markup())


@router.message(default_state, Command("unregister"))
async def cmd_unregister(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Вы точно хотите удалить свою анкету?", reply_markup=ConfirmationButtons.markup()
    )
    await state.set_state(Unregistration.confirmation)


@router.message(Unregistration.confirmation, F.text.in_(ConfirmationButtons.get_buttons()))
async def unregister_confirmation(message: Message, state: FSMContext) -> None:
    if message.text == ConfirmationButtons.YES.value:
        await delete_user_profile(message.from_user.id)
        await message.answer("Анкета успешно удалена", reply_markup=MainMenuButtons.markup())
        await cmd_start(message, state)
    else:
        await message.answer("Удаление анкеты отменено", reply_markup=MainMenuButtons.markup())
        await state.clear()
    # await state.clear()


@router.message(Unregistration.confirmation)
async def unregister_confirmation_wrong_choice(message: Message) -> None:
    await message.answer(
        text="Пожалуйста, выберите ответ из списка ниже:",
        reply_markup=ConfirmationButtons.markup(),
    )
