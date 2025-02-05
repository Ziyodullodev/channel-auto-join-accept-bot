from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatMemberUpdated
from aiogram.filters import CommandStart
from aiogram.enums import ChatMemberStatus
from texts import *
from aiogram import Router
import logging
from dotenv import load_dotenv
from functions import add_user, users_stat
import os, json
import asyncio

load_dotenv()
API_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()

@router.message(CommandStart())
async def start_dispatcher(message: types.Message):
    first_name = message.from_user.first_name
    chat_id = message.chat.id
    await message.answer(
        text=start_text.format(first_name=first_name),
        parse_mode='HTML'
    )
    await add_user(message)
    
    
@router.chat_join_request()
async def new_chat_member(update: types.ChatJoinRequest):
    await update.approve()
    try:
        await bot.send_message(
            chat_id=update.from_user.id,
            text=default_accept_text,
            parse_mode='HTML'
        )
    except Exception as e:
        pass
    
    await add_user(update)

@router.message(F.text)
async def handle_messages(message: types.Message):
    chat_id = message.chat.id
    if chat_id < 0:
        return
    text = message.text
    if text == '/stat' and str(message.from_user.id) == ADMIN_ID:
        statistic = await users_stat()
        return await message.answer(statistic_text.format(statistic=statistic), parse_mode='HTML')
    elif text == '/load' and str(message.from_user.id) == ADMIN_ID:
        try:
            file = types.FSInputFile("users.json")
            await message.answer_document(file)
        except Exception as e:
            await message.answer(str(e))
        return
    return await message.answer(about_text, parse_mode='HTML')

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
