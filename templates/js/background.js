$(document).ready(function () {
    $('goals').change(function () {
        localStorage.setItem('goal', $(this).val());
        $('goals').value(localStorage.getItem('goal'));
    });
});