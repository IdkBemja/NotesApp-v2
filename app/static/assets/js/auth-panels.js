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
                    <label for="confirm_passwd">Repite Contraseña</label>
                    <input type="password" id="confirm_passwd" name="confirm_passwd" placeholder="Repite Contraseña" required>
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

function cleanPanels() {
    const main_container = document.getElementById('main-container');
    main_container.innerHTML = '';
}