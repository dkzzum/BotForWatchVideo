from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_admin import ADMIN_KB, KB_WATCH_ADMIN


def create_admin_kb():
    kb = InlineKeyboardBuilder()

    for k, v in ADMIN_KB.items():
        kb.row(
            InlineKeyboardButton(
                text=k,
                callback_data=v
            )
        )

    return kb.as_markup()


def create_admin_watch_kb():
    kb = InlineKeyboardBuilder()

    for k, v in KB_WATCH_ADMIN.items():
        kb.row(
            InlineKeyboardButton(
                text=k,
                callback_data=v
            )
        )
    kb.adjust(2)
    return kb.as_markup()
