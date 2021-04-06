$(function () {
    //envio de datos al servidor
    $('#frmRecuperarUser').on('submit', function (event) {
        event.preventDefault();
        let form = this;
        let parameters = new FormData(form);
        let correo = parameters.get("correo");
        if(correo.length <= 0)
        {
            message_error("Ingrese el correo")
            return false;
        }
        disableEnableForm(form, true);
        submit_with_ajax(
            window.location.pathname
            , parameters
            , 'Confirmación'
            , '¿Estas seguro de realizar la siguiente acción?'
            , function (data) {
                location.href = "/"
            }, function () {
                disableEnableForm(form, false);
            }
        );
    });
});