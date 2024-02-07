from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_ru import KB_MENU, KB_STATE_SEND_VIDEO


def create_keyboard_main_menu():
    kb = InlineKeyboardBuilder()

    for k, v in KB_MENU.items():
        kb.row(
            InlineKeyboardButton(
                text=k,
                callback_data=v
            )
        )
    kb.adjust(2, 1)
    return kb.as_markup()


def create_kb_state_send_video():
    kb = InlineKeyboardBuilder()

    for k, v in KB_STATE_SEND_VIDEO.items():
        kb.row(
            InlineKeyboardButton(
                text=k,
                callback_data=v
            )
        )

    return kb.as_markup()



