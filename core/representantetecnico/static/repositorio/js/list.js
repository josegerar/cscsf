const repositorio = {
    datatable: null,
    urlrepository: null,
    cookie: getCookie("csrftoken"),
    data: {'action': 'searchcontent', 'type': 'repository'},
    actualizar_ruta: function (rutas) {
        let parent = $('#rutasrepositorio');
        let home = $('<li class="breadcrumb-item"><a style="cursor:pointer;" rel="link-ruta" data-id="0">Inicio</a></li>');
        parent.html("").append(home);
        for (let i = rutas.length; i > 0; i--) {
            let item = rutas[i - 1];
            let ruta = $(`<li class="breadcrumb-item"><a style="cursor:pointer;" rel="link-ruta" data-id="${item.id}">${item.nombre}</a></li>`);
            parent.append(ruta);
        }
        this.activar_events_actualizar_ruta();
    },
    activar_events_actualizar_ruta: function f() {
        $('#rutasrepositorio').find('a[rel=link-ruta]').on('click', function (evt) {
            let filter = this;
            $('#rutas-repositorio').find('a[rel=link-ruta]').removeClass("active");
            $(filter).addClass("active");
            let id = parseInt($(filter).data('id'));
            if (id > 0) {
                let parent = {'id': id, 'is_dir': true};
                history.pushState(parent, null, window.location.origin + repositorio.urlrepository + parent.id + '/');
            } else {
                history.pushState(null, null, window.location.origin + repositorio.urlrepository);
            }
        });
    },
    delete_item: function (data) {
        let parameters = new FormData();
        parameters.append("csrfmiddlewaretoken", this.cookie);
        parameters.append("action", 'deleteitem');
        parameters.append("id", data.id);
        $.ajax({
            'url': window.location.pathname,
            'type': 'POST',
            'data': parameters,
            'dataType': 'json',
            'processData': false,
            'contentType': false
        }).done(function (data) {
            if (!data.hasOwnProperty('error')) {
                repositorio.datatable.ajax.reload();
            } else {
                message_error(data.error);
            }
        }).fail(function (jqXHR, textStatus, errorThrown) {
            message_error(errorThrown);
        }).always(function (data) {

        });
    },
    restaurar_item: function (data) {
        let parameters = new FormData();
        parameters.append("csrfmiddlewaretoken", this.cookie);
        parameters.append("action", 'restoreitem');
        parameters.append("id", data.id);
        $.ajax({
            'url': window.location.pathname,
            'type': 'POST',
            'data': parameters,
            'dataType': 'json',
            'processData': false,
            'contentType': false
        }).done(function (data) {
            if (!data.hasOwnProperty('error')) {
                repositorio.datatable.ajax.reload();
            } else {
                message_error(data.error);
            }
        }).fail(function (jqXHR, textStatus, errorThrown) {
            message_error(errorThrown);
        }).always(function (data) {

        });
    },
    descargar_archivo: function (url, nombre) {
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        // the filename you want
        a.download = nombre;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    },
    disable_enable_contextmenu: function (enabled = true, selector = '') {
        const $trigger = $(`${selector}`);
        if ($trigger.hasClass('context-menu-disabled')) {
            $trigger.contextMenu(enabled);
        } else {
            $trigger.contextMenu(enabled);
        }
    }
}
$(function () {
    repositorio.datatable = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': true,
        'destroy': true,
        'deferRender': true,
        'paging': false,
        'searching': false,
        'ordering': false,
        'info': false,
        'processing': true,
        'scrollY': '55vh',
        'scrollCollapse': false,
        "language": {
            "emptyTable": "",
            "zeroRecords": ""
        },
        'ajax': {
            'url': window.location.pathname,
            'type': 'GET',
            'data': function (d) {
                d.action = repositorio.data.action;
                d.type = repositorio.data.type;
            },
            "dataSrc": function (json) {
                repositorio.urlrepository = json.urlrepository;
                repositorio.actualizar_ruta(json.ruta);
                return json.data;
            }
        },
        'columns': [
            {'data': 'id'},
            {'data': 'nombre'},
            {'data': 'create_date'},
        ],
        'columnDefs': [
            {
                'targets': [1],
                'render': function (data, type, row) {
                    if (row.is_dir) {
                        return `<div style="display: flex"><i class="fas fa-folder fa-2x"></i> <p>${data}</p></div>`;
                    } else if (row.is_file) {
                        return `<div style="display: flex"><i class="far fa-file-pdf fa-2x"></i> <p>${data}</p></div>`;
                    }
                    return data;
                }
            }
        ],
        'rowCallback': function (row, data, displayNum, displayIndex, dataIndex) {
            updateRowsCallback(row, data, dataIndex)
        }
    });

    function updateRowsCallback(row, data, dataIndex) {
        if (repositorio.data.type === 'recicle') {
            repositorio.disable_enable_contextmenu(false, '#context-menu-file');
        } else if (repositorio.data.type === 'repository') {
            repositorio.disable_enable_contextmenu(true, '#context-menu-file')
        }
        if (data.is_recicler) {
            $(row).addClass('item-recicler');
        } else {
            $(row).on('dblclick', function (event) {
                history.pushState(data, null, window.location.origin + repositorio.urlrepository + data.id + '/');
            });
            if (data.is_dir) $(row).addClass('item-repository-folder');
            else if (data.is_file) $(row).addClass('item-repository-file');
        }
        $(row).css("cursor", "pointer");
    }

    $('#formNewFolder').on('submit', function (event) {
        event.preventDefault();
        const form = this;
        const parameters = new FormData(form);
        disableEnableForm(form, true);
        $.ajax({
            'url': window.location.pathname,
            'type': 'POST',
            'data': parameters,
            'dataType': 'json',
            'processData': false,
            'contentType': false
        }).done(function (data) {
            if (!data.hasOwnProperty('error')) {
                repositorio.datatable.ajax.reload();
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

    active_events_filters(['action', 'type'], function (data_send) {
        repositorio.data = data_send;
        repositorio.datatable.ajax.reload();
    });
});

window.addEventListener('locationchange', function (evt) {
    var data = evt.detail;
    if (data) {
        if (data.is_dir) {
            repositorio.datatable.ajax.url(window.location.pathname).load();
        } else if (data.is_file) {
            viewFile(data);
        }
    } else {
        repositorio.datatable.ajax.reload();
    }
});