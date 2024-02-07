from aiogram.types import CallbackQuery, Message, ContentType
from lexicon.lexicon_ru import LEXICON_RU, DATA_USER
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from keyboard.keyboard_main_menu import *
from aiogram import F, Router
from FSMMachine.FSM import *
from environs import Env
from db.db import *

router = Router()
env = Env()
env.read_env()
router.message.filter(lambda f: f.from_user.id in list(map(int, env.list('STREAMERS_IDS'))))


@router.message(Command('streamer'), StateFilter(FSMDefaultState.default_state))
async def start_streamer_mode(message: Message, state: FSMContext):
    if message.from_user.id not in streamer_db.keys():
        streamer_db[message.from_user.id] = {'num_watch_video': 0}

    mes: Message = (await state.get_data())['message_user']

    await message.delete()
    await state.update_data(first_mes_streamer=(await mes.edit_text(text=LEXICON_STREAMER_RU['start_mode'],
                                                                    reply_markup=create_main_kb_streamer())))
    await state.set_state(FSMStreamerMode.streamer_panel)


@router.callback_query(F.data == 'watch_the_video', StateFilter(FSMStreamerMode.streamer_panel))
async def watch_streamer_video(callback: CallbackQuery, state: FSMContext):
    if len(approved_video) != 0:
        await state.set_state(FSMStreamerMode.watch_the_video)

        await callback.message.answer_video(video=approved_video[streamer_db[callback.from_user.id]['num_watch_video']],
                                            reply_markup=create_watch_video_streamer_kb())
    else:
        if callback.message.text != LEXICON_STREAMER_RU['none_video']:
            await callback.message.edit_text(text=LEXICON_STREAMER_RU['none_video'],
                                             reply_markup=create_main_kb_streamer())
        else:
            await callback.answer()


@router.callback_query(F.data == 'next', StateFilter(FSMStreamerMode.watch_the_video))
async def handler_swipe_video(callback: CallbackQuery, state: FSMContext):
    index = streamer_db[callback.from_user.id]['num_watch_video']
    index += 1

    if index < len(approved_video):
        streamer_db[callback.from_user.id]['num_watch_video'] = index

        await callback.message.delete()
        await callback.message.answer_video(video=approved_video[index],
                                            reply_markup=create_watch_video_streamer_kb())
    else:
        mes: Message = (await state.get_data())['first_mes_streamer']
        await state.set_state(FSMStreamerMode.streamer_panel)

        await callback.message.delete()
        if mes.text != LEXICON_STREAMER_RU['last_video']:
            await state.update_data(first_mes_streamer=await mes.edit_text(text=LEXICON_STREAMER_RU['last_video'],
                                                                           reply_markup=create_main_kb_streamer()))
        else:
            await callback.answer()


@router.callback_query(F.data == 'prew', StateFilter(FSMStreamerMode.watch_the_video))
async def handler_swipe_video(callback: CallbackQuery, state: FSMContext):
    index = streamer_db[callback.from_user.id]['num_watch_video']
    index -= 1

    if index >= 0:
        streamer_db[callback.from_user.id]['num_watch_video'] = index

        await callback.message.delete()
        await callback.message.answer_video(video=approved_video[index],
                                            reply_markup=create_watch_video_streamer_kb())
    else:
        mes: Message = (await state.get_data())['first_mes_streamer']
        await state.set_state(FSMStreamerMode.streamer_panel)

        await callback.message.delete()
        if mes.text != LEXICON_STREAMER_RU['first_video']:
            await state.update_data(first_mes_streamer=await mes.edit_text(text=LEXICON_STREAMER_RU['first_video'],
                                                                           reply_markup=create_main_kb_streamer()))
        else:
            await callback.answer()


@router.callback_query(F.data == 'finish_watching_video', StateFilter(FSMStreamerMode.watch_the_video))
async def finish_watching_video(callback: CallbackQuery, state: FSMContext):
    mes: Message = (await state.get_data())['first_mes_streamer']

    await callback.message.delete()

    await state.set_state(FSMStreamerMode.streamer_panel)

    if LEXICON_STREAMER_RU['start_mode'] != mes.text:
         await state.update_data(first_mes_streamer=await mes.edit_text(text=LEXICON_STREAMER_RU['start_mode'],
                                 reply_markup=create_main_kb_streamer()))


@router.callback_query(F.data == 'end_session_streamer', StateFilter(FSMStreamerMode.streamer_panel))
async def end_session_streamer(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMDefaultState.default_state)
    await callback.message.edit_text(text=LEXICON_RU['start'],
                                     reply_markup=create_keyboard_main_menu())
