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
            {
                "className": 'details-control',
                'data': 'id'
            },
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
                        return '<button rel="confirmarSolicitud" class="btn btn-dark btn-flat btn-sm"> <i class="fas fa-save"></i> Aprobar</button>';
                    } else if (data.estado === 'entregado') {
                        return "Entregado";
                    } else if (data.estado === 'revision') {
                        return '<label class="btn-danger">Revisión</label>'
                    } else if (data.estado === 'aprobado') {
                        return "Aprobado";
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

    $('#frmAutorizarSolicitud').on('submit', function (event) {
        event.preventDefault();
        let action_save = $(event.originalEvent.submitter).attr('rel');
        let form = this;
        let parameters = new FormData(form);
        if (action_save === 'aprobar') {
            parameters.append('action', 'aprobarSolicitud');
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
        } else if (action_save === 'revisar') {
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

    addEventListenerOpenDetailRowDatatable('tblistado', tblistado, 'td.details-control',
        function (row, data, dataIndex) {
            updateRowsCallback(row, data, dataIndex);
        });

    function updateRowsCallback(row, data, dataIndex) {
        $(row).find('button[rel="confirmarSolicitud"]').on('click', function (event) {
            $('#modalAutorizarSolicitud').find('input[name=id_solicitud]').val(data.id);
            tbdetallesolicitud.clear();
            tbdetallesolicitud.rows.add(data.detallesolicitud).draw();
            $('#modalAutorizarSolicitud').modal('show');
        });
    }
});