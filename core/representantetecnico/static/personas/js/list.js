function format(d) {
    // `d` is the original data object for the row
    return `<table class="table table-sm table-active" id="tbusersperson${d.id}" style="font-size: 0.95rem; text-align: center; width: 100%">
                <thead class="">
                <tr>
                    <th scope="col">#</th>
                    <th scope="col">Correo</th>
                    <th scope="col">Rol</th>
                    <th scope="col">Estado</th>
                </thead>
                <tbody>
                </tbody>
            </table>`;
}

function activate_datatable_users(data) {
    $(`#tbusersperson${data.id}`).DataTable({
        'responsive': true,
        'autoWidth': true,
        'destroy': true,
        'deferRender': true,
        'paging': false,
        'searching': false,
        'ordering': false,
        'info': false,
        'processing': true,
        'ajax': {
            'url': window.location.pathname,
            'type': 'GET',
            'data': function (d) {
                d.action = "search_user_person";
                d.person_id = data.id
            },
            'dataSrc': ''
        },
        'columns': [
            {'data': 'id'},
            {'data': 'email'},
            {'data': 'id'},
            {'data': 'is_act'},
        ],
        'columnDefs': [
            {
                'targets': [2],
                'render': function (data, type, row) {
                    if (row.is_rep) return "Representante tecnico"
                    else if (row.is_groc) return "Bodeguero"
                    else if (row.is_lab) return "Tecnico laboratorista"
                }
            },
            {
                'targets': [3],
                'orderable': false,
                'render': function (data, type, row) {
                    if (data) return "Activo";
                    else return "Inactivo"
                }
            }
        ]
    });
}

$(function () {
    const tblistado = $('#tblistado').DataTable({
        'scrollX': true,
        'autoWidth': false,
        'destroy': true,
        'deferRender': true,
        'processing': true,
        'ajax': {
            'url': window.location.pathname,
            'type': 'GET',
            'data': function (d) {
                d.action = "searchdata";
            },
            'dataSrc': ''
        },
        'columns': [
            {
                "className": 'details-control',
                "orderable": false,
                "data": null,
                "defaultContent": ''
            },
            {'data': 'nombre'},
            {'data': 'apellido'},
            {'data': 'cedula'},
            {'data': 'id'},
            {'data': 'id'}
        ],
        'columnDefs': [
            {
                'targets': [4],
                'orderable': false,
                'render': function (data, type, row) {
                    return '<a href="/personas/update/' + row.id + '/" class="btn btn-primary"><i class="fas fa-edit"></i></a> ';
                }
            },
            {
                'targets': [5],
                'orderable': false,
                'render': function (data, type, row) {
                    if (row.is_del) {
                        return '<a href="/personas/delete/' + row.id + '/" type="button" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a>';
                    }
                    return ""
                }
            }
        ]
    });

    $('#btnSync').on('click', function (event) {
        tblistado.ajax.reload();
    });

    // Add event listener for opening and closing details
    $('#tblistado tbody').on('click', 'td.details-control', function () {
        const tr = $(this).closest('tr');
        const row = tblistado.row(tr);
        if (row.child.isShown()) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        } else {
            // Open this row
            row.child(format(row.data())).show();
            tr.addClass('shown');
            activate_datatable_users(row.data());
        }
    });
});