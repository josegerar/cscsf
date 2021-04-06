$(function () {
    const tblistado = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': true,
        'columns': [
            {'data': 'id'},
            {'data': 'nombre'},
            {'data': 'dir'},
            {'data': 'responsable'},
            {'data': 'id'},
            {'data': 'is_del'}
        ],
        'columnDefs': [
            {
                'targets': [4],
                'orderable': false,
                'render': function (data, type, row) {
                    return '<a href="/bodegas/update/' + row.id + '/" class="btn btn-primary"><i class="fas fa-edit"></i></a> ';
                }
            },
            {
                'targets': [5],
                'orderable': false,
                'render': function (data, type, row) {
                    if (data) return '<a href="/bodegas/delete/' + row.id + '/" type="button" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a>';
                    else return ""
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
        get_list_data_ajax_loading(window.location.pathname, {'action': 'searchdata'}
            , function (response) {
                tblistado.clear();
                tblistado.rows.add(response).draw();
            });

    });
});