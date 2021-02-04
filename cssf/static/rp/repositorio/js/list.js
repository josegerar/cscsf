$(function () {
    var csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken");
    var data = {}
    if (csrfmiddlewaretoken.length > 0) {
        data['csrfmiddlewaretoken'] = csrfmiddlewaretoken[0].value
    }
    sendData(data);
});

function sendData(data) {
    $.ajax({
        'url': window.location.pathname,
        'type': 'POST',
        'data': data,
        'dataType': 'json'
    }).done(function (data) {
        listarArchivos(data)
    }).fail(function (jqXHR, textStatus, errorThrown) {

    }).always(function (data) {

    });
}

function listarArchivos(data) {
    $.each(data, function (indexdata, itemdata) {
        var filas = $('#context-menu-file table tbody tr');
        var existe = false;
        var cantfolder = 0;
        $.each(filas, function (indexfila, itemfila) {
            var datafila = $(itemfila).data("data");
            if (datafila) {
                if (datafila.id == itemdata.id) {
                    existe = true;
                }
                if (datafila.is_dir) {
                    cantfolder++;
                }
            }
        });
        if (!existe) {
            var fila = $('<tr>');
            var colicon = $('<td>');
            var coliname = $('<td>', {style: 'cursor: default'});
            var imageicon = $('<i>');
            if (itemdata.is_dir) {
                imageicon.prop("class", 'fas fa-folder fa-2x');
            } else if (itemdata.is_file) {
                imageicon.prop("class", "far fa-file fa-2x");
            }
            colicon.append(imageicon);
            coliname.append(itemdata.nombre_real);
            fila.append(colicon).append(coliname);
            fila.data("data", itemdata);
            var cantidadFilas = $('#context-menu-file table tbody tr').length;
            if (cantidadFilas < cantfolder) {
                $('#context-menu-file table tbody tr').eq(cantfolder).after(fila);
            } else {
                $('#context-menu-file table tbody').append(fila);
            }
        }
    });
}