from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup


class FSMSendVideo(StatesGroup):
    send_video = State()


class FSMAdmins(StatesGroup):
    admin_panel = State()
    watch_the_video = State()


class FSMDefaultState(StatesGroup):
    default_state = State()


class FSMStreamerMode(StatesGroup):
    streamer_panel = State()
    watch_the_video = State()
