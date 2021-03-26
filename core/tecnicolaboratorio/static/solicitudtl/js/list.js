$(function () {
    const data = {'action': 'searchdata', 'csrfmiddlewaretoken': getCookie("csrftoken")}
    const tblistado = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': false,
        'destroy': true,
        'columns': [
            {
                "className": 'details-control',
                'data': 'id'
            },
            {'data': 'laboratorio'},
            {'data': 'nombre_actividad'},
            {'data': 'documento'},
            {'data': 'id'},
            {'data': 'estado_solicitud'},
            {'data': 'id'},
            {'data': 'id'}
        ],
        'columnDefs': [
            {
                'targets': [3],
                'orderable': false,
                'render': function (data, type, row) {
                    return get_tag_url_document(data, 'Ver')
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
                        return '<button rel="recibir_solicitud" class="btn btn-success" >Recibir</button>'
                    } else if (data.estado === 'revision') {
                        return '<label class="btn-danger">Revisión</label>'
                    } else {
                        return ""
                    }
                }
            },
            {
                'targets': [6],
                'render': function (data, type, row) {
                    return '<a rel="openobs" class="nav-link" style="cursor: pointer; text-align: center">Ver</a>'
                }
            },
            {
                'targets': [7],
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
        ],
        'rowCallback': function (row, data, displayNum, displayIndex, dataIndex) {
            updateRowsCallback(row, data, dataIndex)
        }
    });

    const tbobservaciones = $('#tbobservaciones').DataTable({
        'responsive': true,
        'autoWidth': false,
        'destroy': true,
        'paging': false,
        'searching': false,
        'ordering': false,
        "info": false,
        'columns': [
            {'data': 'observacion'}
        ]
    });

    const tbdetalles = $('#tbobservaciones').DataTable({
        'responsive': true,
        'autoWidth': false,
        'destroy': true,
        'paging': false,
        'searching': false,
        'ordering': false,
        "info": false,
        'columns': [
            {'data': 'stock.sustancia.nombre'},
            {'data': 'cantidad'},
            {'data': 'observacion'}
        ]
    });

    update_datatable(tblistado, window.location.pathname, data);

    $('#btnSync').on('click', function (event) {
        update_datatable(tblistado, window.location.pathname, data);
    });

    // Add event listener for opening and closing details
    addEventListenerOpenDetailRowDatatable('tblistado', tblistado, 'td.details-control',
        function (row, data, dataIndex) {
            updateRowsCallback(row, data, dataIndex);
        });

    function updateRowsCallback(row, data, dataIndex) {
        $(row).find('a[rel=openobs]').on('click', function (event) {
            //$('#modalDetalleSolicitud').find('textarea[name=observacion]').text(data.observacion);
            console.log(data);
            let observaciones = [];
            if (data.observacion_bodega) observaciones.push({'observacion': data.observacion_bodega});
            if (data.observacion_representante) observaciones.push({'observacion': data.observacion_representante});
            tbobservaciones.clear();
            tbobservaciones.rows.add(observaciones).draw();
            $('#modalDetalleSolicitud').modal('show');
        });
    }
});