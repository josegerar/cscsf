$(function () {
    var csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken");
    var data = {'action': 'searchdata'}
    if (csrfmiddlewaretoken.length > 0) {
        data['csrfmiddlewaretoken'] = csrfmiddlewaretoken[0].value
    }
    var tbdetallecompra = $('#tbdetallecompra').DataTable({
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

    var tblistado = $('#tblistado').DataTable({
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
                    if (data.estado == 'registrado') {
                        var buttons = '<button rel="confirmarCompra" class="btn btn-dark btn-flat btn-sm"> <i class="fas fa-save"></i> Confirmar</button>';
                        return buttons
                    } else if (data.estado == 'almacenado') {
                        return "Almacenado"
                    } else if (data.estado == 'revision') {
                        return '<label class="btn-danger">Revisión</label>'
                    } else {
                        return ""
                    }
                }
            }
        ],
        'rowCallback': function (row, data, displayNum, displayIndex, dataIndex) {
            updateRowsCallback(row,data,dataIndex)
        }
    });

    update_datatable(tblistado, window.location.pathname, data);

    $('#btnSync').on('click', function (event) {
        update_datatable(tblistado, window.location.pathname, data);
    });
    $('#frmconfirmarcompra').on('submit', function (event) {
        event.preventDefault();
        let action_save = $(event.originalEvent.submitter).attr('rel');
        console.log(action_save);
        let form = this;
        let parameters = new FormData(form);
        if (action_save == 'confirmar'){
            parameters.append('action','confirmarCompra');
        } else if(action_save == 'revisar'){
            parameters.append('action','revisionCompra');
        }
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

        // Add event listener for opening and closing details
    $('#tblistado tbody').on('click', 'td.details-control', function () {
        let tr = $(this).closest('tr');
        let row = tblistado.row(tr);
        let child = row.child();
        let data = row.data();
        if (child) {
            updateRowsCallback(child, data, row.index());
        }
    });

    function updateRowsCallback(row, data, dataIndex) {
        $(row).find('button[rel="confirmarCompra"]').on('click', function (event) {
            $('#modalConfirmarCompra').find('input[name=id_compra]').val(data.id);
            tbdetallecompra.clear();
            tbdetallecompra.rows.add(data.detallecompra).draw();
            $('#modalConfirmarCompra').modal('show');
        });
    }
});
