from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message, ContentType
from lexicon.lexicon_ru import LEXICON_RU, DATA_USER
from FSMMachine.FSM import FSMSendVideo, FSMDefaultState
from db.db import *
from keyboard.keyboard_main_menu import *

router = Router()


def read_data_bd(user_id: int):
    user = {}
    for k, v in DATA_USER.items():
        user[k] = v

    db[user_id] = user


@router.message(CommandStart(), StateFilter(default_state, FSMDefaultState.default_state))
async def command_send_start(message: Message, state: FSMContext):
    await state.set_state(FSMDefaultState.default_state)
    await state.update_data(message_user=await message.answer(LEXICON_RU['start'],
                                                              reply_markup=create_keyboard_main_menu()))

    read_data_bd(message.from_user.id)


@router.message(Command(commands='help'), StateFilter(FSMDefaultState.default_state))
async def command_send_help(message: Message, state: FSMContext):
    mes: Message = (await state.get_data())['message_user']

    await message.delete()
    await mes.edit_text(LEXICON_RU['help'],
                        reply_markup=create_keyboard_main_menu())


@router.callback_query(F.data == 'help', StateFilter(FSMDefaultState.default_state))
async def callback_send_help(callback: CallbackQuery):
    if callback.message.text != LEXICON_RU['help']:
        await callback.message.edit_text(LEXICON_RU['help'],
                                         reply_markup=create_keyboard_main_menu())
    else:
        await callback.answer()


@router.callback_query(F.data == 'profile', StateFilter(FSMDefaultState.default_state))
async def callback_send_profile(callback: CallbackQuery):
    data_user = (f'{callback.from_user.username}\n\n'
                 f'Отправлено видео: {db[callback.from_user.id]['send_video']}\n'
                 f'Прошедших модерацию: {db[callback.from_user.id]['accepted_videos']}')

    if data_user == callback.message.text:
        await callback.answer()
    else:
        await callback.message.edit_text(text=data_user,
                                         reply_markup=create_keyboard_main_menu())


@router.message(StateFilter(FSMDefaultState.default_state))
async def unknown_message(message: Message, state: FSMContext):
    mes: Message = (await state.get_data())['message_user']

    await message.delete()
    await mes.edit_text(LEXICON_RU['unknown_message'],
                        reply_markup=create_keyboard_main_menu())


@router.callback_query(F.data == 'send_video', StateFilter(FSMDefaultState.default_state))
async def callback_send_vidio(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(LEXICON_RU['send_video'],
                                     reply_markup=create_kb_state_send_video())

    await state.update_data(message=callback.message)
    await state.set_state(FSMSendVideo.send_video)


@router.message(F.content_type == ContentType.VIDEO, StateFilter(FSMSendVideo.send_video))
async def message_send_video(message: Message, state: FSMContext):
    if message.video.file_unique_id not in all_video:
        await message.delete()
        mes: Message = (await state.get_data())['message']
        await mes.edit_text(LEXICON_RU['load_video'],
                            reply_markup=create_keyboard_main_menu())

        db[message.from_user.id]['video_list'][message.video.file_unique_id] = message.video.file_id
        all_video.append(message.video.file_unique_id)
        db[message.from_user.id]['send_video'] += 1
        deque_for_admins.append([message.video.file_id, False])
        await state.set_state(FSMDefaultState.default_state)
    else:
        mes: Message = (await state.get_data())['message']

        await message.delete()
        await mes.edit_text(LEXICON_RU['send_repeated_video'],
                            reply_markup=create_kb_state_send_video())


@router.message(StateFilter(FSMSendVideo.send_video))
async def message_error_send_video(message: Message, state: FSMContext):
    mes: Message = (await state.get_data())['message']

    await message.delete()
    await mes.edit_text(LEXICON_RU['error_send_video'],
                        reply_markup=create_kb_state_send_video())


@router.callback_query(F.data == 'cancellation', StateFilter(FSMSendVideo.send_video))
async def cancellation_send_video(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(LEXICON_RU['cancellation_send_video'],
                                     reply_markup=create_keyboard_main_menu())

    await state.set_state(FSMDefaultState.default_state)
