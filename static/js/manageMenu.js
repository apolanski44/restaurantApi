const apiUrl = '/api/menu';

function fetchMenu(category = '') {
    const url = category ? `${apiUrl}?category=${category}` : apiUrl;

    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        }
    })
        .then(response => response.json())
        .then(data => {
            const menuList = document.getElementById('menu-items-list');
            menuList.innerHTML = '';
            data.menu_items.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${item.id}</td>
                    <td>${item.name}</td>
                    <td>${item.category}</td>
                    <td>${item.price}</td>
                    <td>
                        <button onclick="deleteMenuItem(${item.id})" class="button">Delete</button>
                        <button onclick="editMenuItem(${item.id}, '${item.name}', '${item.category}', ${item.price})" class="button">Edit</button>
                    </td>
                `;
                menuList.appendChild(row);
            });
        })
        .catch(error => alert('Error fetching menu items: ' + error));
}

document.getElementById('add-item-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const name = document.getElementById('name').value;
    const category = document.getElementById('add-category').value;
    const price = document.getElementById('price').value;

    fetch('/api/menu', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        },
        body: JSON.stringify({ name, category, price: parseFloat(price) })
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                alert(data.message || 'Item added successfully!');
                fetchMenu();
            }
        })
        .catch(error => alert('Error adding menu item: ' + error));
});


function deleteMenuItem(itemId) {
    fetch(`${apiUrl}/${itemId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                alert(data.message || 'Item deleted successfully!');
                fetchMenu();
            }
        })
        .catch(error => alert('Error deleting menu item: ' + error));
}

function editMenuItem(itemId) {
    window.location.href = `/editMenuItem/${itemId}`;
}

document.getElementById('filter-menu-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const category = document.getElementById('category').value;
    fetchMenu(category);
});

fetchMenu();
