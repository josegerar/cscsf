$(function () {
    let data = {'action': 'searchdata', 'type': 'month', 'year': 0, 'mes': 0};
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
                d.mes = data.mes;
                d.type = data.type;
            },
            'dataSrc': ''
        },
        'columns': [
            {'data': 'id'},
            {'data': 'sustancia'},
            {'data': 'cantidad'},
            {'data': 'lugar'},
            {'data': 'nombre_lugar'}
        ]
    });

    $('button[rel=btnSync]').on('click', function (event) {
        data = {'action': 'searchdata', 'type': 'month', 'year': 0, 'mes': 0};
        tblistado.ajax.reload();
    });

    active_events_filters(['action', 'type', 'year', 'mes'], function (data_send) {
        data = data_send;
        tblistado.ajax.reload();
    });
});