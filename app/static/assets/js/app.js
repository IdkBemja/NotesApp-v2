$( document ).ready(function() {

    $(document).on('click', '#home', function() {
        cleanDashboard();
        showhomepage();
    });

    $(document).on('click', '#mynotes', function() {
        cleanDashboard();
        showNotes();
    });
});

function showDashboard(){
    const main_container = document.getElementById('main-container');
    const dashboardHTML = `
    <section class="dashboard-section">
        <div class="dashboard-header">
            <button id="logout"><i class="bi bi-power"></i> Cerrar Sesión</button>
            <ul class="dashboard-nav">
                <li id="home"><i class="bi bi-house"></i> Inicio</li>
                <li id="mynotes"><i class="bi bi-archive"></i> Mis Notas</li>
            </ul>
        </div>
        <div class="dashboard-container">
        </div>
    </section>
    `

    main_container.innerHTML = dashboardHTML;
    showhomepage();
}

function cleanDashboard() {
    const dashboard_container = document.querySelector('.dashboard-container');
    dashboard_container.innerHTML = '';
}

async function showhomepage(){
    const dashboard_container = document.querySelector('.dashboard-container');

    const userid = getUserFromToken();

    if (!userid) {
        dashboard_container.innerHTML = `<p>Error: No se pudo obtener el ID de usuario.</p>`;
        return;
    }

    const user = await fetchUserData(userid);

    if (!user) {
        dashboard_container.innerHTML = `<p>Error: No se pudo obtener la información del usuario.</p>`;
        return;
    }

    const homepageHTML = `
    <div class="homepage">
        <h1>Bienvenido/a ${user.username}</h1>
        <p>Aquí puedes capturar y organizar tus pensamientos e ideas, añadiendo títulos, descripciones, categorías, etiquetas y más. ¡Comienza hoy tu camino hacia una mejor gestión de notas!.</p>
        <p>Aqui Tienes tu ultima nota creada:</p>
        <div class="homepage-lastnote">
            <h2>{lastnote.title}</h2>
            <p>{lastnote.content}</p>
            <p class="note-date">{lastnote.created_at}</p>
            <div class="homepage-lastnote-actions">
                <button id="edit-lastnote">Editar Nota</button>
                <button id="delete-lastnote">Eliminar Nota</button>
            </div>
        </div>
    </div>
    `

    dashboard_container.innerHTML = homepageHTML;
}

window.showDashboard = showDashboard;

async function showNotes(){
    const dashboard_container = document.querySelector('.dashboard-container');
    const notesHTML = `
    <div class="notes">
        <h1>Mis Notas</h1>
        <div class="notes-options">
            <button id="add-note">Añadir Nota</button>
            <button id="delete-note">Eliminar Nota</button>
        </div>
        <div class="notes-list">
            <div class="note-item">
                <h2>Nota 1</h2>
                <p>Contenido de la nota 1</p>
                <p class="note-date">Fecha de creación: 2023-10-01</p>
                <div class="note-actions">
                    <button id="edit-note">Editar Nota</button>
                    <button id="delete-note">Eliminar Nota</button>
                </div>
            </div>
            <div class="note-item">
                <h2>Nota 2</h2>
                <p>Contenido de la nota 2</p>
                <p class="note-date">Fecha de creación: 2023-10-02</p>
                <div class="note-actions">
                    <button id="edit-note">Editar Nota</button>
                    <button id="delete-note">Eliminar Nota</button>
                </div>
        </div>
    </div>
    `
    dashboard_container.innerHTML = notesHTML;
}