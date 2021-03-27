const solicitud_entrega = {
    data: {
        detalles: []
    },
    datatable: null,
    add_detalles: function (detalles) {
        this.data.detalles = detalles;
        this.config_items();
        this.list_detalles();
    },
    config_items: function () {
        $.each(this.data.detalles, function (index, item) {
            if (!item.cantidad_entregada || parseFloat(item.cantidad_entregada) <= 0) item.cantidad_entregada = 0;
            if (!item.cantidad_solicitada || parseFloat(item.cantidad_solicitada) <= 0) item.cantidad_solicitada = 0;
        });
    },
    format_data_send: function () {
        let data = []
        $.each(this.data.detalles, function (index, item) {
            data.push({'id': item.id, 'cantidad_entrega': item.cantidad_entregada});
        });
        return data;
    },
    list_detalles: function () {
        this.datatable.clear();
        this.datatable.rows.add(this.data.detalles).draw();
    },
    update_cantidad_entrega: function (nueva_cantidad, index) {
        this.data.detalles[index].cantidad_entregada = nueva_cantidad;
    }
}

$(function () {
    const data = {'action': 'searchdata', 'csrfmiddlewaretoken': getCookie("csrftoken")};
    solicitud_entrega.datatable = $('#tbdetallesolicitud').DataTable({
        'responsive': true,
        'autoWidth': false,
        'destroy': true,
        'columns': [
            {
                "className": 'details-control',
                'data': 'id'
            },
            {'data': 'stock.sustancia.nombre'},
            {'data': 'cantidad_solicitada'},
            {'data': 'cantidad_entregada'},
            {'data': 'stock.cantidad'}
        ],
        'columnDefs': [
            {
                'targets': [3],
                'orderable': false,
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
            {'data': 'estado_solicitud.estado'}
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
        if (action_save === 'entregar') {
            $('#frmSendObs').find('h5').text("Entregar sustancia")
            $('#frmSendObs').find('button[rel=btnEnviarObs]').text("Entregar")
            $('#frmSendObs').find('button[rel=btnEnviarObs]').attr("class", "btn btn-primary")
            $('#frmSendObs').find('input[name="id"]').val(parameters.get("id_solicitud"))
            $('#frmSendObs').find('input[name="action"]').val("entregarSolicitud")
            $('#modalSendObs').modal('show');
        } else if (action_save === 'revisar') {
            $('#frmSendObs').find('h5').text("Justificaciòn de revisiòn")
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
        parameters.append("detalles", JSON.stringify(solicitud_entrega.format_data_send()));
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
            $('#modalEntregaSustancia').find('input[name=id_solicitud]').val(data.id);
            solicitud_entrega.add_detalles(data.detallesolicitud);
            $('#modalEntregaSustancia').modal('show');
        });
    }

    // Add event listener for opening and closing details
    addEventListenerOpenDetailRowDatatable('tbdetallesolicitud', tblistado, 'td.details-control',
        function (row, data, dataIndex) {
            updateRowsCallbackDetalle(row, data, dataIndex);
        });

    function updateRowsCallbackDetalle(row, data, dataIndex) {
        activePluguinTouchSpinInputRow(row, 'cantidad', parseFloat(data.stock.cantidad),
            0, 0, 0.1);
        $(row).find('input[name="cantidad"]').on('change', function (event) {
            let nueva_cantidad = parseFloat($(this).val());
            solicitud_entrega.update_cantidad_entrega(nueva_cantidad, dataIndex);
        });
    }
});