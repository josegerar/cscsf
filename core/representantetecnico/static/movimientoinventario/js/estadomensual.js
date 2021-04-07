$(function () {
    const tblistado = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': true,
        'columns': [
            {'data': 'id'},
            {'data': 'sustancia'},
            {'data': 'cantidad'},
            {'data': 'lugar'},
            {'data': 'nombre_lugar'}
        ]
    });

    get_list_data_ajax_loading(window.location.pathname
        , {'action': 'searchdata', 'type': 'rp_month', 'year': 0, 'mes': 0}
        , function (response) {
            tblistado.clear();
            tblistado.rows.add(response).draw();
        });

    active_events_filters(['action', 'type', 'year', 'mes'], function (data) {
        get_list_data_ajax_loading(window.location.pathname, data
            , function (response) {
                tblistado.clear();
                tblistado.rows.add(response).draw();
            });
    });
});