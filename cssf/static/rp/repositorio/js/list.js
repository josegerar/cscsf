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
        if (!data.hasOwnProperty('error')) {
            listarArchivos(data.content, data.urlrepository);
        } else {
            message_error(data.error);
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        message_error(errorThrown);
    }).always(function (data) {

    });
}

function listarArchivos(data, urlRepository) {
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
                imageicon.prop("class", "far fa-file-pdf fa-2x");
            }
            colicon.append(imageicon);
            coliname.append(itemdata.nombre_real);
            fila.append(colicon).append(coliname);
            fila.data("data", {
                'urlrepository': urlRepository,
                'itemdata': itemdata
            });
            fila.dblclick(changeFolder);
            var cantidadFilas = $('#context-menu-file table tbody tr').length;
            if (cantidadFilas < cantfolder) {
                $('#context-menu-file table tbody tr').eq(cantfolder).after(fila);
            } else {
                $('#context-menu-file table tbody').append(fila);
            }
        }
    });
}

function changeFolder() {
    var data = $(this).data("data");
    location.href = data.urlrepository + data.itemdata.id + '/';
}