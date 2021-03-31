$(function () {
    //envio de datos al servidor
    $('#frmChangePass').on('submit', function (event) {
        event.preventDefault();
        let form = this;
        let action_save = $(event.originalEvent.submitter).attr('rel');
        let parameters = new FormData(form);
        disableEnableForm(form, true);
        submit_with_ajax(
            window.location.pathname, parameters
            , 'Confirmación'
            , '¿Estas seguro de realizar la siguiente acción?'
            , function (data) {
                location.reload();
            }, function () {
                disableEnableForm(form, false);
            }
        );
    });
});