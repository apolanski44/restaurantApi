const apiUrl = '/api/reservations';

document.getElementById('check-availability-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const reservationDate = document.getElementById('reservation_date').value;
    const reservationTime = document.getElementById('reservation_time').value;

    fetch(`${apiUrl}/check_availability`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ reservation_date: reservationDate, reservation_time: reservationTime })
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showError(data.error);
                return;
            }
            populateAvailableTables(data.available_tables || []);
        })
        .catch(error => showError('Error checking availability: ' + error));
});

function populateAvailableTables(tables) {
    const tablesList = document.getElementById('available-tables-list');
    const tablesSection = document.getElementById('available-tables-section');
    tablesList.innerHTML = '';

    if (!tables || tables.length === 0) {
        showError('No tables available for the selected date and time.');
        tablesSection.style.display = 'none';
        return;
    }

    tables.forEach(table => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${table.id}</td>
            <td>${table.seats}</td>
        `;
        tablesList.appendChild(row);
    });

    tablesSection.style.display = 'block';
}


document.getElementById('auto-reserve-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const lastname = document.getElementById('lastname').value;
    const guests = document.getElementById('guests').value;
    const reservationDate = document.getElementById('reservation_date').value;
    const reservationTime = document.getElementById('reservation_time').value;

    fetch(`${apiUrl}/auto_reserve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ lastname, guests, reservation_date: reservationDate, reservation_time: reservationTime })
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showError(data.error);
                return;
            }
            alert('Reservation confirmed!');
            location.reload();
        })
        .catch(error => showError('Error reserving table: ' + error));
});

document.getElementById('manual-reserve-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const lastname = document.getElementById('lastname-manual').value;
    const tableId = document.getElementById('table_id').value;
    const reservationDate = document.getElementById('reservation_date').value;
    const reservationTime = document.getElementById('reservation_time').value;

    fetch(`${apiUrl}/manual_reserve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ lastname, table_id: tableId, reservation_date: reservationDate, reservation_time: reservationTime })
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showError(data.error);
                return;
            }
            alert('Reservation confirmed!');
            location.reload();
        })
        .catch(error => showError('Error reserving table: ' + error));
});

function showError(message) {

    alert(message)
}
