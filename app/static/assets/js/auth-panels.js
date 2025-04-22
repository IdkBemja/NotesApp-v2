

$(document).ready(function() {

    showLoginPanel();
    $(document).on('click', '#register-panel', function() {
        cleanPanels();
        showRegisterPanel();
    });

    $(document).on('click', '#login-panel', function() {
        cleanPanels();
        showLoginPanel();
    });
});

function showLoginPanel() {
    const main_container = document.getElementById('main-container');
    const login_panelHTML = `
    <section class="login-section">
            <h1>Iniciar Sesión</h1>
            <div class="alert" style="display: none"></div>
            <form id="login-form" method="POST" action="">
                <div class="form-group">
                    <label for="username">Usuario</label>
                    <input type="text" id="username" name="username" required maxlength="10">
                </div>
                <div class="form-group">
                    <label for="password">Contraseña</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <a href="#">¿Olvido La Contraseña?</a>
                <div class="form-group">
                    <button type="submit">Iniciar Sesión</button>
                </div>
            </form>
            <p id="register-panel"><u>¿No tienes cuenta?</u> Regístrate.</p>
        </section>
    `

    main_container.innerHTML = login_panelHTML;
}

function showRegisterPanel() {
    const main_container = document.getElementById('main-container');
    const register_panelHTML = `
    <section class="register-section">
            <h1>Registrarse</h1>
            <div class="alert" style="display: none"></div>
            <form action="" id="register-form">
                <div class="form-group">
                    <label for="username">Usuario</label>
                    <input type="text" id="username" name="username" placeholder="Usuario" required maxlength="10">
                </div>
                <div class="form-group">
                    <label for="email">Correo Electronico</label>
                    <input type="email" id="email" name="email" placeholder="Correo Electronico" required>
                </div>
                <div class="form-group">
                    <label for="password">Contraseña</label>
                    <input type="password" id="password" name="password" placeholder="Contraseña" required>
                </div>
                <div class="form-group">
                    <label for="confirm_password">Repite Contraseña</label>
                    <input type="password" id="confirm_password" name="confirm_password" placeholder="Repite Contraseña" required>
                </div>
                <div class="form-group">
                    <button type="submit">Registrarse</button>
                </div>
            </form>
            <p id="login-panel"><u>¿Ya tienes cuenta?</u> Inicia Sesión.</p>
        </section>
    `

    main_container.innerHTML = register_panelHTML;
}

function showAlert(message) {
    const alertDiv = document.querySelector('.alert');
    if (!alertDiv) {
        console.error("No se encontró el contenedor '.alert'.");
        return;
    }

    // Verificar si el contenedor '.alert' es hijo de '.register-section' o '.login-section'
    const parentSection = alertDiv.closest('.register-section') || alertDiv.closest('.login-section');
    if (!parentSection) {
        console.error("El contenedor '.alert' no es hijo de '.register-section' ni de '.login-section'.");
        return;
    }

    // Mostrar el mensaje en el contenedor '.alert'
    alertDiv.innerHTML = message;
    alertDiv.style.display = 'block';
}

window.showAlert = showAlert;

function cleanPanels() {
    const main_container = document.getElementById('main-container');
    main_container.innerHTML = '';
}