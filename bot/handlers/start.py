from aiogram import Router, types
from aiogram.filters import Command

from bot.database import get_or_create_user
from bot.keyboards import menu_keyboard

router = Router()

@router.message(Command("start"))
async def start_command(message: types.Message):
    get_or_create_user(
        message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )
    await message.answer("👋 Salom! Buyurtma berishga tayyormisiz?", reply_markup=menu_keyboard())