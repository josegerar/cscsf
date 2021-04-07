$(function () {
    const tblistado = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': true,
        'columns': [
            {'data': 'id'},
            {'data': 'sustancia'},
            {'data': 'can_mov'},
            {'data': 'mov_type'},
            {'data': 'date_creation'},
            {'data': 'mes'},
            {'data': 'anio'},
            {'data': 'nombre_lugar'},
        ],
        'columnDefs': [
            {
                'targets': [3],
                'render': function (data, type, row) {
                    if (data === 'delete') return "Consumo"
                    else return "Ingreso"
                }
            },
        ]
    });

    get_list_data_ajax_loading(window.location.pathname
        , {'action': 'searchdata', 'type': 'bdg', 'year': 0, 'sus_id': 0, 'mes': 0}
        , function (response) {
            tblistado.clear();
            tblistado.rows.add(response).draw();
        });

    $('button[rel=btnSync]').on('click', function (event) {
        get_list_data_ajax_loading(window.location.pathname
            , {'action': 'searchdata', 'type': 'bdg', 'year': 0, 'sus_id': 0, 'mes': 0}
            , function (response) {
                tblistado.clear();
                tblistado.rows.add(response).draw();
            });
    });

    active_events_filters(['action', 'type', 'year', 'sus_id', 'mes'], function (data) {
        get_list_data_ajax_loading(window.location.pathname, data
            , function (response) {
                tblistado.clear();
                tblistado.rows.add(response).draw();
            });
    });
});