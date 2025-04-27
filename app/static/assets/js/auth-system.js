$(document).ready(function() {

        // // Send the AJAX request
        // $.ajax({
        //     type: 'POST',
        //     url: '/login',
        //     data: formData,
        //     success: function(response) {
        //         // Handle success (e.g., redirect to dashboard)
        //         window.location.href = '/dashboard';
        //     },
        //     error: function(xhr, status, error) {
        //         // Handle error (e.g., show error message)
        //         alert('Login failed: ' + xhr.responseText);
        //     }
        // });

        $(document).on('submit', '#login-form', function(event) {
            event.preventDefault();
            
            if (!$('#username').val() || !$('#password').val()) {
                showAlert("Por favor, completa todos los campos.");
                return;
            }

            if(!$('#username').val().match(/^[a-zA-Z0-9]+$/)) {
                showAlert("El nombre de usuario solo puede contener letras y números.");
                return;
            }

            if (!$('#password').val().match(/^[a-zA-Z0-9]+$/)) {
                showAlert("La contraseña solo puede contener letras y números.");
                return;
            }

            var formData = {
                username: $('#username').val(),
                password: $('#password').val()
            }
    
            if (formData) {
                console.log(formData);
                login(formData);
            }
        });
    
        $(document).on('submit', '#register-form', function(event) {
            event.preventDefault();

            var formData = {
                username: $('#username').val(),
                email: $('#email').val(),
                password: $('#password').val(),
                confirm_password: $('#confirm_password').val()
                
            }

            for (var key in formData) {
                var value = formData[key];
                if (!value) {
                    showAlert("Por favor, completa todos los campos.");
                    return;
                }
            }

            if (!formData.username.match(/^[a-zA-Z0-9]+$/)) {
                showAlert("El nombre de usuario solo puede contener letras y números.");
                return;
            }

            if (!formData.password.match(/^[a-zA-Z0-9]+$/) || !formData.confirm_password.match(/^[a-zA-Z0-9]+$/)) {
                showAlert("La contraseña solo puede contener letras y números.");
                return;
            }
            
            if (formData.password !== formData.confirm_password) {
                showAlert("Las contraseñas no coinciden.");
                return;
            }

            if (!formData.email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
                showAlert("Por favor, introduce un correo electrónico válido.");
                return;
            }

            if (formData) {
                console.log("Registro!");
                console.log(formData);
                registerUser(formData);
            }
        });

        $(document).on('click', '#logout', function(event) {
            event.preventDefault();
            logout();
        });
});

// Manejar el inicio de sesión
async function login(formData) {
    try {
        const response = await fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();

        if (response.ok) {
            localStorage.setItem("token", result.token);

            if (isTokenExpired(result.token)) {
                showAlert("El token ha expirado. Por favor, inicia sesión nuevamente.");
                logout();
                return;
            }

            showDashboard();
        } else {
            showAlert(result.message || "Error en el inicio de sesión.");
        }
    } catch (error) {
        console.error("Error:", error);
        showAlert("Error al conectar con el servidor.");
    }
}

// Manejar el registro de usuario
async function registerUser(formData) {
    try {
        const response = await fetch("/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();

        if (response.ok) {
            localStorage.setItem("token", result.token);
            showDashboard();
        } else {
            showAlert(result.message || "Error en el registro.");
        }
    } catch (error) {
        console.error("Error:", error);
        showAlert("Error al conectar con el servidor.");
    }
}

// Cerrar sesión
function logout() {
    localStorage.removeItem("token");
    console.log("Logout!");
    cleanPanels();
    showLoginPanel();
}

window.logout = logout;