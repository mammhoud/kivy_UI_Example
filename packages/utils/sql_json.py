import json
import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect("mydatabase.db")

# Create a cursor
cursor = conn.cursor()

# Create the tables
cursor.execute(
    "CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, address TEXT, phone TEXT, email TEXT, dateOfBirth TEXT, gender TEXT, notes TEXT)"
)
cursor.execute(
    "CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, description TEXT, price REAL, quantityInStock INTEGER, category TEXT, brand TEXT, image TEXT)"
)
cursor.execute(
    "CREATE TABLE orders (id INTEGER PRIMARY KEY, customerId INTEGER, date TEXT, time TEXT, status TEXT, paymentMethod TEXT, total REAL, shippingAddress TEXT, items TEXT)"
)
cursor.execute(
    "CREATE TABLE payments (id INTEGER PRIMARY KEY, orderId INTEGER, customerId INTEGER, date TEXT, time TEXT, amount REAL, type TEXT)"
)

# Load the data from the JSON file
with open("data.json", "r") as f:
    data = json.load(f)

# Insert the data into the tables
for customer in data["customers"]:
    cursor.execute(
        "INSERT INTO customers (name, address, phone, email, dateOfBirth, gender, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
        customer.values(),
    )

for product in data["products"]:
    cursor.execute(
        "INSERT INTO products (name, description, price, quantityInStock, category, brand, image) VALUES (?, ?, ?, ?, ?, ?, ?)",
        product.values(),
    )

for order in data["orders"]:
    cursor.execute(
        "INSERT INTO orders (customerId, date, time, status, paymentMethod, total, shippingAddress, items) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        order.values(),
    )

for payment in data["payments"]:
    cursor.execute(
        "INSERT INTO payments (orderId, customerId, date, time, amount, type) VALUES (?, ?, ?, ?, ?, ?)",
        payment.values(),
    )

# Commit the changes
conn.commit()

# Close the connection
conn.close()


##########################################
import json

data = {
    "name": "John Doe",
    "age": 30,
    "hobbies": ["coding", "reading", "hiking"],
}

json_data = json.dumps(data)

print(json_data)
