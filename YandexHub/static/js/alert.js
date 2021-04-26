function view_alert(text) {
    document.querySelectorAll('.toast').forEach((elem) => {
        elem.style.display = 'block';
        elem.className = "toast show";
    });
    document.getElementById('toast-body').innerHTML = text;

    document.querySelectorAll('.toast').forEach((elem) => {
        setTimeout(function () {
            elem.style.display = 'none';
        }, 7500);
    });
}