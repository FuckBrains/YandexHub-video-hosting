function view_alert(text) {
    document.querySelectorAll('#alert').forEach((elem) => {
        elem.style.display = 'block';
        elem.className = "toast show";
    });
    document.getElementById('alert-body').innerHTML = text;

    document.querySelectorAll('#alert').forEach((elem) => {
        setTimeout(function () {
            elem.style.display = 'none';
        }, 7500);
    });
}