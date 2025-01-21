const apiUrl = '/api/reservations';

document.getElementById('cancel-reservation-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const tableId = document.getElementById('table_id').value;
    const reservationDate = document.getElementById('reservation_date').value;
    const reservationTime = document.getElementById('reservation_time').value;
    const lastname = document.getElementById('lastname').value;

    fetch(`${apiUrl}/cancel_reservation`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            table_id: tableId,
            reservation_date: reservationDate,
            reservation_time: reservationTime,
            lastname: lastname
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showError(data.error);
            } else {
                alert(data.message || 'Reservation cancelled successfully!');
                document.getElementById('cancel-reservation-form').reset();
            }
        })
        .catch(error => showError('Error cancelling reservation: ' + error));
});

function showError(message) {
    alert(message)
}
