$(function () {
    $('#tbdetallesustancia').DataTable({
        'responsive': true,
        'autoWidth': true,
        'paging': false,
        'searching': false,
        'ordering': false,
        'info': false,
        'processing': true,
        'ajax': {
            'url': window.location.pathname,
            'type': 'GET',
            'data': function (d) {
                d.action = 'search_stock';
            },
            'dataSrc': ''
        },
        'columns': [
            {'data': 'id'},
            {'data': 'type'},
            {'data': 'nombre'},
            {'data': 'cantidad'}
        ]
    });
});