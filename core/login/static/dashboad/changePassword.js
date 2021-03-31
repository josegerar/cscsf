$(function () {
    //envio de datos al servidor
    $('#frmChangePass').on('submit', function (event) {
        event.preventDefault();
        let form = this;
        let parameters = new FormData(form);
        let act = parameters.get("passact");
        let nueva = parameters.get("pass")
        let nueva2 = parameters.get("pass2")
        if (act == nueva) {
            message_info("La nueva contraseña debe ser diferente a la actual");
            return false
        }
        if (nueva !== nueva2) {
            message_info("La contraseña nueva de confirmación es diferente a la contraseña nueva");
            return false
        }
        disableEnableForm(form, true);
        submit_with_ajax(
            window.location.pathname, parameters
            , 'Confirmación'
            , '¿Estas seguro de realizar la siguiente acción?'
            , function (data) {
                location.href = "/logout/"
            }, function () {
                disableEnableForm(form, false);
            }
        );
    });
    $('button[rel=sendCode]').on('click', function (event) {
        event.preventDefault();
        let parameters = new FormData();
        parameters.append("action", "sendCodeConfirm")
        parameters.append("csrfmiddlewaretoken", getCookie("csrftoken"))
        submit_with_ajax(
            window.location.pathname, parameters
            , 'Confirmación'
            , '¿Estas seguro de realizar la siguiente acción?'
            , function (data) {
                message_info("El codigo ha sido enviado a su correo, por favor verificar")
            }, function () {

            }
        );
    });
});