from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def reply_markup(products):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for product in products:
        product_id, name, *_ = product
        button = KeyboardButton(text=name)
        keyboard.insert(button)
    return keyboard

