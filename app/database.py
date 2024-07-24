import sqlite3

def create_tables():
    try:
        conn = sqlite3.connect('app/pos.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                total REAL NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        conn.commit()
        print("Tables created or already exist.")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        conn.close()

def add_product(name, price):
    try:
        conn = sqlite3.connect('app/pos.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO products (name, price) VALUES (?, ?)', (name, price))
        conn.commit()
        print(f"Product added: {name}, ${price}")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        conn.close()

def get_products():
    try:
        conn = sqlite3.connect('app/pos.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products')
        products = cursor.fetchall()
        conn.close()
        print("Products:", products)
        return products
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return []

def add_sale(product_id, quantity, total):
    try:
        print(f"Adding sale: Product ID {product_id}, Quantity {quantity}, Total ${total}")  # Debug line
        conn = sqlite3.connect('app/pos.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO sales (product_id, quantity, total) VALUES (?, ?, ?)', (product_id, quantity, total))
        conn.commit()
        print(f"Sale added: Product ID {product_id}, Quantity {quantity}, Total ${total}")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        conn.close()


def get_sales():
    try:
        conn = sqlite3.connect('app/pos.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT sales.id, products.name, sales.quantity, sales.total
            FROM sales
            JOIN products ON sales.product_id = products.id
        ''')
        sales = cursor.fetchall()
        conn.close()
        return sales
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return []
    
# Create tables if not exist
create_tables()
