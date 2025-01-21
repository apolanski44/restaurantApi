const apiUrl = '/api/reservations';

document.getElementById('search-reservations-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const reservationDate = document.getElementById('reservation_date').value;
    if (!reservationDate) {
        showError('Please select a reservation date.');
        return;
    }

    fetch(`${apiUrl}/manage?reservation_date=${reservationDate}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showError(data.error);
                return;
            }
            populateReservations(data.reservations || []);
        })
        .catch(error => showError('Error fetching reservations: ' + error));
});

function populateReservations(reservations) {
    const reservationsList = document.getElementById('reservations-list');
    reservationsList.innerHTML = '';

    if (reservations.length === 0) {
        showError('No reservations found for the selected date.');
        return;
    }

    reservations.forEach(reservation => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${reservation.id}</td>
            <td>${reservation.table_id}</td>
            <td>${reservation.reservation_time}</td>
            <td>${reservation.guests}</td>
            <td>${reservation.lastname}</td>
            <td>
                <button class="button" onclick="deleteReservation(${reservation.id})">Delete</button>
            </td>
        `;
        reservationsList.appendChild(row);
    });
}

function deleteReservation(reservationId) {
    if (!confirm('Are you sure you want to delete this reservation?')) return;

    fetch(`${apiUrl}/${reservationId}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showError(data.error);
                return;
            }
            alert(data.message || 'Reservation deleted successfully!');
            document.getElementById('search-reservations-form').dispatchEvent(new Event('submit'));
        })
        .catch(error => showError('Error deleting reservation: ' + error));
}

function showError(message) {
    alert(message);
}
