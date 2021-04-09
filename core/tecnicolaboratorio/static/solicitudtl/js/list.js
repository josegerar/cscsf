$(function () {
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
            {'data': 'codigo'},
            {'data': 'estado'},
            {'data': 'id'},
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
                'targets': [5],
                'render': function (data, type, row) {
                    if (data === 'registrado') {
                        return "Registrado"
                    } else if (data === 'aprobado') {
                        return "Aprobado"
                    } else if (data === 'entregado') {
                        return '<button rel="recibir_solicitud" class="btn btn-success" >Recibir</button>'
                    } else if (data === 'revision') {
                        return '<label class="btn-danger">Revisión</label>'
                    } else if (data === "recibido") {
                        return "Recibido";
                    } else {
                        return ""
                    }
                }
            },
            {
                'targets': [6],
                'render': function (data, type, row) {
                    return '<a rel="opendetail" class="nav-link" style="cursor: pointer; text-align: center">Ver</a>'
                }
            },
            {
                'targets': [7],
                'orderable': false,
                'render': function (data, type, row) {
                    if (row.estado) {
                        if (row.estado === "revision" || row.estado === "registrado") {
                            return '<a href="/solicitudes/update/' + row.id + '/" class="btn btn-primary"><i class="fas fa-edit"></i></a> ';
                        }
                    }
                    return "";
                }
            },
            {
                'targets': [8],
                'orderable': false,
                'render': function (data, type, row) {
                    if (row.estado) {
                        if (row.estado === "revision" || row.estado === "registrado") {
                            return '<a href="/solicitudes/delete/' + row.id + '/" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a>';
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
        'autoWidth': true,
        'paging': false,
        'searching': false,
        'ordering': false,
        "info": false,
        'columns': [
            {'data': 'observacion'}
        ]
    });

    const tbdetalles = $('#tbdetallesolicitud').DataTable({
        'responsive': true,
        'autoWidth': true,
        'paging': false,
        'searching': false,
        'ordering': false,
        "info": false,
        'columns': [
            {'data': 'sustancia'},
            {'data': 'cant_sol'},
            {'data': 'cant_ent'},
            {'data': 'cant_con'}
        ]
    });

    get_list_data_ajax_loading(window.location.pathname, {'action': 'searchdata'}, function (response) {
        tblistado.clear();
        tblistado.rows.add(response).draw();
    });

    $('#btnSync').on('click', function (event) {
        get_list_data_ajax_loading(window.location.pathname, {'action': 'searchdata'}, function (response) {
            tblistado.clear();
            tblistado.rows.add(response).draw();
        });
    });

    // Add event listener for opening and closing details
    addEventListenerOpenDetailRowDatatable('tblistado', tblistado, 'td.details-control',
        function (row, data, dataIndex) {
            updateRowsCallback(row, data, dataIndex);
        });

    function updateRowsCallback(row, data, dataIndex) {
        $(row).find('a[rel=opendetail]').on('click', function (event) {
            $('#modalDetalleSolicitud').find('button[type="submit"]').css("display", 'none');
            $('#modalDetalleSolicitud').find('input[name="action"]').val("");
            $('#modalDetalleSolicitud').find('input[name="id"]').val("");
            llenarModalDetalles(data);
        });
        $(row).find('button[rel=recibir_solicitud]').on('click', function (event) {
            $('#modalDetalleSolicitud').find('button[type="submit"]').css("display", 'block');
            $('#modalDetalleSolicitud').find('input[name="action"]').val("recibirSolicitud");
            $('#modalDetalleSolicitud').find('input[name="id"]').val(data.id);
            llenarModalDetalles(data);
        });
    }

    function llenarModalDetalles(data = {}) {
        get_list_data_ajax_loading(window.location.pathname, {'action': 'search_detalle', 'id_sl': data.id}
            , function (response) {
                let observaciones = [];
                observaciones.push({'observacion': data.obs_bd});
                observaciones.push({'observacion': data.obs_rp});
                tbobservaciones.clear();
                tbobservaciones.rows.add(observaciones).draw();
                tbdetalles.clear();
                tbdetalles.rows.add(response).draw();
                $('#modalDetalleSolicitud').modal('show');
            });
    }

    active_events_filters(['id', 'action', 'type'], function (data) {
        get_list_data_ajax_loading(window.location.pathname, data, function (response) {
            tblistado.clear();
            tblistado.rows.add(response).draw();
        });
    });

    $('#frmDetalleSolicitud').on('submit', function (event) {
        event.preventDefault();
        let form = this;
        let parameters = new FormData(form);
        disableEnableForm(form, true);
        submit_with_ajax(
            window.location.pathname, parameters
            , 'Confirmación'
            , '¿Estas seguro de realizar la siguiente acción?'
            , function (data) {
                $('#modalDetalleSolicitud').modal('hide');
                location.reload();
            }, function () {
                disableEnableForm(form, false);
            }
        );
    });
});