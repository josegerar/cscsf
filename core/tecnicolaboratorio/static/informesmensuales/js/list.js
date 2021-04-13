$(function () {
    let data = {'id': 0, 'action': 'searchdata', 'type': 'todo'};
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
                d.id = data.id;
                d.type = data.type;
            },
            'dataSrc': ''
        },
        'columns': [
            {'data': 'id'},
            {'data': 'laboratorio'},
            {'data': 'mes'},
            {'data': 'year'},
            {'data': 'fecha_creat'},
            {'data': 'estado'},
            {'data': 'id'}
        ],
        'columnDefs': [
            {
                'targets': [6],
                'render': function (data, type, row) {
                    return `<a target="_blank" href="/informes-mensuales/view/${data}/" class="nav-link" style="cursor: pointer; text-align: center">Ver</a>`;
                }
            }
        ]
    });

    $('button[rel=btnSync]').on('click', function (evt) {
        data = {'id': 0, 'action': 'searchdata', 'type': 'todo'};
        tblistado.ajax.reload();
    });

    active_events_filters(['id', 'action', 'type'], function (data_send) {
        data = data_send;
        tblistado.ajax.reload();
    });
});