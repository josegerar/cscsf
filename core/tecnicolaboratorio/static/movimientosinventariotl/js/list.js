$(function () {
    let data = {'action': 'searchdata', 'year': 0, 'sus_id': 0, 'mes': 0}
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
                d.action = data.action;
                d.year = data.year;
                d.sus_id = data.sus_id;
                d.mes = data.mes;
            },
            'dataSrc': ''
        },
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

    $('button[rel=btnSync]').on('click', function (event) {
        data = {'action': 'searchdata', 'year': 0, 'sus_id': 0, 'mes': 0}
        tblistado.ajax.reload();
    });

    active_events_filters(['action', 'year', 'sus_id', 'mes'], function (data_send) {
        data = data_send;
        tblistado.ajax.reload();
    });
});