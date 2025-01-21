from Database import db_connection

class ReservationModel:
    @staticmethod
    def create_reservation(table_id, reservation_time, guests, lastname):
        conn = db_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO Reservations (TableID, ReservationTime, Guests, ClientLastName)
        VALUES (?, ?, ?, ?)
        """
        cursor.execute(query, (table_id, reservation_time, guests, lastname))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_reservations():
        conn = db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM Reservations"
        cursor.execute(query)
        reservations = cursor.fetchall()
        conn.close()
        return [
            {
                "id": row[0],
                "table_id": row[1],
                "reservation_time": row[2],
                "guests": row[3],
                "lastname": row[4]
            }
            for row in reservations
        ]

    @staticmethod
    def get_reservation_by_id(reservation_id):
        conn = db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM Reservations WHERE ID = ?"
        cursor.execute(query, (reservation_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {
                "id": row[0],
                "table_id": row[1],
                "reservation_time": row[2],
                "guests": row[3],
                "lastname": row[4]
            }
        return None

    @staticmethod
    def update_reservation(reservation_id, table_id, reservation_time, guests, lastname):
        conn = db_connection()
        cursor = conn.cursor()
        query = """
        UPDATE Reservations
        SET TableID = ?, ReservationTime = ?, Guests = ?, ClientLastName = ?
        WHERE ID = ?
        """
        cursor.execute(query, (table_id, reservation_time, guests, lastname, reservation_id))
        conn.commit()
        conn.close()

    @staticmethod
    def cancel_reservation(table_id, reservation_datetime, lastname):
        conn = db_connection()
        cursor = conn.cursor()
        query = """
        DELETE FROM Reservations
        WHERE TableID = ? AND ReservationTime = ? AND ClientLastName = ?
        """
        cursor.execute(query, (table_id, reservation_datetime, lastname))
        conn.commit()
        rows_deleted = cursor.rowcount
        conn.close()
        return rows_deleted > 0

    @staticmethod
    def get_available_tables(reservation_datetime, exact_seats=None):
        conn = db_connection()
        cursor = conn.cursor()
        query = """
        SELECT T.ID, T.Seats
        FROM Tables T
        WHERE T.ID NOT IN (
            SELECT R.TableID
            FROM Reservations R
            WHERE R.ReservationTime = ?
        )
        """
        params = [reservation_datetime]

        if exact_seats:
            query += " AND T.Seats = ?"
            params.append(int(exact_seats))

        cursor.execute(query, params)
        tables = cursor.fetchall()
        conn.close()
        return [{"id": row[0], "seats": row[1]} for row in tables]

    @staticmethod
    def get_suitable_table(reservation_datetime, guests):
        conn = db_connection()
        cursor = conn.cursor()
        query = """
        SELECT T.ID, T.Seats
        FROM Tables T
        WHERE T.Seats >= ? AND T.ID NOT IN (
            SELECT R.TableID
            FROM Reservations R
            WHERE R.ReservationTime = ?
        )
        ORDER BY T.Seats ASC
        """
        cursor.execute(query, (guests, reservation_datetime))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"id": row[0], "seats": row[1]}
        return None

    @staticmethod
    def is_table_available(table_id, reservation_datetime):
        conn = db_connection()
        cursor = conn.cursor()
        query = """
        SELECT 1
        FROM Reservations
        WHERE TableID = ? AND ReservationTime = ?
        """
        cursor.execute(query, (table_id, reservation_datetime))
        result = cursor.fetchone()
        conn.close()
        return result is None
    @staticmethod
    def is_reservation_existing(table_id, reservation_datetime, lastname):
        conn = db_connection()
        cursor = conn.cursor()
        query = """
        SELECT 1 FROM Reservations
        WHERE TableID = ? AND ReservationTime = ? AND ClientLastName = ?
        """
        cursor.execute(query, (table_id, reservation_datetime, lastname))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    @staticmethod
    def get_reservations_by_date(reservation_date):
        conn = db_connection()
        cursor = conn.cursor()
        query = """
        SELECT ID, TableID, ReservationTime, Guests, ClientLastName
        FROM Reservations
        WHERE CAST(ReservationTime AS DATE) = ?
        """
        cursor.execute(query, (reservation_date,))
        reservations = cursor.fetchall()
        conn.close()

        return [
            {
                "id": row[0],
                "table_id": row[1],
                "reservation_time": row[2],
                "guests": row[3],
                "lastname": row[4]
            }
            for row in reservations
        ]

    @staticmethod
    def delete_reservation_by_id(reservation_id):
        conn = db_connection()
        cursor = conn.cursor()
        query = "DELETE FROM Reservations WHERE ID = ?"
        cursor.execute(query, (reservation_id,))
        conn.commit()
        conn.close()
