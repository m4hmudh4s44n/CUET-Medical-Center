document.getElementById('login-form').addEventListener('submit', function(e) {
            e.preventDefault();
            // Simple demo: username: admin, password: admin
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value;
            if (username === "admin" && password === "admin") {
                window.location.href = "admin_panel.html";
            } else {
                document.getElementById('login-error').style.display = 'block';
            }
        });