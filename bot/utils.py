carts = {}

def add_to_cart(user_id, prod_id, name, qty, price):
    if user_id not in carts:
        carts[user_id] = []
    carts[user_id].append((prod_id, name, qty, price))

def get_cart(user_id):
    return carts.get(user_id, [])

def clear_cart(user_id):
    carts[user_id] = []

def format_cart(cart):
    if not cart:
        return "🛒 Savat bo‘sh!"
    text = "🛒 Sizning savatingiz:\n\n"
    total = 0
    for prod_id, name, qty, price in cart:
        subtotal = qty * float(price)
        total += subtotal
        text += f"🍣 {name} x {qty} = {subtotal:.0f} so‘m\n"
    text += f"\n💵 Jami: {total:.0f} so‘m"
    return text