$(function () {
    $('a[rel=view_information_user]').on('click', function (evt) {
        $('#modalUpdateInfo').modal('show');
    });

    $('a[rel=change_password_user]').on('click', function (evt) {
        $('#modalChangePass').modal('show');
    });
});