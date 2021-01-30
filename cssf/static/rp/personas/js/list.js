$(function () {
    $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': false,
        'destroy': true,
        'deferRender': true,
        'ajax': {
            'url': window.location.pathname,
            'type': 'POST',
            'data': {
                'action': 'searchdata'
            },
            'dataSrc': ''
        },
        'columns': [
            {'data': 'id'},
            {'data': 'tipo'},
            {'data': 'nombre'},
            {'data': 'apellido'},
            {'data': 'cedula'},
            {'data': 'tipo'}
        ],
        'columnDefs': [
            {
                'targets': [5],
                'orderable': false,
                'render': function (data, type, row) {
                    var buttons = '<a href="/rp/personas/update/' + row.id + '/" class="btn btn-primary"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/rp/personas/delete/' + row.id + '/" type="button" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a>';
                    return buttons
                }
            }
        ]
    });
});