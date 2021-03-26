$(function () {
    const data = {'action': 'searchdata', 'csrfmiddlewaretoken': getCookie("csrftoken")}

    const tbdetallecompra = $('#tbdetallecompra').DataTable({
        'responsive': true,
        'autoWidth': false,
        'destroy': true,
        'columns': [
            {'data': 'stock.bodega.nombre'},
            {'data': 'stock.sustancia.nombre'},
            {'data': 'cantidad'},
            {'data': 'stock.sustancia.cupo_autorizado'}
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
            {'data': 'empresa.nombre'},
            {'data': 'llegada_bodega'},
            {'data': 'hora_llegada_bodega'},
            {'data': 'convocatoria'},
            {'data': 'pedido_compras_publicas'},
            {'data': 'guia_transporte'},
            {'data': 'factura'},
            {'data': 'estado'},
        ],
        'columnDefs': [
            {
                'targets': [5],
                'orderable': false,
                'render': function (data, type, row) {
                    return get_tag_url_document(data, 'Ver pedido de compras publicas')
                }
            },
            {
                'targets': [6],
                'orderable': false,
                'render': function (data, type, row) {
                    return get_tag_url_document(data, 'Ver factura')
                }
            },
            {
                'targets': [7],
                'orderable': false,
                'render': function (data, type, row) {
                    return get_tag_url_document(data, 'Ver guia')
                }
            },
            {
                'targets': [8],
                'orderable': false,
                'render': function (data, type, row) {
                    if (data.estado === 'registrado') {
                        var buttons = '<button rel="confirmarCompra" class="btn btn-dark btn-flat btn-sm"> <i class="fas fa-save"></i> Confirmar</button>';
                        return buttons
                    } else if (data.estado === 'almacenado') {
                        return "Almacenado"
                    } else if (data.estado === 'revision') {
                        return '<label class="btn-danger">Revisión</label>'
                    } else {
                        return ""
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
    $('#frmconfirmarcompra').on('submit', function (event) {
        event.preventDefault();
        let action_save = $(event.originalEvent.submitter).attr('rel');
        let form = this;
        let parameters = new FormData(form);
        if (action_save === 'confirmar') {
            parameters.append('action', 'confirmarCompra');
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
            $('#frmSendObs').find('h5').text("Justificaciòn de revisiòn")
            $('#frmSendObs').find('button[rel=btnEnviarObs]').text("Revisión")
            $('#frmSendObs').find('button[rel=btnEnviarObs]').attr("class", "btn btn-danger")
            $('#frmSendObs').find('input[name="id"]').val(parameters.get("id_solicitud"))
            $('#frmSendObs').find('input[name="action"]').val("revisionSolicitud")
            $('#modalSendObs').modal('show');
        }
    });

    // Add event listener for opening and closing details
    addEventListenerOpenDetailRowDatatable('tblistado', tblistado, 'td.details-control',
        function (row, data, dataIndex) {
            updateRowsCallback(row, data, dataIndex);
        });

    $('#frmSendObs').on('submit', function (event) {
        event.preventDefault();
        let form = this;
        let parameters = new FormData(form);
        disableEnableForm(form, true);
        submit_with_ajax(
            window.location.pathname, parameters
            , 'Confirmación'
            , '¿Estas seguro de realizar la siguiente acción?'
            , function (data) {
                $('#modalConfirmarCompra').modal('hide');
                $('#modalSendObs').modal('hide');
                location.reload();
            }, function () {
                disableEnableForm(form, false);
            }
        );
    });

    function updateRowsCallback(row, data, dataIndex) {
        $(row).find('button[rel="confirmarCompra"]').on('click', function (event) {
            $('#modalConfirmarCompra').find('input[name=id_compra]').val(data.id);
            console.log(data)
            console.log("xni")
            tbdetallecompra.clear();
            tbdetallecompra.rows.add(data.detallecompra).draw();
            $('#modalConfirmarCompra').modal('show');
        });
    }
});
