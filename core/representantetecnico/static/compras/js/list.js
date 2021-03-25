$(function () {
    var csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken");
    var data = {'action': 'searchdata'}
    if (csrfmiddlewaretoken.length > 0) {
        data['csrfmiddlewaretoken'] = csrfmiddlewaretoken[0].value
    }
    var tblistado = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': false,
        'destroy': true,
        'columns': [
            {'data': 'id'},
            {'data': 'empresa.nombre'},
            {'data': 'llegada_bodega'},
            {'data': 'hora_llegada_bodega'},
            {'data': 'convocatoria'},
            {'data': 'pedido_compras_publicas'},
            {'data': 'guia_transporte'},
            {'data': 'factura'},
            {'data': 'estado'},
            {'data': 'observacion'},
            {'data': 'id'},
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
                        return "Registrado"
                    } else if (data.estado === 'almacenado') {
                        return "Almacenado"
                    } else if (data.estado === 'revision') {
                        return '<label class="btn-danger">Revisión</label>'
                    } else {
                        return ""
                    }
                }
            },
            {
                'targets': [9],
                'render': function (data, type, row) {
                    if (row.estado) {
                        if (row.estado.estado === 'revision') {
                            return '<a href="#" rel="openobs">Ver observación</a>'
                        }
                    }
                    return ""
                }
            },
            {
                'targets': [10],
                'orderable': false,
                'render': function (data, type, row) {
                    if (row.estado && row.estado.estado === "almacenado") {
                        return ""
                    } else {
                        let buttons = '<a href="/compras/update/' + row.id + '/" class="btn btn-primary"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="/compras/delete/' + row.id + '/" type="button" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a>';
                        return buttons
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


    function updateRowsCallback(row, data, dataIndex) {
        $(row).find('a[rel=openobs]').on('click', function (event) {
            $('#frmModalObs').find('textarea[name=observacion]').text(data.observacion);
            $('#modalObs').modal('show');
        });
    }
});