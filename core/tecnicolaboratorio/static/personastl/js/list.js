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
            {'data': 'apellido'},
            {'data': 'cedula'},
            {'data': 'id'},
            {'data': 'id'}
        ],
        'columnDefs': [
            {
                'targets': [4],
                'orderable': false,
                'render': function (data, type, row) {
                    return '<a href="/personas/update/' + row.id + '/" class="btn btn-primary"><i class="fas fa-edit"></i></a> ';
                }
            },
            {
                'targets': [5],
                'orderable': false,
                'render': function (data, type, row) {
                    if (row.is_del) {
                        return '<a href="/personas/delete/' + row.id + '/" type="button" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a>';
                    }
                    return ""
                }
            }
        ]
    });

    $('#btnSync').on('click', function (event) {
        tblistado.ajax.reload();
    });
});