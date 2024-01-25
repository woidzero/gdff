import aiogram
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.types import Message

from bot.database.methods import create_user_profile
from bot.keyboards import KbButtons, ReplyKb
from bot.keyboards.base import common_keyboard

router: Router = Router(name=__name__)


class Registration(StatesGroup):
    name = State()
    choosing_category = State()
    writing_profile_description = State()


@router.message(default_state, Command("register"))
async def cmd_register(message: Message, state: FSMContext) -> None:
    await message.answer(
        text="Введите своё имя", reply_markup=common_keyboard(message.from_user.full_name)
    )
    await state.set_state(Registration.name)


@router.message(Registration.name)
async def state_category(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await message.answer(
        text="Кем вы являтесь и кого хотите найти?", reply_markup=ReplyKb.category_select
    )
    await state.set_state(Registration.choosing_category)


@router.message(Registration.choosing_category, F.text.in_(KbButtons.category_select.values()))
async def category_chosen(message: Message, state: FSMContext) -> None:
    category = KbButtons.category_select.get_key(str(message.text))
    category_id = KbButtons.category_to_id.get_value(category)
    await state.update_data(category_id=category_id)

    await message.answer(
        text="Теперь, пожалуйста, расскажите о себе:",
        reply_markup=aiogram.types.ReplyKeyboardRemove(),
    )
    await state.set_state(Registration.writing_profile_description)


@router.message(Registration.choosing_category)
async def category_chosen_incorrectly(message: Message) -> None:
    await message.answer(
        text="Пожалуйста, выберите категорию из списка ниже:", reply_markup=ReplyKb.category_select
    )


@router.message(Registration.writing_profile_description)
async def description_filled(message: Message, state: FSMContext) -> None:
    description = str(message.text)
    if len(description) > 1000:
        await message.answer(
            f"Анкета не должна быть длинее 1000 символов.\n\nТекущая длина: {len(description)}"
        )
        await state.set_state(Registration.writing_profile_description)
        return

    user_data = await state.get_data()
    category_id = user_data.get("category_id")
    name = user_data.get("name")
    await create_user_profile(
        user_id=message.from_user.id, name=name, category_id=category_id, description=description
    )
    await message.answer("Вы успешно зарегистрированы!", reply_markup=ReplyKb.main)
    await state.clear()
