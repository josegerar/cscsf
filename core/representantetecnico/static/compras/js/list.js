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
        'deferRender': true,
        'columns': [
            {'data': 'id'},
            {'data': 'empresa'},
            {'data': 'llegada_bodega'},
            {'data': 'hora_llegada_bodega'},
            {'data': 'convocatoria'},
            {'data': 'responsable_entrega'},
            {'data': 'transportista'},
            {'data': 'guia_transporte'},
            {'data': 'factura'},
            {'data': 'id'}
        ],
        'columnDefs': [
            {
                'targets': [7],
                'orderable': false,
                'render': function (data, type, row) {
                    return get_tag_url_document(data, 'Ver factura')
                }
            },
            {
                'targets': [8],
                'orderable': false,
                'render': function (data, type, row) {
                    return get_tag_url_document(data, 'Ver guia')
                }
            },
            {
                'targets': [9],
                'orderable': false,
                'render': function (data, type, row) {
                    var buttons = '<a href="/compras/update/' + row.id + '/" class="btn btn-primary"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/compras/delete/' + row.id + '/" type="button" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a>';
                    return buttons
                }
            }
        ]
    });

    update_datatable(tblistado, window.location.pathname, data);

    $('#btnSync').on('click', function (event) {
        update_datatable(tblistado, window.location.pathname, data);
    });
});