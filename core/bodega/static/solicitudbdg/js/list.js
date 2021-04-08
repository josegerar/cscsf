const solicitud_entrega = {
    data: {
        detalles: []
    },
    datatable: null,
    add_detalles: function (detalles) {
        this.data.detalles = detalles;
        this.list_detalles();
    },
    list_detalles: function () {
        this.datatable.clear();
        this.datatable.rows.add(this.data.detalles).draw();
    },
    update_cantidad_entrega: function (nueva_cantidad, index) {
        this.data.detalles[index].cant_ent = nueva_cantidad;
    }
}

$(function () {
    solicitud_entrega.datatable = $('#tbdetallesolicitudentrega').DataTable({
        'responsive': true,
        'autoWidth': true,
        'columns': [
            {
                "className": 'details-control',
                'data': 'id'
            },
            {'data': 'sustancia'},
            {'data': 'cant_sol'},
            {'data': 'cant_ent'},
            {'data': 'cant_bdg'}
        ],
        'columnDefs': [
            {
                'targets': [3],
                'render': function (data, type, row) {
                    return '<input value="' + data + '" type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off"/>';
                }
            }
        ],
        'rowCallback': function (row, data, displayNum, displayIndex, dataIndex) {
            updateRowsCallbackDetalle(row, data, dataIndex);
        }
    });

    const tblistado = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': true,
        'columns': [
            {
                "className": 'details-control',
                'data': 'id'
            },
            {'data': 'solicitante'},
            {'data': 'laboratorio'},
            {'data': 'nombre_actividad'},
            {'data': 'documento'},
            {'data': 'codigo'},
            {'data': 'estado'},
            {'data': 'id'}
        ],
        'columnDefs': [
            {
                'targets': [4],
                'orderable': false,
                'render': function (data, type, row) {
                    return get_tag_url_document(data, 'Ver')
                }
            },
            {
                'targets': [6],
                'orderable': false,
                'render': function (data, type, row) {
                    if (data === 'registrado') {
                        return "Registrado";
                    } else if (data === 'entregado') {
                        return "Entregado";
                    } else if (data === 'revision') {
                        return '<label class="btn-danger">Revisión</label>'
                    } else if (data === 'recibido') {
                        return "Recibido"
                    } else if (data === 'aprobado') {
                        return '<button rel="entregarSustancias" class="btn btn-dark btn-flat btn-sm"> <i class="fas fa-save"></i> Entregar</button>';
                    }
                    return data;
                }
            },
            {
                'targets': [7],
                'orderable': false,
                'render': function (data, type, row) {
                    return '<a rel="opendetail" class="nav-link" style="cursor: pointer; text-align: center">Ver</a>';
                }
            }
        ],
        'rowCallback': function (row, data, displayNum, displayIndex, dataIndex) {
            updateRowsCallback(row, data, dataIndex)
        }
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
        console.log(response);
        tblistado.clear();
        tblistado.rows.add(response).draw();
    });


    $('#btnSync').on('click', function (event) {
        get_list_data_ajax_loading(window.location.pathname, {'action': 'searchdata'}, function (response) {
            tblistado.clear();
            tblistado.rows.add(response).draw();
        });
    });

    $('#frmEntregaSustancia').on('submit', function (event) {
        event.preventDefault();
        let action_save = $(event.originalEvent.submitter).attr('rel');
        let form = this;
        let parameters = new FormData(form);
        if (action_save === 'entregar') {
            $('#frmSendObs').find('h5').text("Entregar sustancia")
            $('#frmSendObs').find('button[rel=btnEnviarObs]').text("Entregar")
            $('#frmSendObs').find('button[rel=btnEnviarObs]').attr("class", "btn btn-primary")
            $('#frmSendObs').find('input[name="id"]').val(parameters.get("id_solicitud"))
            $('#frmSendObs').find('input[name="action"]').val("entregarSolicitud")
            $('#modalSendObs').modal('show');
        } else if (action_save === 'revisar') {
            $('#frmSendObs').find('h5').text("Justificación de revisión")
            $('#frmSendObs').find('button[rel=btnEnviarObs]').text("Revisión")
            $('#frmSendObs').find('button[rel=btnEnviarObs]').attr("class", "btn btn-danger")
            $('#frmSendObs').find('input[name="id"]').val(parameters.get("id_solicitud"))
            $('#frmSendObs').find('input[name="action"]').val("revisionSolicitud")
            $('#modalSendObs').modal('show');
        }
    });

    $('#frmSendObs').on('submit', function (event) {
        event.preventDefault();
        let form = this;
        let parameters = new FormData(form);
        parameters.append("tipoobs", "bdg");
        if (parameters.get("action") === 'entregarSolicitud') {
            parameters.append("detalles", JSON.stringify(solicitud_entrega.data.detalles));
        }
        disableEnableForm(form, true);
        submit_with_ajax(
            window.location.pathname, parameters
            , 'Confirmación'
            , '¿Estas seguro de realizar la siguiente acción?'
            , function (data) {
                $('#modalEntregaSustancia').modal('hide');
                $('#modalSendObs').modal('hide');
                location.reload();
            }, function () {
                disableEnableForm(form, false);
            }
        );
    });

    // Add event listener for opening and closing details
    addEventListenerOpenDetailRowDatatable('tblistado', tblistado, 'td.details-control',
        function (row, data, dataIndex) {
            updateRowsCallback(row, data, dataIndex);
        });

    function updateRowsCallback(row, data, dataIndex) {
        $(row).find('button[rel=entregarSustancias]').on('click', function (event) {
            get_list_data_ajax_loading(window.location.pathname, {'action': 'search_detalle', 'id_sl': data.id}
                , function (response) {
                    $('#modalEntregaSustancia').find('input[name=id_solicitud]').val(data.id);
                    solicitud_entrega.add_detalles(response);
                    $('#modalEntregaSustancia').modal('show');
                });
        });

        $(row).find('a[rel=opendetail]').on('click', function (event) {
            get_list_data_ajax_loading(window.location.pathname, {'action': 'search_detalle', 'id_sl': data.id}
                , function (response) {
                    tbdetalles.clear();
                    tbdetalles.rows.add(response).draw();
                    $('#modalDetalleSolicitud').modal('show');
                });
        });
    }

    // Add event listener for opening and closing details
    addEventListenerOpenDetailRowDatatable('tbdetallesolicitud', solicitud_entrega.datatable, 'td.details-control',
        function (row, data, dataIndex) {
            updateRowsCallbackDetalle(row, data, dataIndex);
        });

    function updateRowsCallbackDetalle(row, data, dataIndex) {
        activePluguinTouchSpinInputRow(row, 'cantidad', parseFloat(data.cant_bdg),
            data.cant_sol, data.cant_sol, 0.1);
        $(row).find('input[name="cantidad"]').on('change', function (event) {
            let nueva_cantidad = parseFloat($(this).val());
            solicitud_entrega.update_cantidad_entrega(nueva_cantidad, dataIndex);
        });
        $(row).find('input[name="cantidad"]').trigger('change');
    }
});