$(function () {
    const data = {'action': 'searchdata', 'csrfmiddlewaretoken': getCookie("csrftoken")}
    const tblistado = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': false,
        'destroy': true,
        'columns': [
            {'data': 'id'},
            {'data': 'laboratorio'},
            {'data': 'nombre_actividad'},
            {'data': 'documento'},
            {'data': 'id'},
            {'data': 'estado_solicitud'},
            {'data': 'id'}
        ],
        'columnDefs': [
            {
                'targets': [3],
                'orderable': false,
                'render': function (data, type, row) {
                    return get_tag_url_document(data, 'Ver solicitud')
                }
            },
            {
                'targets': [4],
                'orderable': false,
                'render': function (data, type, row) {
                    if (row.hasOwnProperty("fecha_autorizacion")) return row.fecha_autorizacion;
                    else return "No autorizado";
                }
            },
            {
                'targets': [5],
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
                'targets': [6],
                'orderable': false,
                'render': function (data, type, row) {
                    if (row.estado_solicitud) {
                        if (row.estado_solicitud.estado === "entregado") {
                            return "Recibida";
                        } else if (row.estado_solicitud.estado === "aprobado") {
                            return "Aprobado";
                        } else if (row.estado_solicitud.estado === "revision" || row.estado_solicitud.estado === "registrado") {
                            let buttons = '<a href="/solicitudes/update/' + row.id + '/" class="btn btn-primary"><i class="fas fa-edit"></i></a> ';
                            buttons += '<a href="/solicitudes/delete/' + row.id + '/" type="button" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a>';
                            return buttons;
                        }
                    }
                    return "";
                }
            }
        ]
    });

    update_datatable(tblistado, window.location.pathname, data);

    $('#btnSync').on('click', function (event) {
        update_datatable(tblistado, window.location.pathname, data);
    });
});