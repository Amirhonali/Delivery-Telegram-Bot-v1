import asyncio
from aiogram import Bot, Router, F, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import (Message, FSInputFile, KeyboardButton,
                           ReplyKeyboardMarkup,InlineKeyboardMarkup, InlineKeyboardButton)


bot = Bot("")
rr = Router()
dp = Dispatcher()
dp.include_router(rr)
class Register(StatesGroup):
    main_menu = State()