import aiogram
from aiogram import F
from aiogram.dispatcher.router import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove
from db import get_user, new_user

from src.keyboards import common_keyboard

category_kb_classification = {
    "talking": "Общение",
    "slayer": "Слеер",
    "host": "Хост",
    "creator_gp": "Креатор (ГП)",
    "creator_deco": "Креатор (Деко)",
    "go_back": "Вернутся",
}

category_to_id = {category: id for id, category in enumerate(category_kb_classification.values(), 1)}

category_keyboard_buttons = list(category_kb_classification.values())

category_keyboard = common_keyboard(*category_keyboard_buttons, row_width=3)

router = Router()


class Registration(StatesGroup):
    choosing_category = State()
    writing_profile_description = State()


@router.message(StateFilter(None), Command("register"))
async def cmd_register(message: Message, state: FSMContext):
    try:
        user = await get_user(message.from_user.id)
        if user.get("reg_time"):
            await message.answer("Вы уже зарегистрированы. Ваша прошлая анкета будет перезаписанна.")
            # todo: ask for profile deletion
    except:
        pass

    await message.answer(text="Кем вы являтесь и кого хотите найти?", reply_markup=category_keyboard)
    await state.set_state(Registration.choosing_category)


@router.message(Registration.choosing_category, F.text.in_(category_keyboard_buttons))
async def category_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_category=message.text)
    await message.answer(
        text="Теперь, пожалуйста, расскажите о себе:", reply_markup=aiogram.types.ReplyKeyboardRemove()
    )
    await state.set_state(Registration.writing_profile_description)


@router.message(Registration.choosing_category)
async def category_chosen_incorrectly(message: Message):
    await message.answer(text="Пожалуйста, выберите категорию из списка ниже:", reply_markup=category_keyboard)


@router.message(Registration.writing_profile_description)
async def description_filled(message: Message, state: FSMContext):
    user_data = await state.get_data()
    try:
        user = await get_user(message.from_user.id)
        if user.get("reg_time"):
            await message.answer("Анкета не перезаписанна", reply_markup=ReplyKeyboardRemove())
            # todo: edit user profile
    except:
        await new_user(
            full_name=message.from_user.full_name,
            category=category_to_id[user_data["chosen_category"]],
            user_details=message.text,
            user_id=message.from_user.id,
            user_picture="",
        )
        await message.answer("Вы успешно зарегистрированы!", reply_markup=ReplyKeyboardRemove())
    await state.clear()
