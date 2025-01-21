from flask import Blueprint, request, jsonify, render_template
from models.ReservationModel import ReservationModel
from models.TableModel import  TableModel
from datetime import datetime
from routes.auth import require_api_key
import re

reservations_bp = Blueprint('reservations', __name__)

def validate_manual_reservation_data(data):
    errors = []

    table_id = data.get('table_id')
    reservation_date = data.get('reservation_date')
    reservation_time = data.get('reservation_time')
    lastname = data.get('lastname')

    if not table_id or not str(table_id).isdigit() or int(table_id) <= 0:
        errors.append("Table ID must be a positive integer.")
    elif not TableModel.is_table_existing(int(table_id)):
        errors.append(f"Table ID {table_id} does not exist.")

    if not reservation_date or not reservation_time:
        errors.append("Reservation date and time are required.")
    else:
        try:
            datetime.strptime(f"{reservation_date} {reservation_time}", "%Y-%m-%d %H:%M")
        except ValueError:
            errors.append("Invalid date or time format. Use 'YYYY-MM-DD' and 'HH:MM'.")

    if not lastname or not re.match("^[A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ-]{1,50}$", lastname):
        errors.append("Last name must only contain letters and cannot include numbers or special characters.")

    return errors

def validate_auto_reservation_data(data):
    errors = []

    reservation_date = data.get('reservation_date')
    reservation_time = data.get('reservation_time')
    guests = data.get('guests')
    lastname = data.get('lastname')

    if not reservation_date or not reservation_time:
        errors.append("Reservation date and time are required.")
    else:
        try:
            datetime.strptime(f"{reservation_date} {reservation_time}", "%Y-%m-%d %H:%M")
        except ValueError:
            errors.append("Invalid date or time format. Use 'YYYY-MM-DD' and 'HH:MM'.")

    if not guests or not str(guests).isdigit() or int(guests) <= 0:
        errors.append("Number of guests must be a positive integer.")

    if not lastname or not re.match("^[A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ-]{1,50}$", lastname):
        errors.append("Last name must only contain letters and cannot include numbers or special characters.")

    return errors

