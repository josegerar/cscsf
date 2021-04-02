$(function () {
    const tblistado = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': false,
        'destroy': true,
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

    get_list_data_ajax_loading(window.location.pathname, {'action': 'searchdata', 'type': 'lab'}
        , function (response) {
            tblistado.clear();
            tblistado.rows.add(response).draw();
        });

    $('#btnSync').on('click', function (event) {
        get_list_data_ajax_loading(window.location.pathname, {'action': 'searchdata', 'type': 'lab'}
            , function (response) {
                tblistado.clear();
                tblistado.rows.add(response).draw();
            });
    });
});