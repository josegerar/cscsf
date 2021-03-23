$(function () {
    var csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken");
    var data = {'action': 'searchdata'}
    if (csrfmiddlewaretoken.length > 0) {
        data['csrfmiddlewaretoken'] = csrfmiddlewaretoken[0].value
    }
    var tblistado = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': false,
        'destroy': true,
        'deferRender': true,
        'columns': [
            {'data': 'id'},
            {'data': 'solicitante'},
            {'data': 'laboratorio'},
            {'data': 'proyecto'},
            {'data': 'documento'},
            {'data': 'fecha_autorizacion'},
            {'data': 'estado_solicitud'},
            {'data': 'id'}
        ],
        'columnDefs': [
            {
                'targets': [4],
                'orderable': false,
                'render': function (data, type, row) {
                    return get_tag_url_document(data, 'Ver solicitud')
                }
            },
            {
                'targets': [6],
                'render': function (data, type, row) {
                    if (data.estado === 'registrado') {
                        return "Registrado"
                    } else if (data.estado === 'aprobado') {
                        return "Aprobado"
                    } else if (data.estado === 'entregado') {
                        return "Entregado"
                    } else if (data.estado === 'revision') {
                        return '<label class="btn-danger">Revisión</label>'
                    } else {
                        return ""
                    }
                }
            },
            {
                'targets': [7],
                'orderable': false,
                'render': function (data, type, row) {
                    if (row.estado && row.estado.estado === "entregado" || row.estado.estado === "aprobado") {
                        return ""
                    } else {
                        let buttons = '<a href="/solicitudes/update/' + row.id + '/" class="btn btn-primary"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="/solicitudes/delete/' + row.id + '/" type="button" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a>';
                        return buttons
                    }
                }
            }
        ]
    });

    update_datatable(tblistado, window.location.pathname, data);

    $('#btnSync').on('click', function (event) {
        update_datatable(tblistado, window.location.pathname, data);
    });
});