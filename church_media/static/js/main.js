// Auto-dismiss alerts after 4s
setTimeout(() => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        new bootstrap.Alert(alert).close();
    });
}, 3000);

