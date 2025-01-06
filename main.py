from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatMemberUpdated
# from aiogram.filters import 
from aiogram.enums import ChatMemberStatus
from aiogram import Router
import logging
from dotenv import load_dotenv
import os
import asyncio

# Load environment variables
load_dotenv()
API_TOKEN = os.getenv('BOT_TOKEN')


tabrik_text = """Tabriklaymiz!
Siz <b>Maqsadli Inson Club</b>ga azo bo'ldingiz! 🎉
Endi clubda ajoyib imkoniyatlar va yangiliklarni kuzatib boring.
Darxol clubga qo'shilib o'ling va muvaffaqiyat sari birgalikda qadam qo'ying! 💪
<a href="https://t.me/Maqsadli_inson2025">Qo'shilish uchun tugma</a>"""


# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()

# Logging setup
logging.basicConfig(level=logging.INFO)

# Inline buttons
keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Maqsadli inson', url='https://t.me/maqsadli_inson2025')],
    [InlineKeyboardButton(text='Davron Turdiyev zapislar', url='https://t.me/DTurdiyev_marafons')],
])

# Handle new chat member requests
@router.chat_join_request()
async def new_chat_member(update: types.ChatJoinRequest):
    # print(update)
    await update.approve()
    # send message to from user
    # await bot.send_message(
    #     chat_id=update.from_user.id,
    #     text="Salom! Reklama xabari:",
    #     reply_markup=keyboard
    # )
    

# Handle /start and text messages
@router.message(F.text)
async def handle_messages(message: types.Message):
    await message.answer(
        text=tabrik_text,
        reply_markup=keyboard,
        parse_mode='HTML'
    )

async def main():
    # Include the router
    dp.include_router(router)

    # Start polling
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
