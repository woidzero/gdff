from enum import Enum
from typing import Any, List

from aiogram.types import ReplyKeyboardMarkup

from bot.keyboards.base import common_keyboard


class ExtendedEnum(Enum):
    @classmethod
    def _get_name_by_value(cls, value: Any) -> str | None:
        for member in cls:
            if member.value == value:
                return member.name
        return None


class ButtonsEnum(ExtendedEnum):
    row_length: int

    @staticmethod
    def process_button(member: Any) -> str:
        return member

    @classmethod
    def get_buttons(cls) -> List[str]:
        buttons = []
        kb_params = ("row_length",)
        for member in cls:
            if member.name not in kb_params:
                buttons.append(cls.process_button(member.value))

        return buttons

    @classmethod
    def markup(cls) -> ReplyKeyboardMarkup:
        row_width = cls.row_length.value if hasattr(cls, "row_length") else 2
        return common_keyboard(*cls.get_buttons(), row_width=row_width)


class MainMenuButtons(ButtonsEnum):
    row_length = 3
    CHECK_SURVEYS = "👥 Посмотреть анкеты"
    MY_SURVEY = "📝 Моя анкета"
    INFORMATION = "📍 Информация"


class GenericButtons(ButtonsEnum):
    GO_BACK = "Вернуться"
    REGISTER = "Зарегистрироваться"


class ConfirmationButtons(ButtonsEnum):
    YES = "✅ Да"
    NO = "❌ Нет"


class CategoryToId(ExtendedEnum):
    TALKING = 1
    SLAYER = 2
    HOST = 3
    CREATOR_GP = 4
    CREATOR_DECO = 5


class CategorySelectButtons(ButtonsEnum):
    row_length = 5
    TALKING = "Общение"
    SLAYER = "Слеер"
    HOST = "Хост"
    CREATOR_GP = "Креатор (ГП)"
    CREATOR_DECO = "Креатор (Деко)"

    @classmethod
    def get_id_by_name(cls, category: str) -> int | None:
        name = cls._get_name_by_value(category)
        try:
            return getattr(CategoryToId, name).value
        except AttributeError:
            return None

    @classmethod
    def get_name_by_id(cls, id: int) -> str | None:
        category_type = str(CategoryToId._get_name_by_value(id))
        try:
            return getattr(cls, category_type).value
        except AttributeError:
            return "Неизвестная категория"
