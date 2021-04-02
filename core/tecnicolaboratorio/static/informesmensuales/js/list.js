$(function () {
    const data = {'action': 'searchdata'}
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
            {'data': 'mes'},
            {'data': 'year'},
            {'data': 'id'},
            {'data': 'id'},
            {'data': 'id'},
            {'data': 'id'}
        ],
        'columnDefs': [
            {
                'targets': [4],
                'orderable': false,
                'render': function (data, type, row) {
                    return '<button rel="ver_detalles" class="btn btn-success btn-flat" >Ver</button>'
                }
            },
            {
                'targets': [5],
                'orderable': false,
                'render': function (data, type, row) {
                    if (row.is_editable) {
                        return '<button rel="archivar_informe" class="btn btn-secondary btn-flat" > <i class="fas fa-archive"></i></button> ';
                    }
                    return "Informe archivado";
                }
            },
            {
                'targets': [6],
                'orderable': false,
                'render': function (data, type, row) {
                    if (row.is_editable) {
                        return '<a href="/informes-mensuales/update/' + row.id + '/" class="btn btn-primary btn-flat"><i class="fas fa-edit"></i></a> ';
                    }
                    return "";
                }
            },
            {
                'targets': [7],
                'orderable': false,
                'render': function (data, type, row) {
                    if (row.is_editable) {
                        return '<a href="/informes-mensuales/delete/' + row.id + '/" class="btn btn-danger btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    }
                    return "";
                }
            }
        ],
        'rowCallback': function (row, data, displayNum, displayIndex, dataIndex) {
            updateRowsCallback(row, data, dataIndex)
        }
    });
    const tbdetalleinforme = $('#tbdetallesinforme').DataTable({
        'responsive': true,
        'autoWidth': true,
        'ordering': false,
        'columns': [
            {
                "className": 'details-control',
                'data': 'id'
            },
            {'data': 'sustancia.nombre'},
            {'data': 'unidad_medida'},
            {'data': 'cantidad_lab'},
            {'data': 'cantidad_consumida'},
            {'data': 'id'}
        ],
        'columnDefs': [
            {
                'targets': [5],
                'orderable': false,
                'render': function (data, type, row) {
                    return '<button type="button" rel="ver_desglose" class="btn btn-success btn-flat" ><i class="fas fa-people-carry"></i></button>'
                }
            }
        ],
        'rowCallback': function (row, data, displayNum, displayIndex, dataIndex) {
            updateRowsCallbackDetalles(row, data, dataIndex);
        }
    });
    const tbdesglosedetalleinforme = $('#tbdesglosesustanciainforme').DataTable({
        'responsive': true,
        'autoWidth': false,
        'ordering': false,
        'columns': [
            {'data': 'solicitud'},
            {'data': 'cantidad_solicitada'},
            {'data': 'responsable_actividad'},
            {'data': 'cantidad_consumida_total'},
            {'data': 'cantidad_consumida'},
            {'data': 'id'},
            {'data': 'documento'}
        ],
        'columnDefs': [
            {
                'targets': [5],
                'render': function (data, type, row) {
                    return (parseFloat(row.cantidad_solicitada) - parseFloat(row.cantidad_consumida_total)).toFixed(4)
                }
            },
            {
                'targets': [6],
                'orderable': false,
                'render': function (data, type, row) {
                    return get_tag_url_document(data, 'Ver')
                }
            }
        ]
    });

    get_list_data_ajax_loading(window.location.pathname, data, function (response) {
        tblistado.clear();
        tblistado.rows.add(response).draw();
    });

    active_events_filters(['id', 'action', 'type'], function (data) {
        get_list_data_ajax_loading(window.location.pathname, data, function (response) {
            tblistado.clear();
            tblistado.rows.add(response).draw();
        });
    });

    $("#frmverdetalles").find('button[rel=btnSync]').on('click', function (evt) {
        let id_detalle = $("#frmverdetalles").find('input[name=id_informe]').val();
        updatetbDetallesInforme(id_detalle);
    });

    // Add event listener for opening and closing details
    addEventListenerOpenDetailRowDatatable('tblistado', tblistado, 'td.details-control',
        function (row, data, dataIndex) {
            updateRowsCallback(row, data, dataIndex);
        });

    function updateRowsCallback(row, data, dataIndex) {
        $(row).find('button[rel=archivar_informe]').on('click', function (event) {
            let parameters = new FormData();
            parameters.append("action", "archivar_informe");
            parameters.append("informe_id", data.id);
            parameters.append("csrfmiddlewaretoken", getCookie("csrftoken"));
            submit_with_ajax(
                window.location.pathname, parameters
                , 'Confirmación'
                , `¿Estas seguro de realizar la siguiente acción? Una vez archivado, 
                ya no podra realizar operaciones de edicción o eliminación del informe`
                , function (data) {
                    get_list_data_ajax_loading(window.location.pathname, data, function (response) {
                        tblistado.clear();
                        tblistado.rows.add(response).draw();
                    });
                }, function () {
                    disableEnableForm(form, false);
                }
            );
        });
        $(row).find('button[rel=ver_detalles]').on('click', function (event) {
            $("#frmverdetalles").find('input[name=id_informe]').val(data.id);
            updatetbDetallesInforme(data.id);
        });
    }

    function updatetbDetallesInforme(informe_id) {
        get_list_data_ajax_loading(window.location.pathname, {'action': 'informe_detail', 'informe_id': informe_id}
            , function (res_data) {
                tbdetalleinforme.clear();
                tbdetalleinforme.rows.add(res_data).draw();
                $("#modalverdetalles").modal("show");
            });
    }

    // Add event listener for opening and closing details
    addEventListenerOpenDetailRowDatatable('tbdetallesinforme', tblistado, 'td.details-control',
        function (row, data, dataIndex) {
            updateRowsCallbackDetalles(row, data, dataIndex);
        });

    function updateRowsCallbackDetalles(row, data, dataIndex) {
        $(row).find('button[rel=ver_desglose]').on('click', function (event) {
            $("#frmDetalleConsumoSustanciaInforme").find('input[name=id_detalle]').val(data.id);
            updatetbDesglosesInforme(data.id);
        });
    }

    $("#frmDetalleConsumoSustanciaInforme").find('button[rel=add_consumo]').remove()

    $("#frmDetalleConsumoSustanciaInforme").find('button[rel=btnSync]').on('click', function (evt) {
        let id_detalle = $("#frmDetalleConsumoSustanciaInforme").find('input[name=id_detalle]').val();
        updatetbDetallesInforme(id_detalle);
    });

    function updatetbDesglosesInforme(detalle_id) {
        get_list_data_ajax_loading('/informes-mensuales/desglose-sustancia/', {
                'action': 'search_desglose_sustancia',
                'detalle_informe_id': detalle_id
            }
            , function (res_data) {
                tbdesglosedetalleinforme.clear();
                tbdesglosedetalleinforme.rows.add(res_data).draw();
                $("#modalDetalleConsumoSustanciaInforme").modal("show");
            });
    }
});