from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup


class FSMSendVideo(StatesGroup):
    send_video = State()


class FSMAdmins(StatesGroup):
    admin_panel = State()
    watch_the_video = State()

