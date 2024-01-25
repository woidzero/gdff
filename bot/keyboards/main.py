from dataclasses import dataclass

from .base import BidirectionalDict, common_keyboard


@dataclass
class KbButtons:
    go_back = "Вернутся"

    main = BidirectionalDict(
        {
            "check_surveys": "👥 Посмотреть анкеты",
            "my_servey": "📝 Моя анкета",
            "information": "📍 Информация",
        }
    )

    category_select = BidirectionalDict(
        {
            "talking": "Общение",
            "slayer": "Слеер",
            "host": "Хост",
            "creator_gp": "Креатор (ГП)",
            "creator_deco": "Креатор (Деко)",
        }
    )
    category_to_id = BidirectionalDict(
        {
            "talking": 1,
            "slayer": 2,
            "host": 3,
            "creator_gp": 4,
            "creator_deco": 5,
        }
    )


@dataclass
class ReplyKb:
    main = common_keyboard(*KbButtons.main.values(), row_width=3)

    category_select = common_keyboard(
        *KbButtons.category_select.values(),
        KbButtons.go_back,
        row_width=3,
    )
