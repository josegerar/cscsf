$(function () {
    let data = {'id': 0, 'action': 'searchdata', 'type': 'todo'};
    const tblistado = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': true,
        'destroy': true,
        'deferRender': true,
        'ajax': {
            'url': window.location.pathname,
            'type': 'GET',
            'data': function (d) {
                d.action = data.action;
                d.id = data.id;
                d.type = data.type;
            },
            'dataSrc': ''
        },
        'columns': [
            {
                "className": 'details-control',
                'data': 'id'
            },
            {'data': 'empresa'},
            {'data': 'llegada_bodega'},
            {'data': 'hora_llegada_bodega'},
            {'data': 'convocatoria'},
            {'data': 'estado'},
            {'data': 'id'}
        ],
        'columnDefs': [
            {
                'targets': [5],
                'render': function (data, type, row) {
                    if (data === 'revision') {
                        return '<label class="btn-danger">Revisión</label>'
                    }
                    return data
                }
            },
            {
                'targets': [6],
                'render': function (data, type, row) {
                    return `<a target="_blank" href="/compras/view/${data}/" class="nav-link" style="cursor: pointer; text-align: center">Ver</a>`;
                }
            }
        ]
    });

    $('#btnSync').on('click', function (event) {
        data = {'id': 0, 'action': 'searchdata', 'type': 'todo'};
        tblistado.ajax.reload();
    });

    active_events_filters(['id', 'action', 'type'], function (data_send) {
        data = data_send;
        tblistado.ajax.reload();
    });
});