@reservations_bp.route('/api/reservations/check_availability', methods=['POST'])
def check_availability():
    try:
        data = request.json
        reservation_date = data.get('reservation_date')
        reservation_time = data.get('reservation_time')

        if not reservation_date or not reservation_time:
            return jsonify({"error": "Please select both date and time."}), 400

        reservation_datetime = f"{reservation_date} {reservation_time}:00"

        available_tables = ReservationModel.get_available_tables(reservation_datetime)

        if not available_tables:
            return jsonify({"available_tables": []}), 200

        return jsonify({"available_tables": available_tables}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@reservations_bp.route('/api/reservations/auto_reserve', methods=['POST'])
def auto_reserve():
    try:
        data = request.json
        errors = validate_auto_reservation_data(data)

        if errors:
            return jsonify({"error": "; ".join(errors)}), 400

        reservation_date = data.get('reservation_date')
        reservation_time = data.get('reservation_time')
        guests = int(data.get('guests'))
        lastname = data.get('lastname')

        reservation_datetime = f"{reservation_date} {reservation_time}:00"
        table = ReservationModel.get_suitable_table(reservation_datetime, guests)
        if not table:
            return jsonify({"error": "No suitable tables available for the selected time and date."}), 404

        ReservationModel.create_reservation(table['id'], reservation_datetime, guests, lastname)
        return jsonify({
            "message": "Table reserved successfully.",
            "reservation_details": {
                "table_id": table['id'],
                "reservation_datetime": reservation_datetime,
                "guests": guests,
                "lastname": lastname
            }
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@reservations_bp.route('/api/reservations/manual_reserve', methods=['POST'])
def manual_reserve():
    try:
        data = request.json
        errors = validate_manual_reservation_data(data)

        if errors:
            return jsonify({"error": "; ".join(errors)}), 400

        reservation_date = data.get('reservation_date')
        reservation_time = data.get('reservation_time')
        table_id = int(data.get('table_id'))
        lastname = data.get('lastname')

        reservation_datetime = f"{reservation_date} {reservation_time}:00"

        if not ReservationModel.is_table_available(table_id, reservation_datetime):
            return jsonify({"error": f"Table {table_id} is not available at the selected time."}), 404

        ReservationModel.create_reservation(table_id, reservation_datetime, 1, lastname)
        return jsonify({
            "message": "Reservation confirmed.",
            "reservation_details": {
                "table_id": table_id,
                "reservation_datetime": reservation_datetime,
                "lastname": lastname
            }
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@reservations_bp.route('/userReservation')
def userReservation():
    return render_template('userReservation.html')

@reservations_bp.route('/cancelreservation')
def cancelReservation():
    return render_template('cancelReservation.html')

@reservations_bp.route('/api/reservations/cancel_reservation', methods=['POST'])
def cancel_reservation():
    try:
        data = request.json
        errors = validate_cancel_reservation(data)
        if errors:
            return jsonify({"error": "; ".join(errors)}), 400

        table_id = int(data['table_id'])
        reservation_date = data['reservation_date']
        reservation_time = data['reservation_time']
        lastname = data['lastname']

        reservation_datetime = f"{reservation_date} {reservation_time}:00"

        if not ReservationModel.is_reservation_existing(table_id, reservation_datetime, lastname):
            return jsonify({"error": "Reservation does not exist."}), 404

        success = ReservationModel.cancel_reservation(table_id, reservation_datetime, lastname)
        if success:
            return jsonify({"message": "Reservation cancelled successfully."}), 200
        else:
            return jsonify({"error": "Failed to cancel reservation."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@reservations_bp.route('/api/reservations/by_date', methods=['GET'])
def get_reservations_by_date():
    try:
        reservation_date = request.args.get('reservation_date')
        if not reservation_date:
            return jsonify({"error": "Reservation date is required."}), 400

        reservations = ReservationModel.get_reservations_by_date(reservation_date)
        if not reservations:
            return jsonify({"message": "No reservations found for the selected date."}), 404
        return jsonify({"reservations": reservations}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def validate_cancel_reservation(data):
    errors = []

    table_id = data.get('table_id')
    reservation_date = data.get('reservation_date')
    reservation_time = data.get('reservation_time')
    lastname = data.get('lastname')

    if not table_id or not str(table_id).isdigit() or int(table_id) <= 0:
        errors.append("Table ID must be a positive integer.")
    if not reservation_date or not reservation_time:
        errors.append("Reservation date and time are required.")
    else:
        try:
            datetime.strptime(f"{reservation_date} {reservation_time}", "%Y-%m-%d %H:%M")
        except ValueError:
            errors.append("Invalid date or time format. Use 'YYYY-MM-DD' and 'HH:MM'.")

    if not lastname or not re.match("^[A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ-]{1,50}$", lastname):
        errors.append("Last name must only contain letters and cannot include numbers or special characters.")

    return errors


@reservations_bp.route('/manageReservation')

def manageReservation():
    return render_template('manageReservation.html')

@reservations_bp.route('/api/reservations/<int:reservation_id>', methods=['DELETE'])
@require_api_key
def delete_reservation(reservation_id):
    try:
        if not ReservationModel.get_reservation_by_id(reservation_id):
            return jsonify({"error": "Reservation not found."}), 404
        ReservationModel.delete_reservation_by_id(reservation_id)
        return jsonify({"message": "Reservation deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@reservations_bp.route('/api/reservations/manage', methods=['GET'])
@require_api_key
def manage_reservations():
    try:
        reservation_date = request.args.get('reservation_date')
        if not reservation_date:
            return jsonify({"error": "Reservation date is required."}), 400

        reservations = ReservationModel.get_reservations_by_date(reservation_date)
        if not reservations:
            return jsonify({"message": "No reservations found for the selected date."}), 404
        return jsonify({"reservations": reservations}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
