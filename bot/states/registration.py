import aiogram
from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove

from bot.database.methods import create_user_profile
from bot.keyboards import KbButtons, ReplyKb

router: Router = Router(name=__name__)


class Registration(StatesGroup):
    choosing_category = State()
    writing_profile_description = State()


@router.message(StateFilter(None), Command("register"))
async def cmd_register(message: Message, state: FSMContext) -> None:
    await message.answer(
        text="Кем вы являтесь и кого хотите найти?", reply_markup=ReplyKb.category_select
    )
    await state.set_state(Registration.choosing_category)


@router.message(Registration.choosing_category, F.text.in_(KbButtons.category_select.keys()))
async def category_chosen(message: Message, state: FSMContext) -> None:
    await state.update_data(chosen_category=KbButtons.category_select[str(message.text)])
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
    user_data = await state.get_data()
    category = KbButtons.category_to_id[user_data["chosen_category"]]
    description = str(message.text)
    if len(description) > 1000:
        await message.answer(
            f"Анкета не должна быть длинее 1000 символов.\n\nТекущая длина: {len(description)}"
        )
        await state.set_state(Registration.writing_profile_description)
        return
    await create_user_profile(
        user_id=message.from_user.id, category=category, description=description  # type: ignore
    )
    await message.answer("Вы успешно зарегистрированы!", reply_markup=ReplyKeyboardRemove())
    await state.clear()
