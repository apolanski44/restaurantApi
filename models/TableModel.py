from Database import db_connection

class TableModel:
    @staticmethod
    def add_table(seats):
        conn = db_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO Tables (Seats)
        VALUES (?)
        """
        cursor.execute(query, (seats,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_tables():
        conn = db_connection()
        cursor = conn.cursor()
        query = "SELECT ID, Seats FROM Tables"
        cursor.execute(query)
        tables = cursor.fetchall()
        conn.close()
        return [{"id": row[0], "seats": row[1]} for row in tables]

    @staticmethod
    def update_table(table_id, seats):
        conn = db_connection()
        cursor = conn.cursor()
        query = """
        UPDATE Tables
        SET Seats = ?
        WHERE ID = ?
        """
        cursor.execute(query, (seats, table_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_table(table_id):
        conn = db_connection()
        cursor = conn.cursor()
        query_check_reservations = "SELECT COUNT(*) FROM Reservations WHERE TableID = ?"
        cursor.execute(query_check_reservations, (table_id,))
        reservation_count = cursor.fetchone()[0]

        if reservation_count > 0:
            raise Exception("Cannot delete table because there are existing reservations.")
        query_delete_table = "DELETE FROM Tables WHERE ID = ?"
        cursor.execute(query_delete_table, (table_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_table_by_id(table_id):
        conn = db_connection()
        cursor = conn.cursor()
        query = "SELECT ID, Seats FROM Tables WHERE ID = ?"
        cursor.execute(query, (table_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"id": row[0], "seats": row[1]}
        return None

    @staticmethod
    def is_table_existing(table_id):
        conn = db_connection()
        cursor = conn.cursor()
        query = "SELECT 1 FROM Tables WHERE ID = ?"
        cursor.execute(query, (table_id,))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    @staticmethod
    def get_reservations_for_table(table_id):
        conn = db_connection()
        cursor = conn.cursor()

        query = """
        SELECT R.ID, R.ReservationTime, R.Guests, R.ClientLastName
        FROM Reservations R
        WHERE R.TableID = ?
        ORDER BY R.ReservationTime ASC
        """
        cursor.execute(query, (table_id,))
        reservations = cursor.fetchall()
        conn.close()

        return [
            {
                "id": row[0],
                "reservation_time": row[1],
                "guests": row[2],
                "client_last_name": row[3],
            }
            for row in reservations
        ]
