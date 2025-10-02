from aiogram import Router, types

from bot.database import get_product, get_or_create_user, save_order
from bot.keyboards import product_keyboard, cart_keyboard, menu_keyboard
from bot.utils import add_to_cart, clear_cart, get_cart, format_cart

router = Router()

@router.callback_query()
async def callbacks(call: types.CallbackQuery):
    data = call.data
    if ":" in data:
        action, prod_id, qty = data.split(":")
        prod_id = int(prod_id)
        qty = int(qty)
    else:
        action = data
        prod_id = None
        qty = 1

    if action == "inc":
        qty += 1
        await call.message.edit_reply_markup(
            reply_markup=product_keyboard(prod_id, qty)
        )
    elif action == "dec" and qty > 1:
        qty -= 1
        await call.message.edit_reply_markup(
            reply_markup=product_keyboard(prod_id, qty)
        )
    elif action == "add":
        prod = get_product(prod_id)
        add_to_cart(call.from_user.id, prod[0], prod[1], qty, float(prod[2]))
        await call.answer("✅ Savatchaga qo‘shildi")
    elif action == "back_main":
        await call.message.answer(
            "🏠 Bosh menyu:",
            reply_markup=menu_keyboard()
        )
    elif action == "clear":
        clear_cart(call.from_user.id)
        await call.message.answer("🗑 Savat tozalandi")
    elif action == "confirm":
        cart = get_cart(call.from_user.id)
        if not cart:
            await call.message.answer("❌ Savat bo‘sh")
            return
        user_id = get_or_create_user(call.from_user.id, call.from_user.username, call.from_user.first_name, call.from_user.last_name)
        order_id = save_order(user_id, [(p, q, price) for p, _, q, price in cart])
        await call.message.answer(f"✅ Buyurtma #{order_id} qabul qilindi!")
        clear_cart(call.from_user.id)

@router.message(lambda m: m.text == "🛒 Savat")
async def show_cart(message: types.Message):
    cart = get_cart(message.from_user.id)
    await message.answer(format_cart(cart), reply_markup=cart_keyboard())