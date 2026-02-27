document.addEventListener("DOMContentLoaded", function () {
    const alerts = document.querySelectorAll(".custom-alert");

    alerts.forEach(alert => {
        const closeBtn = alert.querySelector(".close-alert");

        closeBtn.addEventListener("click", () => {
            alert.remove();
        });

        // Fecha automaticamente após 4 segundos
        setTimeout(() => {
            alert.remove();
        }, 4000);
    });
});