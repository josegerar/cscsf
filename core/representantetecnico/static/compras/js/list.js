$(function () {
    const tblistado = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': true,
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
            {'data': 'observacion'},
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
                        return "Registrado"
                    } else if (data === 'almacenado') {
                        return "Almacenado"
                    } else if (data === 'revision') {
                        return '<label class="btn-danger">Revisión</label>'
                    } else {
                        return ""
                    }
                }
            },
            {
                'targets': [7],
                'render': function (data, type, row) {
                    return '<a class="nav-link" style="text-align: center; cursor: pointer;" rel="openobs">Ver</a>'
                }
            },
            {
                'targets': [8],
                'render': function (data, type, row) {
                    if (data === "almacenado") {
                        return ""
                    } else {
                        return '<a href="/compras/update/' + row.id + '/" class="btn btn-primary"><i class="fas fa-edit"></i></a> ';
                    }
                }
            },
            {
                'targets': [9],
                'render': function (data, type, row) {
                    if (data === "almacenado") {
                        return ""
                    } else {
                        return '<a href="/compras/delete/' + row.id + '/" type="button" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a>';
                    }
                }
            }
        ],
        'rowCallback': function (row, data, displayNum, displayIndex, dataIndex) {
            updateRowsCallback(row, data, dataIndex)
        }
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
        $(row).find('a[rel=openobs]').on('click', function (event) {
            $('#frmModalObs').find('textarea[name=observacion]').text(data.observacion);
            $('#modalObs').modal('show');
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