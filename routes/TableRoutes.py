from flask import Blueprint, request, jsonify, render_template
from models.TableModel import TableModel
from functools import wraps
from routes.auth import require_api_key

tables_bp = Blueprint('tables', __name__)

@tables_bp.route('/api/tables', methods=['POST'])
@require_api_key
def add_table():
    try:
        seats = request.json.get('seats')
        if not seats or seats <= 0:
            return jsonify({"error": "Seats must be a positive integer."}), 400

        TableModel.add_table(seats)
        return jsonify({"message": "Table added successfully."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@tables_bp.route('/api/tables', methods=['GET'])
def get_tables():
    try:
        tables = TableModel.get_all_tables()
        if not tables:
            return jsonify({"message": "No tables found."}), 200
        return jsonify({"tables": tables}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@tables_bp.route('/api/tables/<int:table_id>', methods=['GET'])
def get_table_by_id(table_id):
    try:
        table = TableModel.get_table_by_id(table_id)
        if not table:
            return jsonify({"error": "Table not found."}), 404

        reservations = TableModel.get_reservations_for_table(table_id)
        return jsonify({"table": table, "reservations": reservations}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@tables_bp.route('/api/tables/<int:table_id>', methods=['PUT'])
@require_api_key
def update_table(table_id):
    try:
        seats = request.json.get('seats')
        if not seats or seats <= 0:
            return jsonify({"error": "Seats must be a positive integer."}), 400

        TableModel.update_table(table_id, seats)
        return jsonify({"message": "Table updated successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@tables_bp.route('/api/tables/<int:table_id>', methods=['DELETE'])
@require_api_key
def delete_table(table_id):
    try:
        if not TableModel.is_table_existing(table_id):
            return jsonify({"error": "Table not found."}), 404

        TableModel.delete_table(table_id)
        return jsonify({"message": "Table deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@tables_bp.route('/api/tables/occupied', methods=['POST'])
def get_occupied_tables():
    try:
        data = request.json
        reservation_date = data.get('reservation_date')
        reservation_time = data.get('reservation_time')

        if not reservation_date or not reservation_time:
            return jsonify({"error": "Both reservation_date and reservation_time are required."}), 400

        occupied_tables = TableModel.get_tables_occupied_on_date(reservation_date, reservation_time)
        if not occupied_tables:
            return jsonify({"message": "No occupied tables for the selected date and time."}), 200
        return jsonify({"occupied_tables": occupied_tables}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@tables_bp.route('/manageTables', methods=['GET'])
def manage_tables():
    try:
        tables = TableModel.get_all_tables()
        return render_template('manageTables.html', tables=tables, selected_table=None, occupied_times=None)
    except Exception as e:
        return render_template('manageTables.html', error=str(e), tables=[], selected_table=None, occupied_times=None)
