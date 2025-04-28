$( document ).ready(function() {

    $(document).on('click', '#home', function() {
        cleanDashboard();
        showhomepage();
    });

    $(document).on('click', '#mynotes', function() {
        cleanDashboard();
        showNotes();
    });

    $(document).on('click', '#add-note', function() {
        cleanDashboard();
        addNote();
    });

    $(document).on('click', '#edit-note', function() {
        cleanDashboard();
    });

    $(document).on('click', '#edit-lastnote', function() {
        cleanDashboard();
    });
});

function showDashboard(){
    const main_container = document.getElementById('main-container');
    const dashboardHTML = `
    <section class="dashboard-section">
        <div class="dashboard-header">
            <button id="logout"><i class="bi bi-power"></i></button>
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

    let lastnote;
    try {
        lastnote = await protectedRequest(`/notes/latest/${userid}`, 'GET');
        if (!lastnote || lastnote.error) {
            lastnote = null;
        }
    } catch (error) {
        console.error('Error al obtener la última nota:', error);
        lastnote = null;
    }

    const homepageHTML = `
    <div class="homepage">
        <h1>Bienvenido/a ${user.username}</h1>
        <p>Aquí puedes capturar y organizar tus pensamientos e ideas, añadiendo títulos, descripciones, categorías, etiquetas y más. ¡Comienza hoy tu camino hacia una mejor gestión de notas!.</p>
        <p>Aqui Tienes tu ultima nota creada:</p>
        ${
            lastnote
                ? `
                <div class="homepage-lastnote">
                    <h2>${lastnote.title}</h2>
                    <p class="note-content">${lastnote.content}</p>
                    <p class="note-date">Fecha de creación: ${lastnote.created_at}</p>
                    <div class="homepage-lastnote-actions">
                        <button onclick="editNote(${lastnote.id})" id="edit-lastnote"><i class="bi bi-pencil-square"></i></button>
                        <button onclick="deleteNote(${lastnote.id})" id="delete-lastnote"><i class="bi bi-trash-fill"></i></button>
                    </div>
                </div>
                `
                : `<p>No tienes notas creadas aún. ¡Añade tu primera nota!</p>`
        }
    </div>
    `;

    dashboard_container.innerHTML = homepageHTML;
}

window.showDashboard = showDashboard;

async function showNotes() {
    const dashboard_container = document.querySelector('.dashboard-container');

    let notes;
    try {
        notes = await protectedRequest('/user/notes', 'GET');
        if (!notes || notes.error) {
            dashboard_container.innerHTML = `
            <p class="notes-error">${notes?.error || 'No tienes notas disponibles.'}</p>
            <button id="add-note"><i class="bi bi-plus-circle-fill"></i> Añadir Nota</button>
            `;
            return;
        }
    } catch (error) {
        console.error('Error al cargar las notas:', error);
        dashboard_container.innerHTML = '<p class="error">Error al cargar las notas. Por favor, intenta nuevamente.</p>';
        return;
    }

    const notesHTML = `
    <div class="notes">
        <h1>Mis Notas</h1>
        <div class="notes-options">
            <button id="add-note"><i class="bi bi-plus-circle-fill"></i></button>
        </div>
        <div class="notes-list">
            ${notes.map(note => `
                <div class="note-item">
                    <h2 class="note-title">${note.title}</h2>
                    <p class="note-content">${note.content}</p>
                    <p class="note-date">Fecha de creación: ${note.created_at}</p>
                    <div class="note-actions">
                        <button onclick="editNote(${note.id})" id="edit-note"><i class="bi bi-pencil-square"></i></button>
                        <button onclick="deleteNote(${note.id})" id="delete-note"><i class="bi bi-trash-fill"></i></button>
                    </div>
                </div>
            `).join('')}
        </div>
    </div>
    `;
    dashboard_container.innerHTML = notesHTML;

    document.getElementById('add-note').addEventListener('click', addNote);
}

async function addNote() {
    const dashboard_container = document.querySelector('.dashboard-container');
    const addNoteHTML = `
    <div class="notes">
        <h1>Añadir Nota</h1>
        <div class="add-note">
            <form id="add-note-form">
                <label for="title">Título</label>
                <input type="text" id="title" name="title" maxlength="20" required>
                <label for="content">Contenido</label>
                <textarea id="content" name="content" maxlength="255" required></textarea>  
                <button type="submit" id="add-note-submit">Guardar Nota</button>
            </form>
        </div>  
    </div>
    `
    dashboard_container.innerHTML = addNoteHTML;

    const form = document.getElementById('add-note-form');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = {
            title: document.getElementById('title').value,
            content: document.getElementById('content').value
        };

        try {
            const response = await protectedRequest('/notes/add', 'POST', formData);
            if (response.success) {
                showNotes();
            } else {
                alert(response.error || 'Error al añadir la nota.');
            }
        } catch (error) {
            console.error('Error al añadir la nota:', error);
        }
    });
}

async function editNote(noteId) {
    const dashboard_container = document.querySelector('.dashboard-container');

    let noteData;
    try {
        noteData = await protectedRequest(`/notes/${noteId}`, 'GET');
        if (!noteData) {
            console.log('No se pudo cargar la nota.');
            return;
        }
    } catch (error) {
        console.error('Error al cargar la nota:', error);
        return;
    }

    const editNoteHTML = `
    <div class="notes">
        <h1>Editar Nota</h1>
        <div class="edit-note">
            <form id="edit-note-form">
                <label for="title">Título</label>
                <input type="text" id="title" name="title" maxlength="10" value="${noteData.title}" required>
                <label for="content">Contenido</label>
                <textarea id="content" name="content" maxlength="255" required>${noteData.content}</textarea>  
                <button type="submit" id="edit-note-submit">Actualizar Nota</button>
            </form>
        </div>
    </div>
    `;
    dashboard_container.innerHTML = editNoteHTML;

    const form = document.getElementById('edit-note-form');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = {
            title: document.getElementById('title').value,
            content: document.getElementById('content').value
        };

        try {
            const response = await protectedRequest(`/notes/edit/${noteId}`, 'POST', formData);
            if (response.success) {
                showNotes();
            } else {
                alert(response.error || 'Error al actualizar la nota.');
            }
        } catch (error) {
            console.error('Error al actualizar la nota:', error);
        }
    });
}

window.editNote = editNote;

async function deleteNote(noteId) {
    if (!noteId) {
        console.log('No se proporcionó un ID de nota válido.');
        return;
    }

    try {
        const response = await protectedRequest(`/notes/remove/${noteId}`, 'DELETE');
        if (response.success) {
            showNotes();
        } else {
            alert(response.error || 'Error al eliminar la nota.');
        }
    } catch (error) {
        console.error('Error al eliminar la nota:', error);
    }
}

window.deleteNote = deleteNote;