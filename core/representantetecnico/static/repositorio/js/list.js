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
    console.log(data);
    var parent = null;
    if (data.hasOwnProperty("parent")) {
        parent = data.parent
    }
    if (data.hasOwnProperty("object")) {
        var object = data.object;
        if (object.is_file) {
            viewFile({'itemdata': object, 'urlrepository': data.urlrepository, "parent": parent});
        } else if (object.is_dir) {
            parent = object;
        }
    }
    var tbody = $(document.createElement("tbody"));
    $.each(data.folders, function (indexdata, itemdata) {
        tbody.append(addRow(itemdata, data.urlrepository));
    });
    $.each(data.files, function (indexdata, itemdata) {
        tbody.append(addRow(itemdata, data.urlrepository, parent));
    });
    $('#context-menu-file table tbody').replaceWith(tbody);
}

function addRow(itemdata, urlRepository, parent) {
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
    var data = {
        'urlrepository': urlRepository,
        'itemdata': itemdata
    }
    if (parent) {
        data['parent'] = parent;
    }
    fila.data("data", data);
    fila.dblclick(changeFolder);
    return fila;
}

function changeFolder() {
    var data = $(this).data("data");
    history.pushState(data, null, window.location.origin + data.urlrepository + data.itemdata.id + '/');
}

window.addEventListener('locationchange', function (evt) {
    var data = evt.detail;
    if (data) {
        var itemData = data.itemdata;
        if (itemData.is_dir) {
            init();
        } else if (itemData.is_file) {
            viewFile(data);
        }
    } else {
        init();
    }
});