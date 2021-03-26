$(function () {
    const data = {'action': 'searchdata', 'csrfmiddlewaretoken': getCookie("csrftoken")}
    const tblistado = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': false,
        'destroy': true,
        'columns': [
            {'data': 'id'},
            {'data': 'nombre'},
            {'data': 'responsable'},
            {'data': 'id'}
        ],
        'columnDefs': [
            {
                'targets': [3],
                'orderable': false,
                'render': function (data, type, row) {
                    var buttons = '<a href="/laboratorios/update/' + row.id + '/" class="btn btn-primary"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/laboratorios/delete/' + row.id + '/" type="button" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a>';
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