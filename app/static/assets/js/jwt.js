async function refreshToken() {
    const token = localStorage.getItem("token");

    try {
        const response = await fetch("/refresh-token", {
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
        } else {
            console.warn(result.message || "No se pudo renovar el token.");
        }
    } catch (error) {
        console.error("Error al renovar el token:", error);
    }
}

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