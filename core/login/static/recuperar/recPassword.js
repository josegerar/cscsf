$(function () {
    //envio de datos al servidor
    $('#frmRecuperarPass').on('submit', function (event) {
        event.preventDefault();
        let form = this;
        let parameters = new FormData(form);
        let nueva = parameters.get("pass")
        let nueva2 = parameters.get("pass2")
        if (nueva !== nueva2) {
            message_info("La contraseña nueva de confirmación es diferente a la contraseña nueva");
            return false
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
    $('button[rel=sendCode]').on('click', function (event) {
        event.preventDefault();
        let parameters = new FormData();
        let usuario = $('input[name=usuario]').val();
        if(usuario.length === 0)
        {
            message_error("Registre el usuario");
            return false;
        }
        parameters.append("usuario", usuario);
        parameters.append("action", "sendCodeConfirm");
        parameters.append("csrfmiddlewaretoken", getCookie("csrftoken"));
        submit_with_ajax(
            window.location.pathname
            , parameters
            , 'Confirmación'
            , '¿Estas seguro de realizar la siguiente acción?'
            , function (data) {
                message_info("El codigo ha sido enviado a su correo, por favor verificar")
            }, function () {

            }
        );
    });
});