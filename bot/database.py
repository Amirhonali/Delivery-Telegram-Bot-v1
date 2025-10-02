import psycopg2
import uuid
import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_ROOT = os.path.join(BASE_DIR, "wwwroot", "images")

def connect():
    return psycopg2.connect(
        user="postgres",
        password="4554",
        host="localhost",
        database="food_db",
        port="5433"
    )

# --- Category ---
def get_categories():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM apps_category;")
    rows = cursor.fetchall()
    conn.close()
    return rows

# --- Products ---
def get_products_by_category(category_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, price, image FROM apps_product WHERE cat_id = %s AND active = TRUE;",
        (category_id,)
    )
    rows = cursor.fetchall()
    conn.close()

    result = []
    for prod_id, name, price, image in rows:
        full_path = os.path.join(MEDIA_ROOT, str(image)) if image else None
        result.append((prod_id, name, price, full_path))
    return result

def get_product(prod_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, image FROM apps_product WHERE id = %s;", (prod_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None

    prod_id, name, price, image = row
    full_path = os.path.join(MEDIA_ROOT, str(image)) if image else None
    return (prod_id, name, price, full_path)

# --- User ---
def get_or_create_user(telegram_id, username=None, first_name=None, last_name=None):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM apps_user WHERE telegram_id = %s;", (telegram_id,))
    user = cursor.fetchone()
    if user:
        conn.close()
        return user[0]

    cursor.execute("""
        INSERT INTO apps_user (telegram_id, username, first_name, last_name, created_at)
        VALUES (%s, %s, %s, %s, NOW())
        RETURNING id;
    """, (telegram_id, username, first_name, last_name))
    user_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return user_id

# --- Order ---
def save_order(user_id, cart):
    conn = connect()
    cursor = conn.cursor()
    order_id = str(uuid.uuid4())[:8]

    cursor.execute(
        "INSERT INTO apps_order (user_id, order_id, status, created_at, updated_at) VALUES (%s, %s, %s, %s, %s) RETURNING id",
        (user_id, order_id, "pending", datetime.datetime.now(), datetime.datetime.now())
    )
    order_db_id = cursor.fetchone()[0]

    for prod_id, name, qty, price in cart:
        cursor.execute(
            "INSERT INTO apps_orderitem (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
            (order_db_id, prod_id, qty, price)
        )

    conn.commit()
    conn.close()
    return order_id