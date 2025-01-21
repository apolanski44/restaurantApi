const apiUrl = '/api/menu';

function fetchMenu(category = '') {
    const url = category ? `${apiUrl}?category=${category}` : apiUrl;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const menuList = document.getElementById('menu-items-list');
            menuList.innerHTML = '';

            if (data.menu_items.length === 0) {
                const row = document.createElement('tr');
                row.innerHTML = `<td colspan="4">No items found in this category.</td>`;
                menuList.appendChild(row);
                return;
            }

            data.menu_items.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${item.id}</td>
                    <td>${item.name}</td>
                    <td>${item.category}</td>
                    <td>${item.price}</td>
                `;
                menuList.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching menu items:', error));
}

document.getElementById('filter-menu-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const category = document.getElementById('category').value;
    fetchMenu(category);
});

fetchMenu();
