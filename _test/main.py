import sqlite3

# create a connection object
conn = sqlite3.connect("mydb.db")

# create a cursor object
cur = conn.cursor()

# create a table called products
cur.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL, quantity INTEGER)")

# commit the changes
conn.commit()
# insert a product into the table
cur.execute("INSERT INTO products VALUES (1, 'Laptop', 500.0, 10)")

# commit the changes
conn.commit()
# insert multiple products into the table
products = [(2, 'Mouse', 10.0, 20), (3, 'Keyboard', 15.0, 15), (4, 'Monitor', 100.0, 5)]
cur.executemany("INSERT INTO products VALUES (?, ?, ?, ?)", products)

# commit the changes
conn.commit()
# create a table called bills
cur.execute("CREATE TABLE bills (id INTEGER PRIMARY KEY, date TEXT, total REAL, customer_id INTEGER)")

# commit the changes
conn.commit()
# insert a bill into the table
cur.execute("INSERT INTO bills VALUES (1, '2023-07-02', 550.0, 1)")

# commit the changes
conn.commit()
# query all products from the table
cur.execute("SELECT * FROM products")

# fetch all rows as a list of tuples
products = cur.fetchall()
print("product :##########################")
# print each product
for product in products:
    print(product)
(1, 'Laptop', 500.0, 10)
(2, 'Mouse', 10.0, 20)
(3, 'Keyboard', 15.0, 15)
(4, 'Monitor', 100.0, 5)
# query all bills from the table
cur.execute("SELECT * FROM bills")

# fetch all rows as a list of tuples
bills = cur.fetchall()
print("bill :##########################")

# print each bill
for bill in bills:
    print(bill)
(1, '2023-07-02', 550.0, 1)
# query all bills with customer names from both tables
cur.execute("SELECT b.id, b.date, b.total, p.name FROM bills b JOIN products p ON b.customer_id = p.id")

# fetch all rows as a list of tuples
bills = cur.fetchall()
print("bill :##########################")

# print each bill with customer name
for bill in bills:
    print(bill)
# close the connection
conn.close()
