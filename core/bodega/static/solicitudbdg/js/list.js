$(function () {
    const data = {'action': 'searchdata', 'csrfmiddlewaretoken': getCookie("csrftoken")};
    var tbdetallesolicitud = $('#tbdetallesolicitud').DataTable({
        'responsive': true,
        'autoWidth': false,
        'destroy': true,
        'columns': [
            {'data': 'stock.bodega.nombre'},
            {'data': 'stock.sustancia.nombre'},
            {'data': 'cantidad'},
            {'data': 'stock.cantidad'}
        ]
    });

    const tblistado = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': false,
        'destroy': true,
        'columns': [
            {'data': 'id'},
            {'data': 'solicitante'},
            {'data': 'laboratorio'},
            {'data': 'nombre_actividad'},
            {'data': 'documento'},
            {'data': 'id'},
            {'data': 'estado_solicitud'}
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
                'targets': [5],
                'orderable': false,
                'render': function (data, type, row) {
                    if (row.hasOwnProperty("fecha_autorizacion")) return row.fecha_autorizacion;
                    else return "No autorizado";
                }
            },
            {
                'targets': [6],
                'orderable': false,
                'render': function (data, type, row) {
                    if (data.estado === 'registrado') {
                        return "Registrado";
                    } else if (data.estado === 'entregado') {
                        return "Entregado";
                    } else if (data.estado === 'revision') {
                        return '<label class="btn-danger">Revisión</label>'
                    } else if (data.estado === 'aprobado') {
                        return '<button rel="entregarSustancias" class="btn btn-dark btn-flat btn-sm"> <i class="fas fa-save"></i> Entregar</button>';
                    }
                }
            }
        ],
        'rowCallback': function (row, data, displayNum, displayIndex, dataIndex) {
            updateRowsCallback(row, data, dataIndex)
        }
    });

    update_datatable(tblistado, window.location.pathname, data);

    $('#btnSync').on('click', function (event) {
        update_datatable(tblistado, window.location.pathname, data);
    });

    $('#frmEntregaSustancia').on('submit', function (event) {
        event.preventDefault();
        let action_save = $(event.originalEvent.submitter).attr('rel');
        let form = this;
        let parameters = new FormData(form);
        if (action_save == 'entregar') {
            parameters.append('action', 'entregarSustancias');
            disableEnableForm(form, true);
            submit_with_ajax(
                window.location.pathname, parameters
                , 'Confirmación'
                , '¿Estas seguro de realizar la siguiente acción?'
                , function (data) {
                    location.reload();
                }, function () {
                    disableEnableForm(form, false);
                }
            );
        } else if (action_save == 'revisar') {
            $('#modalEntregaSustancia').modal('hide');
            $('#frmJustRevision').find('input[name="id_solicitud"]').val(parameters.get("id_solicitud"))
            $('#modalJustRevision').modal('show');
        }
    });

    $('#frmJustRevision').on('submit', function (event) {
        event.preventDefault();
        let form = this;
        let parameters = new FormData(form);
        parameters.append('action', 'revisionSolicitud');
        disableEnableForm(form, true);
        submit_with_ajax(
            window.location.pathname, parameters
            , 'Confirmación'
            , '¿Estas seguro de realizar la siguiente acción?'
            , function (data) {
                location.reload();
            }, function () {
                disableEnableForm(form, false);
            }
        );
    });

    function updateRowsCallback(row, data, dataIndex) {
        $(row).find('button[rel=entregarSustancias]').on('click', function (event) {
            $('#modalEntregaSustancia').find('input[name=id_solicitud]').val(data.id);
            tbdetallesolicitud.clear();
            console.log(data.detallesolicitud)
            tbdetallesolicitud.rows.add(data.detallesolicitud).draw();
            $('#modalEntregaSustancia').modal('show');
        });
    }
});