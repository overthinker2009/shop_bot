import sqlite3
from ctypes import c_char


def create_user_table():
    database = sqlite3.connect('shop.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name VARCHAR(70),
        telegram_id BIGINT NOT NULL UNIQUE,
        phone VARCHAR(25)
    );
    ''')
    database.commit()
    database.close()


def create_carts_table():
    database = sqlite3.connect('shop.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS carts(
        cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER REFERENCES users(user_id),
        total_price DECIMAL(9, 2) DEFAULT 0,
        total_products INTEGER DEFAULT 0
    );
    ''')
    database.commit()
    database.close()

def create_cart_products_table():
    database = sqlite3.connect('shop.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart_products(
        cart_product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name VARCHAR(50),
        quantity INTEGER NOT NULL DEFAULT 0,
        final_price DECIMAL(9, 2) NOT NULL,
        cart_id INTEGER REFERENCES carts(cart_id),
        UNIQUE(product_name, cart_id)
    )
    ''')
    database.commit()
    database.close()


def create_categories_table():
    database = sqlite3.connect('shop.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories(
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name VARCHAR(30) NOT NULL UNIQUE
    )
    ''')
    database.commit()
    database.close()


def create_products_table():
    database = sqlite3.connect('shop.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products(
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER NOT NULL,
        product_name VARCHAR(50) NOT NULL UNIQUE,
        price DECIMAL(9, 2) NOT NULL,
        description VARCHAR(150),
        image TEXT,
        FOREIGN KEY(category_id) REFERENCES categories(category_id)
    )
    ''')
    database.commit()
    database.close()

# create_user_table()
# create_carts_table()
# create_cart_products_table()
# create_categories_table()
# create_products_table()

def insert_categories(info):
    database = sqlite3.connect('shop.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO categories(category_name)
    VALUES (?)
    ''', (info,))
    database.commit()
    database.close()
    return True


# category_info = ['Пиццы', 'Бургеры', 'Лаваши', 'Combo set', 'Напитки', 'Хот-доги']
# for i in category_info:
#     if insert_categories(i):
#         print(f'Successfully added - {i}!')


def insert_products_table(category_id, product_name, price, description, image):
    database = sqlite3.connect('shop.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO products(category_id, product_name, price, description, image)
    VALUES (?, ?, ?, ?, ?)
    ''', (category_id, product_name, price, description, image))
    database.commit()
    database.close()
    return True


product_info = [
    [1, 'Пеперони', 70000, 'Тесто, колбаса, сыр, соус', 'media/pizza/img.png'],
    [2, 'Cheese burger', 40000, 'Булочка, сыр, котлета, салатный лист', 'media/burgers/img.png'],
    [3, 'Лаваш', 32000, 'тесто для лаваша, мясо, чипсы, помидоры, огурцы, лук', 'media/lavash/img.png']
]

product_info_2 = [
    [5, 'Coca cola 0.5', 8000, '1 l', 'media/drinks/img.png'],
    [5, 'Coca cola 1', 13000, '1 l', 'media/drinks/img_1.png'],
    [5, 'Coca cola 1.5', 15000, '1.5 l', 'media/drinks/img_2.png'],
    [6, 'Хот-дог classic', 18000, 'булочка, сосиска, салат, кетчуп, майонез', 'media/hot_dog/img.png'],
    [4, 'Combo traditsiya', 45000, 'club sendvich, cola 0.5, free', 'media/combo/img.png'],
]

# for i in product_info_2:
#     if insert_products_table(i[0], i[1], i[2], i[3], i[4]):
#         print(f'{i[1]}- успешно добавлен!')


def first_register_user(chat_id, full_name):
    database = sqlite3.connect('shop.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO users(telegram_id, full_name)
    VALUES (?, ?)
    ''', (chat_id, full_name))
    database.commit()
    database.close()
    return True


def update_user_to_finish_register(chat_id, phone):
    database = sqlite3.connect('shop.db')
    cursor = database.cursor()
    cursor.execute('''
    UPDATE users
    SET phone = ?
    WHERE telegram_id = ?
    ''', (phone, chat_id))
    database.commit()
    database.close()
    return True


def insert_to_cart(chat_id):
    database = sqlite3.connect('shop.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO carts(user_id)
    VALUES ((SELECT user_id FROM users WHERE telegram_id = ?))
    ''', (chat_id,))
    database.commit()
    database.close()
    return True

def first_select_user(chat_id):
    database = sqlite3.connect('shop.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM users
    WHERE telegram_id = ?
    ''', (chat_id, ))
    user = cursor.fetchone()
    database.close()
    return user


def get_all_categories():
    database = sqlite3.connect('shop.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM categories
    ''',)
    categories = cursor.fetchall()
    database.close()
    return categories


def get_products_by_category_id(category_id):
    database = sqlite3.connect('shop.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT product_id, product_name
    FROM products WHERE category_id = ?
    ''', (category_id,))
    products = cursor.fetchall()
    database.close()
    return products


def get_product_detail(product_id):
    database = sqlite3.connect('shop.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM products 
    WHERE product_id = ?
    ''', (product_id,))
    products = cursor.fetchone()
    database.close()
    return products


def get_user_cart_id(chat_id):
    database = sqlite3.connect('shop.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT cart_id FROM carts
    WHERE user_id = (SELECT user_id FROM users WHERE telegram_id = ?)
    ''', (chat_id,))
    cart_id = cursor.fetchone()[0]
    database.close()
    return cart_id


