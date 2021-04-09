$(function () {
    const tblistado = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': true,
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