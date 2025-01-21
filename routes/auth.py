from flask import Blueprint, request, jsonify, render_template
from models.UserModel import UserModel
import bcrypt
import jwt
import datetime
from functools import wraps

auth_bp = Blueprint('auth', __name__)

SECRET_KEY = "your_secret_key"

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({"error": "Unauthorized. Token is missing."}), 401

        try:
            token = token.split()[1]
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Unauthorized. Token has expired."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Unauthorized. Invalid token."}), 401

        return f(*args, **kwargs)
    return decorated



@auth_bp.route("/adminlogin")
def adminlogin():
    return render_template('adminlogin.html')
@auth_bp.route('/api/adminlogin', methods=['POST'])
def admin_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    user = UserModel.find_by_username(username)

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        token = jwt.encode(
            {"user_id": user['id'], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            SECRET_KEY,
            algorithm="HS256"
        )
        return jsonify({"message": "Login successful.", "token": token}), 200
    else:
        return jsonify({"error": "Invalid username or password."}), 401


@auth_bp.route('/api/adminindex', methods=['GET'])

def adminindex():
    try:
        return jsonify({"message": f"Welcome to the admin index. User ID:"}), 200
    except Exception as e:
        print(f"Error in adminindex: {e}")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500


@auth_bp.route('/adminindex')
def admini_ndex():
    return render_template('adminindex.html')


@auth_bp.route('/userindex', methods=['GET'])
def userindex():
    return render_template('userindex.html')

@auth_bp.route('/api/logout', methods=['POST'])
def logout():
    return jsonify({"message": "Logout successful."}), 200
