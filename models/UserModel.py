from Database import db_connection
from functools import wraps
from flask import session, redirect, url_for, request, jsonify

class UserModel:
    @staticmethod
    def find_by_username(username):
        try:
            conn = db_connection()
            cursor = conn.cursor()
            query = "SELECT id, username, password FROM Users WHERE username = ?"
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            conn.close()
            if user:
                return {"id": user[0], "username": user[1], "password": user[2]}
            return None
        except Exception as e:
            print(f"Database error: {e}")
            return None
