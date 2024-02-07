from keyboard.keyboard_user import create_keyboard_main_menu
from aiogram.fsm.state import default_state
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram import Router
from environs import Env

router = Router()
env = Env()
env.read_env()


@router.message(~StateFilter(default_state))
async def unknown_message(message: Message, state: FSMContext):

    await message.delete()
    if message.text in ['/admin', '/streamer']:
        mes: Message = (await state.get_data())['message_user']

        if (mes.text != LEXICON_RU['not_enough_tights'] and
                message.from_user.id not in list(map(int, env.list('ADMIN_IDS')))):
            await state.update_data(message_user=await mes.edit_text(LEXICON_RU['not_enough_tights'],
                                                                     reply_markup=create_keyboard_main_menu()))
