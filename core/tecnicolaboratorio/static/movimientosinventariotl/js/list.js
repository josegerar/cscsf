$(function () {
    const tblistado = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': true,
        'columns': [
            {'data': 'id'},
            {'data': 'sustancia'},
            {'data': 'cantidad'},
            {'data': 'mes'},
            {'data': 'year'},
            {'data': 'lugar'},
            {'data': 'nom_lug'},
            {'data': 'un_med'},
        ]
    });

    get_list_data_ajax_loading(window.location.pathname, {'action': 'searchdata', 'type': 'lab'}
        , function (response) {
            tblistado.clear();
            tblistado.rows.add(response).draw();
        });
});