from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class FSMStreamerMode(StatesGroup):
    streamer_panel = State()
    watch_the_video = State()
