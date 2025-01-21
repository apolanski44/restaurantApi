from Database import db_connection

class MenuModel:
    @staticmethod
    def get_all_items():
        try:
            conn = db_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM Menu"
            cursor.execute(query)
            items = cursor.fetchall()
            return [{"id": row[0], "name": row[1], "category": row[2], "price": row[3]} for row in items]
        finally:
            conn.close()

    @staticmethod
    def get_items_by_category(category):
        try:
            conn = db_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM Menu WHERE Category = ?"
            cursor.execute(query, (category,))
            items = cursor.fetchall()
            return [{"id": row[0], "name": row[1], "category": row[2], "price": row[3]} for row in items]
        finally:
            conn.close()

    @staticmethod
    def get_item_by_id(item_id):
        try:
            conn = db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Menu WHERE ID = ?", (item_id,))
            row = cursor.fetchone()
            if row:
                return {"id": row[0], "name": row[1], "category": row[2], "price": row[3]}
            return None
        finally:
            conn.close()

    @staticmethod
    def add_item(name, category, price):
        if price <= 0:
            raise ValueError("Price must be a positive number.")
        try:
            conn = db_connection()
            cursor = conn.cursor()
            query = """
            INSERT INTO Menu (Name, Category, Price)
            VALUES (?, ?, ?)
            """
            cursor.execute(query, (name, category, price))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def update_item(item_id, name, category, price):
        if price <= 0:
            raise ValueError("Price must be a positive number.")
        try:
            conn = db_connection()
            cursor = conn.cursor()
            existing_item = MenuModel.get_item_by_id(item_id)
            if not existing_item:
                raise ValueError(f"Item with ID {item_id} does not exist.")
            cursor.execute("UPDATE Menu SET Name = ?, Category = ?, Price = ? WHERE ID = ?",
                           (name, category, price, item_id))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def delete_item(item_id):
        try:
            conn = db_connection()
            cursor = conn.cursor()
            existing_item = MenuModel.get_item_by_id(item_id)
            if not existing_item:
                raise ValueError(f"Item with ID {item_id} does not exist.")

            cursor.execute("DELETE FROM Menu WHERE ID = ?", (item_id,))
            conn.commit()
        finally:
            conn.close()
