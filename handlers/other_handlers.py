from keyboard.keyboard_main_menu import *
from aiogram import Router
from lexicon.lexicon_ru import LEXICON_RU, DATA_USER
from FSMMachine.FSM import FSMSendVideo, FSMDefaultState
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


router = Router()


@router.message(StateFilter(FSMDefaultState.default_state))
async def unknown_message(message: Message, state: FSMContext):
    mes: Message = (await state.get_data())['message_user']

    await message.delete()
    if mes.text != LEXICON_RU['unknown_message']:
        await state.update_data(message_user=await mes.edit_text(LEXICON_RU['unknown_message'],
                                                                 reply_markup=create_keyboard_main_menu()))
