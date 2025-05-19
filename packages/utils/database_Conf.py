import sqlite3
import pandas as pd
import csv


class Database:
    path = "./libs/"
    dbName = "store.db"

    def __init__(self):
        self.connection = sqlite3.connect(self.path + self.dbName)
        self.cursor = self.connection.cursor()

    def fetch_query(self, query):
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results

    def fetch_join(self, t1, t2):
        result = select_data(
            f"{t1}, {t2}",
            f"as {t2}_Name {t1} as t1 join {t2} as t2 WHERE t2.id = t1.{t2}_id",
            fetchall=True,
        )
        return result
        #############################################################################################################

    def get_data_from_csv(self, csv_file_name):
        with open(self.path + csv_file_name, "r") as csvfile:
            csvreader = csv.reader(csvfile, delimiter=",")
            data = []
            for row in csvreader:
                data.append(row)
        self.connection.commit()
        self.close_connection()
        return data

    def fetch_columns_names(self, table_name):
        query = "PRAGMA table_info({})".format(table_name)
        results = self.fetch_query(query)
        columns_names = []
        print(results)
        for row in results:
            if row[1] != "id":
                columns_names.append(row[1])
        self.connection.commit()

        return columns_names

    def create_table(self, table_name, columns):
        query = "CREATE TABLE IF NOT EXISTS {} ({})".format(table_name, columns)
        self.cursor.execute(query)

    def insert_fromCSV(self, table):
        table_csv = table + ".csv"
        data = self.get_data_from_csv(table_csv)
        for d in data:
            self.insert_data(table, d)

    def insert_data(self, table_name, data):
        query = (
            "INSERT INTO {} ({}) VALUES ({})".format(
                table_name, self.fetch_columns_names(table_name), data
            )
            .replace("[", "")
            .replace("]", "")
        )
        print(query, "--------> Running ")

        self.cursor.execute(query)
        self.connection.commit()
        self.close_connection()

    def select_data(self, table_name, where_clause=None, fetchall=True):
        query = f"SELECT * FROM {table_name} {where_clause}"
        if where_clause:
            query = query.format(where_clause)
        print(query, "--------> Running ")
        self.cursor.execute(query)
        if fetchall == False:
            results01 = self.cursor.fetchone()

        else:
            results01 = self.cursor.fetchall()
        self.connection.commit()
        self.close_connection()

        return results01

    def search_database(self, table_name, search_by, search_term):
        """SELECT * FROM {table_name} WHERE {search_by} LIKE {search_term}"""
        query = f"SELECT * FROM {table_name} WHERE {search_by} LIKE ?"

        self.cursor.execute(query, (f"%{search_term}%",))

        results = self.cursor.fetchall()

        for result in results:
            print(result[0])

    def update_data(self, table_name, values, where_clause=None):
        query = "UPDATE user SET "
        for column_name in self.fetch_columns_names(table_name):
            query += f"{column_name} = ?, "
        query = query[:-2]  # remove the trailing comma
        if where_clause:
            query += where_clause
        self.cursor.execute(query, values)
        self.connection.commit()
        self.close_connection()

    def delete_data(self, table_name, where_clause=None):
        query = "DELETE FROM {} {}".format(table_name, where_clause)
        self.cursor.execute(query)
        self.connection.commit()
        self.close_connection()

    def close_connection(self):
        self.connection.close()

    def db_SP(self):
        self.create_table(
            "category",
            "id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,description TEXT",
        )
        self.create_table(
            "user",
            "id INTEGER PRIMARY KEY AUTOINCREMENT,firstName TEXT NOT NULL,lastName TEXT NOT NULL,username TEXT UNIQUE NOT NULL, email TEXT,password TEXT NOT NULL,createdAt Date DEFAULT CURRENT_DATE,signedIn Date DEFAULT CURRENT_DATE, role TEXT NOT NULL",
        )
        self.create_table(
            "customer",
            "id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,email TEXT UNIQUE,address TEXT,phone TEXT",
        )
        self.create_table(
            "'order'",
            "id INTEGER PRIMARY KEY AUTOINCREMENT,date DATE ,amount REAL NOT NULL,status TEXT NOT NULL,customer_id INTEGER NOT NULL,FOREIGN KEY (customer_id) REFERENCES customer (id)",
        )
        self.create_table(
            "product",
            "id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,price REAL NOT NULL,description TEXT,category_id INTEGER,FOREIGN KEY (category_id) REFERENCES categories (id)",
        )
        self.create_table(
            "material",
            "id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,quantity INTEGER NOT NULL,cost REAL NOT NULL",
        )
        self.create_table(
            "shift",
            "id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,date DATE,start_time TIME,end_time TIME,FOREIGN KEY (user_id) REFERENCES users (id)",
        )
        self.create_table(
            "order_detail",
            "order_id INTEGER NOT NULL,product_id INTEGER NOT NULL,quantity INTEGER NOT NULL,price REAL NOT NULL,PRIMARY KEY (order_id, product_id),FOREIGN KEY (order_id) REFERENCES orders (id),FOREIGN KEY (product_id) REFERENCES products (id)",
        )
        """users = [
            
            {date
                1: "firstName",
                2: "lastName",
                3: "userName",
                3: "*******",
                4: "createdAt",######
                5:"signedIn",####### 
                6:"role",
                7: "Email"
            },    
            ]"""


"""main
    def main(self):
        
        # Create table
        database.create_table("users", "id INTEGER PRIMARY KEY, name TEXT, email TEXT, password TEXT")
        # Insert data
        database.insert_data("users", "'me', 'ename@example.com', 'pword1'")
        # Select data
        results = database.select_data("users")
        for row in results:
            print(row)
        # Update data
        database.update_data("users", "name='ename'", "id=1")
        # Delete data
        database.delete_data("users", "id=1")
        # Close connection
        database.close_connection()
        
        
    


        database = Database()
        database.db_SP()
        
        database.insert_fromCSV('users')
        results = database.select_data("users")
        for row in results:
            print(row)
        database.connection.commit()
        database.close_connection()
"""


if __name__ == "__main__":
    database = Database()
    # database.db_SP()
    database.insert_fromCSV("category")
    results = database.select_data("category")
    for row in results:
        print(row)
