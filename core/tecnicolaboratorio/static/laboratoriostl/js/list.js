$(function () {
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
                d.action = 'searchdata';
            },
            'dataSrc': ''
        },
        'columns': [
            {'data': 'id'},
            {'data': 'nombre'},
            {'data': 'dir'},
            {'data': 'responsable'},
        ]
    });

    $('#btnSync').on('click', function (event) {
        tblistado.ajax.reload();
    });
});