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
});


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
            ShowDashboard();
        } else {
            showAlert(result.message || "Error en el inicio de sesión.");
        }
    } catch (error) {
        console.error("Error:", error);
        showAlert("Error al conectar con el servidor.");
    }
}

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
            ShowDashboard();
        } else {
            showAlert(result.message || "Error en el registro.");
        }
    } catch (error) {
        console.error("Error:", error);
        showAlert("Error al conectar con el servidor.");
    }
}

function getUserFromToken() {
    const token = localStorage.getItem("token");
    if (!token) {
        return null;
    }

    try {
        const payload = jwt.decode(token);
        return payload;
    } catch (error) {
        console.error("Error al decodificar el token:", error);
        return null;
    }
}

async function getUserInfo() {
    const userId = getUserIdFromToken();
    if (!userId) {
        console.error("No se pudo obtener el user_id del token.");
        return null;
    }

    try {
        const response = await fetch(`/api/get_user/${userId}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (response.ok) {
            const userInfo = await response.json();
            return userInfo;
        } else {
            console.error("Error al obtener los datos del usuario:", await response.json());
            return null;
        }
    } catch (error) {
        console.error("Error al conectar con el servidor:", error);
        return null;
    }
}

function logout(){
    localStorage.removeItem("token");
    localStorage.removeItem("user_id");
    console.log("Logout!");
    cleanPanels();
    showLoginPanel();
}