// Obtener información del usuario desde el token
function getUserFromToken() {
    const token = localStorage.getItem("token");
    if (!token || isTokenExpired(token)) {
        return null;
    }

    try {
        const payload = JSON.parse(atob(token.split('.')[1])); // Decodificar el payload del token

        if(!payload.privilege) {
            return { id: payload.user_id };
        }

        return {
            id: payload.user_id,
            privilege: payload.privilege
        };
    } catch (error) {
        console.error("Error al decodificar el token:", error);
        return null;
    }
}
window.getUserFromToken = getUserFromToken;

function isTokenExpired(token) {
    if (!token) {
        console.error("El token no existe o es inválido.");
        return true;
    }

    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        const currentTime = Math.floor(Date.now() / 1000); 
        return payload.exp < currentTime;
    } catch (error) {
        console.error("Error al verificar el token:", error);
        return true;
    }
}

window.isTokenExpired = isTokenExpired;

async function refreshToken() {
    const token = localStorage.getItem("token");

    try {
        const response = await fetch("/api/refresh-token", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            }
        });

        const result = await response.json();

        if (response.ok && result.token) {
            localStorage.setItem("token", result.token);
            console.log("Token renovado:", result.token);
        } else if (result.message == "Token inválido.") {
            logout();
            showAlert("Por favor, inicia sesión nuevamente.");
            console.warn(result.message || "No se pudo renovar el token.");
        } else {
            console.warn(result.message || "No se pudo renovar el token.");
        }
    } catch (error) {
        console.error("Error al renovar el token:", error);
    }
}

async function fetchUserData(userId) {
    try {
        const response = await fetch(`/api/get_user/${userId}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (response.ok) {
            const userData = await response.json();
            return userData;
        } else {
            console.error("Error al obtener los datos del usuario:", await response.json());
            return null;
        }
    } catch (error) {
        console.error("Error al conectar con el servidor:", error);
        return null;
    }
}

window.fetchUserData = fetchUserData;


async function protectedRequest(url, method = "GET", body = null) {
    await refreshToken();

    const token = localStorage.getItem("token");
    const headers = {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
    };

    const options = { method, headers };
    if (body) {
        options.body = JSON.stringify(body);
    }

    const response = await fetch(url, options);
    return response.json(); 
}

window.protectedRequest = protectedRequest;