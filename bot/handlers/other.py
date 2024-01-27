from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove

from bot.database.methods import create_user, is_registered_user

from bot.keyboards.main import MainMenuButtons
from bot.states.registration import cmd_register

router = Router()


@router.message(F.text == MainMenuButtons.INFORMATION.value)
@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        text=f"{message.from_user.first_name}, Добро пожаловать в GMD DVN!\n\n"
        "Зарегистрируйтесь с помощью /register\n"
        "Удалить анкету: /unregister\n"
        "Просмотреть свою анкету: /my_profile\n"
        "Посмотреть случайный профиль: /random_profile",
        reply_markup=MainMenuButtons.markup(),
    )
    await create_user(message.from_user.id, name=message.from_user.full_name)

    is_registered = await is_registered_user(message.from_user.id)
    if not is_registered:
        await message.answer("Перед использованием бота необходимо пройти регистрацию")
        await cmd_register(message, state)


# Нетрудно догадаться, что следующие два хэндлера можно объединить в один


@router.message(default_state, Command(commands=["cancel"]))
@router.message(default_state, F.text.lower() == "отмена")
async def cmd_cancel_no_state(message: Message, state: FSMContext) -> None:
    # Стейт сбрасывать не нужно, удалим только данные
    await state.set_data({})
    await message.answer(text="Нечего отменять", reply_markup=ReplyKeyboardRemove())


@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(text="Действие отменено", reply_markup=ReplyKeyboardRemove())
