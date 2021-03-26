$(function () {
    const data = {'action': 'searchdata', 'csrfmiddlewaretoken': getCookie("csrftoken")}
    const tbroles = $('#tbroles').DataTable({
        'responsive': true,
        'autoWidth': false,
        'destroy': true,
        'columns': [
            {'data': 'id'},
            {'data': 'rol'},
            {'data': 'estado'},
            {'data': 'id'}
        ],
        'columnDefs': [
            {
                'targets': [2],
                'orderable': false,
                'render': function (data, type, row) {
                    return '<div class="form-group form-group-sm"><select name="lugar_ingreso" class="form-control-sm" style="width: 100%"> ' +
                        '<option value="value1">Representante Técnico </option>\n' +
                        '  <option value="value2" selected>Bodeguera/a</option>\n' +
                        '  <option value="value3">Técnico Laboratorista</option>' +
                        '</select></div>';
                    return combo
                }
            },
            {
                'targets': [3],
                'orderable': false,
                'render': function (data, type, row) {
                    var buttons = '<a href="/personas/update/' + row.id + '/" class="btn btn-primary"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/personas/delete/' + row.id + '/" type="button" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a>';
                    return buttons
                }
            }
        ]
    });

    update_datatable(tbroles, window.location.pathname, data);

    $('#btnSync').on('click', function (event) {
        update_datatable(tbroles, window.location.pathname, data);
    });
});