from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def menu_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🍔 Buyurtma berish")],
            [KeyboardButton(text="🛒 Savat")]
        ],
        resize_keyboard=True
    )

def categories_keyboard(categories: list[tuple[int, str]]):
    buttons = [[KeyboardButton(text=name)] for cat_id, name in categories]
    buttons.append([KeyboardButton(text="🔙 Orqaga")])
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )

def product_keyboard(prod_id: int, qty: int = 1):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➖", callback_data=f"dec:{prod_id}:{qty}"),
                InlineKeyboardButton(text=str(qty), callback_data="none"),
                InlineKeyboardButton(text="➕", callback_data=f"inc:{prod_id}:{qty}")
            ],
            [InlineKeyboardButton(text="🛒 Qo‘shish", callback_data=f"add:{prod_id}:{qty}")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_main")]  # faqat bosh menyu
        ]
    )

def cart_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="confirm"),
                InlineKeyboardButton(text="❌ Tozalash", callback_data="clear")
            ]
        ]
    )