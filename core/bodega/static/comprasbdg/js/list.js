$(function () {
    const data = {'action': 'searchdata', 'csrfmiddlewaretoken': getCookie("csrftoken")};

    const tblistado = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': true,
        'destroy': true,
        'columns': [
            {
                "className": 'details-control',
                'data': 'id'
            },
            {'data': 'empresa'},
            {'data': 'llegada_bodega'},
            {'data': 'hora_llegada_bodega'},
            {'data': 'convocatoria'},
            {'data': 'id'},
            {'data': 'estado'},
            {'data': 'estado'}
        ],
        'columnDefs': [
            {
                'targets': [5],
                'render': function (data, type, row) {
                    return '<a class="nav-link" style="text-align: center; cursor: pointer;" rel="opendocs">Ver</a>'
                }
            },
            {
                'targets': [6],
                'render': function (data, type, row) {
                    if (data === 'registrado') {
                        return "Registrado";
                    } else if (data === 'almacenado') {
                        return "Almacenado";
                    } else if (data === 'revision') {
                        return '<label class="btn-danger">Revisión</label>';
                    }
                    return "";
                }
            },
            {
                'targets': [7],
                'orderable': false,
                'render': function (data, type, row) {
                    if (data === 'registrado') {
                        return '<button rel="confirmarCompra" class="btn btn-dark btn-flat btn-sm"> <i class="fas fa-save"></i> Confirmar</button>'
                    }
                    return "";
                }
            }
        ],
        'rowCallback': function (row, data, displayNum, displayIndex, dataIndex) {
            updateRowsCallback(row, data, dataIndex)
        }
    });

    const tbdetallecompra = $('#tbdetallecompra').DataTable({
        'responsive': true,
        'autoWidth': true,
        'columns': [
            {'data': 'id'},
            {'data': 'stock.value'},
            {'data': 'stock.unidad_medida'},
            {'data': 'cantidad'},
            {'data': 'stock.cantidad_bodega'},
            {'data': 'stock.cupo_autorizado'}
        ]
    });

    const tbdocumentos = $('#tbdocumentos').DataTable({
        'responsive': true,
        'autoWidth': true,
        'paging': false,
        'searching': false,
        'ordering': false,
        "info": false,
        'columns': [
            {
                "className": 'details-control',
                'data': 'tipo'
            },
            {'data': 'documento'},
        ],
        'columnDefs': [
            {
                'targets': [1],
                'render': function (data, type, row) {
                    return get_tag_url_document(data, 'Ver')
                }
            }
        ]
    });

    get_list_data_ajax_loading(window.location.pathname, {'action': 'searchdata'}
        , function (response) {
            tblistado.clear();
            tblistado.rows.add(response).draw();
        });

    $('#btnSync').on('click', function (event) {
        get_list_data_ajax_loading(window.location.pathname, {'action': 'searchdata', 'type': 'bdg'}
            , function (response) {
                tblistado.clear();
                tblistado.rows.add(response).draw();
            });
    });

    active_events_filters(['id', 'action', 'type'], function (data) {
        get_list_data_ajax_loading(window.location.pathname, data
            , function (response) {
                tblistado.clear();
                tblistado.rows.add(response).draw();
            });
    });

    $('#frmconfirmarcompra').on('submit', function (event) {
        event.preventDefault();
        let action_save = $(event.originalEvent.submitter).attr('rel');
        let form = this;
        let parameters = new FormData(form);
        if (action_save === 'confirmar') {
            $('#frmSendObs').find('h5').text("Justificaciòn de confirmación")
            $('#frmSendObs').find('button[rel=btnEnviarObs]').text("Confirmar Compra")
            $('#frmSendObs').find('button[rel=btnEnviarObs]').attr("class", "btn btn-primary")
            $('#frmSendObs').find('input[name="id"]').val(parameters.get("id_compra"))
            $('#frmSendObs').find('input[name="action"]').val("confirmarCompra")
            $('#modalSendObs').modal('show');
        } else if (action_save === 'revisar') {
            $('#frmSendObs').find('h5').text("Justificación de revisión")
            $('#frmSendObs').find('button[rel=btnEnviarObs]').text("Revisión")
            $('#frmSendObs').find('button[rel=btnEnviarObs]').attr("class", "btn btn-danger")
            $('#frmSendObs').find('input[name="id"]').val(parameters.get("id_compra"))
            $('#frmSendObs').find('input[name="action"]').val("revisionCompra")
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
            get_list_data_ajax_loading(window.location.pathname, {'action': 'searchdetail', 'id_comp': data.id}
                , function (response) {
                    $('#modalConfirmarCompra').find('input[name=id_compra]').val(data.id);
                    tbdetallecompra.clear();
                    tbdetallecompra.rows.add(response).draw();
                    $('#modalConfirmarCompra').modal('show');
                });

        });

        $(row).find('a[rel=opendocs]').on('click', function (event) {
            let documentos = []
            documentos.push({'tipo': 'Factura', 'documento': data.factura});
            documentos.push({'tipo': 'Guia de transporte', 'documento': data.guia_transporte});
            documentos.push({'tipo': 'Pedidod de compras publicas', 'documento': data.pedido_compras_publicas});
            tbdocumentos.clear();
            tbdocumentos.rows.add(documentos).draw();
            $('#modaldocumentos').modal('show');
        });
    }
});
