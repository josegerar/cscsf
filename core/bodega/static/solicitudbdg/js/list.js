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
            {'data': 'solicitante'},
            {'data': 'laboratorio'},
            {'data': 'nombre_actividad'},
            {'data': 'codigo'},
            {'data': 'estado'},
            {'data': 'fecha_autorizacion'},
            {'data': 'id'}
        ],
        'columnDefs': [
            {
                'targets': [5],
                'render': function (data, type, row) {
                    if (data === 'revision') {
                        return `<label class="btn-danger">${data}</label>`
                    }
                    return data;
                }
            },
            {
                'targets': [7],
                'render': function (data, type, row) {
                    return `<a target="_blank" href="/solicitudes/view/${data}" class="nav-link" style="cursor: pointer; text-align: center">Ver</a>`;
                }
            }
        ]
    });

    active_events_filters(['id', 'action', 'type'], function (data_send) {
        data = data_send;
        tblistado.ajax.reload();
    });


    $('#btnSync').on('click', function (event) {
        data = {'id': 0, 'action': 'searchdata', 'type': 'todo'};
        tblistado.ajax.reload();
    });
});