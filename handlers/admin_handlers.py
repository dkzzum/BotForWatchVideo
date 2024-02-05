from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message, ContentType
from lexicon.lexicon_ru import LEXICON_RU, DATA_USER
from FSMMachine.FSM import *
from db.db import *
from environs import Env
from keyboard.keyboard_main_menu import *

router = Router()
env = Env()
env.read_env()
router.message.filter(lambda f: f.from_user.id in list(map(int, env.list('ADMIN_IDS'))))


@router.message(StateFilter(FSMDefaultState.default_state), Command('admin'))
async def start_admin_menu(message: Message, state: FSMContext):
    mes: Message = (await state.get_data())['message_user']

    await message.delete()

    await state.update_data(first_message_admin=await mes.edit_text(ADMIN_MENU['start'],
                                                                    reply_markup=create_admin_kb()))
    await state.set_state(FSMAdmins.admin_panel)


@router.callback_query(F.data == 'new_video', StateFilter(FSMAdmins.admin_panel))
async def watch_moder_video(callback: CallbackQuery, state: FSMContext):
    i = 0
    while len(deque_for_admins) > i and deque_for_admins[i][1] is True:
        i += 1

    if len(deque_for_admins) <= i:
        await callback.message.edit_text(ADMIN_MENU['end'],
                                         reply_markup=create_admin_kb())
    else:
        await state.set_state(FSMAdmins.watch_the_video)
        await state.update_data(index=i)
        deque_for_admins[i][1] = True
        await callback.message.answer_video(video=deque_for_admins[i][0],
                                            reply_markup=create_admin_watch_kb())


@router.callback_query(F.data.in_(['True', 'False']), StateFilter(FSMAdmins.watch_the_video))
async def decision_making(callback: CallbackQuery, state: FSMContext):
    index = (await state.get_data())['index']

    if callback.data == 'True':
        approved_video.append(deque_for_admins[index][0])

        db[callback.from_user.id]['accepted_videos'] += 1

    deque_for_admins.remove(deque_for_admins[index])

    i = 0
    while len(deque_for_admins) > i and deque_for_admins[i][1] is not False:
        i += 1

    if len(deque_for_admins) <= i:
        mes: Message = (await state.get_data())['first_message_admin']

        await callback.message.delete()
        await mes.edit_text(ADMIN_MENU['end'],
                            reply_markup=create_admin_kb())
    else:
        await state.update_data(index=i)
        deque_for_admins[i][1] = True
        await callback.message.delete()
        await callback.message.answer_video(video=deque_for_admins[i][0],
                                            reply_markup=create_admin_watch_kb())


@router.callback_query(F.data == 'end_session', StateFilter(FSMAdmins.watch_the_video))
async def end_watch_video_admin(callback: CallbackQuery, state: FSMContext):
    index = (await state.get_data())['index']
    deque_for_admins[index][1] = False
    await state.set_state(FSMAdmins.admin_panel)
    await callback.message.delete()


@router.callback_query(F.data == 'exit_admin', ~StateFilter(default_state))
async def exit_for_admin_menu(callback: CallbackQuery, state: FSMContext):
    if callback.message.text != LEXICON_RU['help']:
        await callback.message.edit_text(LEXICON_RU['help'],
                                         reply_markup=create_keyboard_main_menu())
    else:
        await callback.message.answer()

    await state.set_state(FSMDefaultState.default_state)


@router.message(Command(commands='help'), StateFilter(FSMAdmins.admin_panel))
async def command_send_help(message: Message, state: FSMContext):
    mes: Message = (await state.get_data())['message_user']

    await message.delete()
    await mes.edit_text(LEXICON_RU['help'],
                        reply_markup=create_admin_kb())


@router.message(StateFilter(FSMAdmins.admin_panel, FSMAdmins.watch_the_video))
async def unknown_message(message: Message):
    await message.delete()
