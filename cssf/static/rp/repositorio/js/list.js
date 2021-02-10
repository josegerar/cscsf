$(function () {
    init();
});

function init() {
    var csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken");
    var data = {}
    if (csrfmiddlewaretoken.length > 0) {
        data['csrfmiddlewaretoken'] = csrfmiddlewaretoken[0].value
    }
    sendData(data);
}

function sendData(data) {
    $.ajax({
        'url': window.location.pathname,
        'type': 'POST',
        'data': data,
        'dataType': 'json'
    }).done(function (data) {
        if (!data.hasOwnProperty('error')) {
            proccessData(data);
        } else {
            message_error(data.error);
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        message_error(errorThrown);
    }).always(function (data) {

    });
}

function proccessData(data) {
    var tbody = $('<tbody>');
    $.each(data.folders, function (indexdata, itemdata) {
        tbody.append(addRow(itemdata, data.urlrepository));
    });
    $.each(data.files, function (indexdata, itemdata) {
        tbody.append(addRow(itemdata, data.urlrepository));
    });
    $('#context-menu-file table tbody').html("").append(tbody.children());
}

function addRow(itemdata, urlRepository) {
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
    return fila;
}

function changeFolder() {
    var data = $(this).data("data");
    history.pushState(data, null, window.location.origin + data.urlrepository + data.itemdata.id + '/');
}

window.addEventListener('locationchange', function (evt) {
    var data = evt.data;
    if (data) {
        var itemData = data.itemdata;
        if (itemData.is_dir) {
            init();
        } else if (itemData.is_file) {

        }
    } else {
        init();
    }
});