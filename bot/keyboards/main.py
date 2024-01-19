from dataclasses import dataclass

from .base import common_keyboard


@dataclass
class KbButtons:
    go_back = "Вернутся"

    main = {
        "👥 Посмотреть анкеты": "check_surveys",
        "📝 Моя анкета": "my_servey",
        "📍 Информация": "information",
    }

    category_select = {
        "Общение": "talking",
        "Слеер": "slayer",
        "Хост": "host",
        "Креатор (ГП)": "creator_gp",
        "Креатор (Деко)": "creator_deco",
    }
    category_to_id = {
        "talking": 1,
        "slayer": 2,
        "host": 3,
        "creator_gp": 4,
        "creator_deco": 5,
    }


@dataclass
class ReplyKb:
    main = common_keyboard(*KbButtons.main.keys())

    category_select = common_keyboard(
        *KbButtons.category_select.keys(),
        KbButtons.go_back,
        row_width=3,
    )
