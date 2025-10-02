import psycopg2
from psycopg2.extras import RealDictCursor
import uuid

def connect():
    return psycopg2.connect(
        user="postgres",
        password="4554",
        host="localhost",
        port="5433",
        database="food_db"
    )

# --- USER ---
def get_or_create_user(telegram_id, username=None, first_name=None, last_name=None):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM apps_user WHERE telegram_id = %s", (telegram_id,))
    user = cursor.fetchone()
    if not user:
        cursor.execute(
            "INSERT INTO apps_user (telegram_id, username, first_name, last_name) VALUES (%s, %s, %s, %s) RETURNING id",
            (telegram_id, username, first_name, last_name)
        )
        user_id = cursor.fetchone()[0]
        conn.commit()
    else:
        user_id = user[0]
    conn.close()
    return user_id

# --- CATEGORY ---
def get_categories():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM apps_category;")
    result = cursor.fetchall()
    conn.close()
    return result

# --- PRODUCT ---
def get_products_by_category(category_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, image, '' as desc FROM apps_product WHERE cat_id = %s;", (category_id,))
    result = cursor.fetchall()
    conn.close()
    return result

# --- ORDER ---
def save_order(user_id, cart):
    """
    cart = [(prod_id, qty, price), ...]
    """
    conn = connect()
    cursor = conn.cursor()
    order_id = str(uuid.uuid4())[:8]  # unikal order ID

    cursor.execute(
        "INSERT INTO apps_order (user_id, order_id, status) VALUES (%s, %s, %s) RETURNING id",
        (user_id, order_id, "pending")
    )
    order_db_id = cursor.fetchone()[0]

    for prod_id, qty, price in cart:
        cursor.execute(
            "INSERT INTO apps_orderitem (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
            (order_db_id, prod_id, qty, price)
        )
    conn.commit()
    conn.close()
    return order_id