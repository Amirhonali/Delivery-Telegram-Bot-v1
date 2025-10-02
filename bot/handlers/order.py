import os
from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from bot.database import get_categories, get_products_by_category
from bot.keyboards import categories_keyboard, product_keyboard, menu_keyboard
from bot.states import OrderStates

router = Router()

@router.message(lambda m: m.text == "🍔 Buyurtma berish")
async def order_start(message: types.Message, state: FSMContext):
    categories = get_categories()
    await message.answer("🍴 Kategoriya tanlang:", reply_markup=categories_keyboard(categories))
    await state.set_state(OrderStates.choosing_category)

@router.message(OrderStates.choosing_category)
async def choose_category(message: types.Message, state: FSMContext):
    if message.text == "🔙 Orqaga":
        await message.answer("🏠 Bosh menyu:", reply_markup=menu_keyboard())
        await state.clear()
        return

    categories = get_categories()
    category_dict = {name: cat_id for cat_id, name in categories}
    if message.text not in category_dict:
        await message.answer("❌ Noto‘g‘ri tanlov, qaytadan urinib ko‘ring.")
        return

    cat_id = category_dict[message.text]
    products = get_products_by_category(cat_id)

    for prod_id, name, price, image in products:
        caption = f"{name}\n💵 {int(price)} so‘m"
        if image and os.path.exists(image):
            with open(image, "rb") as photo:
                await message.answer_photo(photo, caption=caption, reply_markup=product_keyboard(prod_id))
        else:
            await message.answer(caption, reply_markup=product_keyboard(prod_id))

    await state.set_state(OrderStates.choosing_product)