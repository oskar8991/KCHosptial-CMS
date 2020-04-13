$(document).ready(function () {
    $('#collapse').on('click', function () {
        $('#sidebar').toggleClass('hidden');
    });

    $('#collapse').on('click', function () {
        $('#content').toggleClass('hidden');
    });
});