def insert_or_update_cart_product(cart_id, product_name, quantity, final_price):
    database = sqlite3.connect('shop.db')
    cursor = database.cursor()
    try:
        cursor.execute('''
        INSERT INTO cart_products(cart_id, product_name, quantity, final_price)
        VALUES (?, ?, ?, ?)
        ''', (cart_id, product_name, quantity, final_price))
        database.commit()
        return True
    except:
        cursor.execute('''
        UPDATE cart_products
        SET quantity = ?,
        final_price = ?
        WHERE product_name = ? AND cart_id = ?
        ''', (quantity, final_price, product_name, cart_id))
        database.commit()
        return False
    finally:
        database.close()


def get_quantity(cart_id, product_name):
    database = sqlite3.connect('shop.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT quantity FROM cart_products
    WHERE cart_id = ? AND product_name = ?
    ''', (cart_id, product_name))
    quantity = cursor.fetchone()[0]
    database.close()
    return quantity
def update_total_product_total_price(cart_id):
    database = sqlite3.connect('shop.db')
    cursor = database.cursor()
    cursor.execute('''
        UPDATE carts
        SET total_products = (
        SELECT SUM(quantity) FROM cart_products
        WHERE cart_id = :cart_id
        ),
        total_price = (
        SELECT SUM(final_price) FROM cart_products
        WHERE cart_id = :cart_id
        )
        WHERE cart_id = :cart_id
        ''', {'cart_id': cart_id})
    database.commit()
    database.close()
    return True


def get_cart_products(cart_id):
    database = sqlite3.connect('shop.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT product_name, quantity, final_price
    FROM cart_products
    WHERE cart_id= ?
    ''',(cart_id,))
    info = cursor.fetchall()
    database.close()
    return info


def get_total_products_price(cart_id):
    database = sqlite3.connect('shop.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT total_products, total_price FROM carts WHERE cart_id = ?
    ''', (cart_id,))
    total_products, total_price = cursor.fetchone()
    database.close()
    return total_products, total_price


def get_cart_product_for_delete(cart_id):
    database = sqlite3.connect('shop.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT cart_product_id, product_name
    FROM cart_products
    WHERE cart_id = ?
    
    ''', (cart_id,))
    info = cursor.fetchall()
    database.close()
    return info

def delete_cart_products_from_db(cart_product_id):
    database = sqlite3.connect('shop.db')
    cursor = database.cursor()
    cursor.execute('''
    DELETE FROM cart_products
    WHERE cart_product_id = ?
    ''', (cart_product_id,))
    database.commit()
    database.close()
    return True


def create_orders_check():
    database = sqlite3.connect('shop.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders_check(
        order_check_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cart_id INTEGER REFERENCES carts(cart_id),
        total_price DECIMAL(9, 2) NOT NULL,
        total_products INTEGER DEFAULT 0,
        time_order TEXT,
        date_order TEXT
    )
    ''')
    database.commit()
    database.close()
# create_orders_check()
def create_table_orders():
    database = sqlite3.connect('shop.db')
    cursor = database.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders(
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_check_id INTEGER REFERENCES orders_check(order_check_id),
            product_name VARCHAR(100) NOT NULL,
            quantity INTEGER NOT NULL,
            final_price DECIMAL(9, 2) NOT NULL
        )
    ''', )
    database.commit()
    database.close()
    return True

# create_table_orders()
def save_order_check(cart_id, total_price, total_products, time_order, date_order):
    database = sqlite3.connect('shop.db')
    cursor = database.cursor()
    cursor.execute('''
        INSERT INTO orders_check(cart_id, total_price, total_products, time_order, date_order)
        VALUES (?,?,?,?,?)
    ''', (cart_id, total_price, total_products, time_order, date_order))
    database.commit()
    database.close()
    
def get_order_check_id(cart_id):
    database = sqlite3.connect('shop.db')
    cursor = database.cursor()
    cursor.execute('''
        SELECT order_check_id FROM orders_check
        WHERE cart_id = ?
    ''', (cart_id,))
    order_check_id = cursor.fetchone()[0]
    database.close()
    return order_check_id

def save_order(order_check_id, product_name, quantity, final_price):
    database = sqlite3.connect('shop.db')
    cursor = database.cursor()
    cursor.execute('''
        INSERT INTO orders(order_check_id, product_name, quantity, final_price)
        VALUES (?, ?, ?, ?)
    ''', (order_check_id, product_name, quantity, final_price,))
    database.commit()
    database.close()
    return True

def get_order_check(cart_id):
    database = sqlite3.connect('shop.db')
    cursor = database.cursor()
    cursor.execute('''
        SELECT * FROM orders_check
        WHERE cart_id = ?
            ''', (cart_id))
    order_check = cursor.fetchall()
    database.close()
    return order_check

def get_detail_order(order_check_id):
    database = sqlite3.connect('shop.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT product_name, quantity, final_prce FROM orders
    WHERE order_check_id = ?
        ''',(order_check_id))
    detail_order_info = cursor.fetchall()
    database.close()    
    return detail_order_info

def drop_cart_products_default(cart_id):
    database = sqlite3.connect('shop.db')
    cursor = database.cursor()
    cursor.execute('''
        DELETE FROM cart_products
        WHERE cart_id = ?
    ''', (cart_id,))
    database.commit()
    database.close()
    return True











