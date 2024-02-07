from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_ru import *


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


def create_main_kb_streamer():
    kb = InlineKeyboardBuilder()

    for k, v in STREAMER_MAIN_KB.items():
        kb.row(
            InlineKeyboardButton(
                text=k,
                callback_data=v
            )
        )

    return kb.as_markup()


def create_watch_video_streamer_kb():
    kb = InlineKeyboardBuilder()

    for k, v in STREAMER_WATCH_VIDEO_KB.items():
        kb.row(
            InlineKeyboardButton(
                text=k,
                callback_data=v
            )
        )

    kb.adjust(2, 1)
    return kb.as_markup()
