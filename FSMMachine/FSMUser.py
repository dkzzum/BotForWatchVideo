from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class FSMDefaultState(StatesGroup):
    default_state = State()


class FSMSendVideo(StatesGroup):
    send_video = State()
