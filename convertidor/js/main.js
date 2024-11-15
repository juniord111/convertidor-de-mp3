const convertForm = document.getElementById("convertForm");
const urlInput = document.getElementById("urlInput");
const statusMessage = document.getElementById("statusMessage");
const downloadLink = document.getElementById("downloadLink");
const mp3Download = document.getElementById("mp3Download");

convertForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const url = urlInput.value.trim();
    if (url === "") {
        alert("Por favor ingresa un enlace válido.");
        return;
    }

    statusMessage.classList.remove("hidden");
    statusMessage.textContent = "Estamos procesando tu solicitud...";

    try {
        const response = await fetch("http://localhost:5001/api/convert", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ url: url }),
        });

        const result = await response.json();

        if (result.success) {
            mp3Download.href = result.mp3Url;
            mp3Download.textContent = "Descargar MP3";
            downloadLink.classList.remove("hidden");
            statusMessage.textContent = "¡Conversión completada!";
        } else {
            statusMessage.textContent = "Hubo un error en la conversión. Intenta de nuevo.";
        }
    } catch (error) {
        console.error("Error al convertir el enlace:", error);
        statusMessage.textContent = "Error al procesar la solicitud. Por favor, intenta nuevamente más tarde.";
    }
});
