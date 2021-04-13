$(function () {
    const tblistado = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': true,
        'destroy': true,
        'deferRender': true,
        'processing': true,
        'ajax': {
            'url': window.location.pathname,
            'type': 'GET',
            'data': function (d) {
                d.action = 'searchdata';
            },
            'dataSrc': ''
        },
        'columns': [
            {'data': 'id'},
            {'data': 'nombre'},
            {'data': 'ruc'},
            {'data': 'id'},
            {'data': 'id_del'}
        ],
        'columnDefs': [
            {
                'targets': [3],
                'render': function (data, type, row) {
                    return '<a href="/empresas/update/' + row.id + '/" class="btn btn-primary"><i class="fas fa-edit"></i></a> ';
                }
            },
            {
                'targets': [4],
                'render': function (data, type, row) {
                    if (data) return '<a href="/empresas/delete/' + row.id + '/" type="button" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a>';
                    return "";
                }
            }
        ]
    });

    $('#btnSync').on('click', function (event) {
        tblistado.ajax.reload();
    });
});