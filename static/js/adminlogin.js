document.getElementById('admin-login-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('/api/adminlogin', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {

                localStorage.setItem('authToken', data.token);

                window.location.href = '/adminindex';
            }
        })
        .catch(error => {
            alert('An error occurred while logging in.');
            console.error(error);
        });
});


function showError(message) {
    alert(message)
}
