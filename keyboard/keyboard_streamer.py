from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_streamer import STREAMER_MAIN_KB, STREAMER_WATCH_VIDEO_KB


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
