from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message, ContentType
from lexicon.lexicon_ru import LEXICON_RU, DATA_USER
from FSMMachine.FSM import FSMSendVideo
from db.db import *
from keyboard.keyboard_main_menu import *

router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def command_start(message: Message):
    await message.answer(LEXICON_RU['start'],
                         reply_markup=create_keyboard_main_menu())
    print(message.from_user.id)
    user = {}
    for k, v in DATA_USER.items():
        user[k] = v

    db[message.from_user.id] = user


@router.message(Command(commands='help'), StateFilter(default_state))
async def command_help(message: Message):
    await message.answer(LEXICON_RU['help'],
                         reply_markup=create_keyboard_main_menu())


@router.callback_query(F.data == 'help', StateFilter(default_state))
async def callback_help(callback: CallbackQuery):
    if callback.message.text != LEXICON_RU['help']:
        await callback.message.edit_text(LEXICON_RU['help'],
                                         reply_markup=create_keyboard_main_menu())
    else:
        await callback.answer()


@router.message(StateFilter(default_state))
async def unknown_message(message: Message):
    await message.answer(LEXICON_RU['unknown_message'],
                         reply_markup=create_keyboard_main_menu())
    print(message.from_user.id)


@router.callback_query(F.data == 'send_video', StateFilter(default_state))
async def callback_send_vidio(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(LEXICON_RU['send_video'],
                                     reply_markup=create_kb_state_send_video())

    await state.set_state(FSMSendVideo.send_video)


@router.message(F.content_type == ContentType.VIDEO, StateFilter(FSMSendVideo.send_video))
async def message_send_video(message: Message, state: FSMContext):
    if message.video.file_unique_id not in all_video:
        await message.answer(LEXICON_RU['load_video'],
                             reply_markup=create_keyboard_main_menu())

        db[message.from_user.id]['video_list'][message.video.file_unique_id] = message.video.file_id
        all_video.append(message.video.file_unique_id)
        db[message.from_user.id]['send_video'] += 1
        deque_for_admins.append([message.video.file_id, False])
        print(deque_for_admins)
        await state.clear()
    else:
        await message.answer(LEXICON_RU['send_repeated_video'],
                             reply_markup=create_kb_state_send_video())


@router.message(StateFilter(FSMSendVideo.send_video))
async def message_error_send_video(message: Message):
    await message.answer(LEXICON_RU['error_send_video'],
                         reply_markup=create_kb_state_send_video())


@router.callback_query(F.data == 'cancellation', StateFilter(FSMSendVideo.send_video))
async def cancellation_send_video(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(LEXICON_RU['cancellation_send_video'],
                                     reply_markup=create_keyboard_main_menu())

    await state.clear()
