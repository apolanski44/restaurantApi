from flask import Blueprint, request, jsonify, render_template, redirect
from models.MenuModel import MenuModel
from functools import wraps
from routes.auth import require_api_key

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/api/menu', methods=['GET'])
def get_menu():
    try:
        category = request.args.get('category')
        if category:
            items = MenuModel.get_items_by_category(category)
        else:
            items = MenuModel.get_all_items()
        return jsonify({"menu_items": items}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@menu_bp.route('/api/menu', methods=['POST'])
@require_api_key
def add_menu_item():
    try:
        data = request.json
        name = data.get('name')
        category = data.get('category')
        price = data.get('price')

        if not name or not category:
            return jsonify({"error": "Name and category are required."}), 400
        if price is None or price <= 0:
            return jsonify({"error": "Price must be a positive number."}), 400

        MenuModel.add_item(name, category, price)
        return jsonify({"message": "Menu item added successfully."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@menu_bp.route('/api/menu/<int:item_id>', methods=['GET'])
def get_menu_item(item_id):
    try:
        item = MenuModel.get_item_by_id(item_id)
        if not item:
            return jsonify({"error": "Menu item not found."}), 404
        return jsonify({"menu_item": item}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@menu_bp.route('/api/menu/<int:item_id>', methods=['PUT'])
@require_api_key
def edit_menu_item(item_id):
    try:
        data = request.json
        name = data.get('name')
        category = data.get('category')
        price = data.get('price')

        if not name or not category:
            return jsonify({"error": "Name and category are required."}), 400
        if price is None or price <= 0:
            return jsonify({"error": "Price must be a positive number."}), 400

        MenuModel.update_item(item_id, name, category, price)
        return jsonify({"message": "Menu item updated successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@menu_bp.route('/api/menu/<int:item_id>', methods=['DELETE'])
@require_api_key
def delete_menu_item(item_id):
    try:
        if not MenuModel.get_item_by_id(item_id):
            return jsonify({"error": "Menu item not found."}), 404

        MenuModel.delete_item(item_id)
        return jsonify({"message": "Menu item deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@menu_bp.route('/api/menu/<int:item_id>', methods=['POST'])
@require_api_key
def update_menu_item(item_id):
    try:
        data = request.form
        name = data.get('name')
        category = data.get('category')
        price = data.get('price')

        if not name or not category:
            return jsonify({"error": "Name and category are required."}), 400
        if price is None or float(price) <= 0:
            return jsonify({"error": "Price must be a positive number."}), 400

        MenuModel.update_item(item_id, name, category, float(price))
        return redirect('/manageMenu')
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@menu_bp.route("/menuindex")
def menuindex():
    return render_template('menuindex.html')

@menu_bp.route("/manageMenu")

def manageMenu():
    return render_template('manageMenu.html')

@menu_bp.route('/editMenuItem/<int:item_id>', methods=['GET'])
def render_edit_menu_item(item_id):
    try:
        item = MenuModel.get_item_by_id(item_id)
        if not item:
            return render_template('404.html'), 404
        return render_template('editMenuItem.html', item=item)
    except Exception as e:
        return render_template('error.html', error=str(e)), 500
