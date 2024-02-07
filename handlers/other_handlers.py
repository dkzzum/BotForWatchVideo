from keyboard.keyboard_main_menu import create_keyboard_main_menu
from aiogram import Router
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.fsm.state import default_state
from FSMMachine.FSM import FSMDefaultState
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


router = Router()


@router.message(~StateFilter(default_state))
async def unknown_message(message: Message, state: FSMContext):
    mes: Message = (await state.get_data())['message_user']

    await message.delete()
