$(function () {
    const tblistado = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': true,
        'columns': [
            {'data': 'id'},
            {'data': 'nombre'},
            {'data': 'dir'},
            {'data': 'responsable'}
        ]
    });

    get_list_data_ajax_loading(window.location.pathname, {'action': 'searchdata', 'type': 'bdg'}
        , function (response) {
            tblistado.clear();
            tblistado.rows.add(response).draw();
        });

    $('button[rel=btnSync]').on('click', function (event) {
        get_list_data_ajax_loading(window.location.pathname, {'action': 'searchdata', 'type': 'bdg'}
            , function (response) {
                tblistado.clear();
                tblistado.rows.add(response).draw();
            });
    });
});