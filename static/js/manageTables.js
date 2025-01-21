const apiUrl = '/api/tables';

function fetchTables() {
    fetch(apiUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        }
    })
        .then(response => response.json())
        .then(data => {
            const tableList = document.getElementById('table-list');
            tableList.innerHTML = '';
            data.tables.forEach(table => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${table.id}</td>
                    <td>${table.seats}</td>
                    <td>
                        <button onclick="deleteTable(${table.id})" class="button">Delete</button>
                        <button onclick="showEditForm(${table.id}, ${table.seats})" class="button">Edit</button>
                    </td>
                `;
                tableList.appendChild(row);
            });
        })
        .catch(error => alert('Error fetching tables: ' + error));
}

document.getElementById('add-table-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const seats = document.getElementById('seats').value;

    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        },
        body: JSON.stringify({ seats: parseInt(seats) })
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                alert(data.message || 'Table added successfully!');
                fetchTables();
            }
        })
        .catch(error => alert('Error adding table: ' + error));
});

function deleteTable(tableId) {
    fetch(`${apiUrl}/${tableId}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                alert(data.message || 'Table deleted successfully!');
                fetchTables();
            }
        })
        .catch(error => alert('Error deleting table: ' + error));
}

function showEditForm(tableId, seats) {
    document.getElementById('edit-table-section').style.display = 'block';
    document.getElementById('edit-table-id').value = tableId;
    document.getElementById('edit-seats').value = seats;
}

document.getElementById('edit-table-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const tableId = document.getElementById('edit-table-id').value;
    const seats = document.getElementById('edit-seats').value;

    fetch(`${apiUrl}/${tableId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        },
        body: JSON.stringify({ seats: parseInt(seats) })
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                alert(data.message || 'Table updated successfully!');
                fetchTables();
                document.getElementById('edit-table-section').style.display = 'none';
            }
        })
        .catch(error => alert('Error updating table: ' + error));
});

fetchTables();
