$(function () {
    $('#formNewFolder').on('submit', function (event) {
        event.preventDefault();
        var form = this;
        var parameters = $(this).serializeArray();
        disableEnableForm(form, true);
        $.ajax({
            'url': window.location.pathname,
            'type': 'POST',
            'data': parameters,
            'dataType': 'json'
        }).done(function (data) {
            if (!data.hasOwnProperty('error')) {
                listarArchivos(data.content, data.urlrepository);
                $('#modalNewFolder').modal('hide');
            } else {
                message_error(data.error);
            }
            disableEnableForm(form, false);
        }).fail(function (jqXHR, textStatus, errorThrown) {
            message_error(errorThrown);
            disableEnableForm(form, false);
        }).always(function (data) {

        });
    });
});