$(function () {
    var csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken");
    var data = {'action': 'searchdata'}
    if (csrfmiddlewaretoken.length > 0) {
        data['csrfmiddlewaretoken'] = csrfmiddlewaretoken[0].value
    }
    var tblistado = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': false,
        'destroy': true,
        'deferRender': true,
        'columns': [
            {'data': 'id'},
            {'data': 'tipo'},
            {'data': 'nombre'},
            {'data': 'apellido'},
            {'data': 'cedula'},
            {'data': 'tipo'}
        ],
        'columnDefs': [
            {
                'targets': [5],
                'orderable': false,
                'render': function (data, type, row) {
                    var buttons = '<a href="/personas/update/' + row.id + '/" class="btn btn-primary"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/personas/delete/' + row.id + '/" type="button" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a>';
                    return buttons
                }
            }
        ]
    });

    update_datatable(tblistado, window.location.pathname, data);

    $('#btnSync').on('click', function (event) {
        update_datatable(tblistado, window.location.pathname, data);
    });
});