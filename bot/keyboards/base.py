from typing import Optional

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def common_keyboard(
    *texts: str,
    is_persistent: Optional[bool] = None,
    resize_keyboard: bool = True,
    one_time_keyboard: Optional[bool] = None,
    input_field_placeholder: Optional[str] = None,
    selective: Optional[bool] = None,
    row_width: int = 2,
) -> ReplyKeyboardMarkup:
    """
    Common reply keyboards build helper.
    """
    builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    builder.row(*[KeyboardButton(text=text) for text in texts], width=row_width)
    return builder.as_markup(
        is_persistent=is_persistent,
        resize_keyboard=resize_keyboard,
        one_time_keyboard=one_time_keyboard,
        input_field_placeholder=input_field_placeholder,
        selective=selective,
    )


class BidirectionalDict:
    def __init__(self, my_dict: Optional[dict] = None):
        self.forward_dict = {}
        self.reverse_dict = {}

        if my_dict:
            for key, value in my_dict.items():
                self.add_mapping(key, value)

    def add_mapping(self, key, value):
        self.forward_dict[key] = value
        self.reverse_dict[value] = key

    def get_key(self, value):
        return self.reverse_dict.get(value)

    def get_value(self, key):
        return self.forward_dict.get(key)

    # @property
    def values(self):
        return self.forward_dict.values()

    # @property
    def keys(self):
        return self.forward_dict.keys()

    def __getitem__(self, key):
        return self.get_value(key)
