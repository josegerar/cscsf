$(function () {
    const tblistado = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': true,
        'columns': [
            {
                "className": 'details-control',
                'data': 'id'
            },
            {'data': 'nombre'},
            {'data': 'apellido'},
            {'data': 'cedula'},
            {'data': 'tipo'},
            {'data': 'id'},
            {'data': 'id'},
        ],
        'columnDefs': [
            {
                'targets': [4],
                'orderable': false,
                'render': function (data, type, row) {
                    return '<button type="button" rel="ver_usuarios" class="btn btn-success btn-flat" >Ver</button>';
                }
            },
            {
                'targets': [5],
                'orderable': false,
                'render': function (data, type, row) {
                    return '<a href="/personas/update/' + row.id + '/" class="btn btn-primary"><i class="fas fa-edit"></i></a> ';
                }
            },
            {
                'targets': [6],
                'orderable': false,
                'render': function (data, type, row) {
                    if (row.is_del) {
                        return '<a href="/personas/delete/' + row.id + '/" type="button" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a>';
                    }
                    return ""
                }
            }
        ],
        'rowCallback': function (row, data, displayNum, displayIndex, dataIndex) {
            updateRowsCallback(row, data, dataIndex);
        }
    });

    const tbverusuarios = $('#tbverusuarios').DataTable({
        'responsive': true,
        'autoWidth': true,
        'ordering': false,
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

    get_list_data_ajax_loading(window.location.pathname, {'action': 'searchdata', 'type': 'rt'}
        , function (response) {
            tblistado.clear();
            tblistado.rows.add(response).draw();
        });

    $('#btnSync').on('click', function (event) {
        get_list_data_ajax_loading(window.location.pathname, {'action': 'searchdata', 'type': 'rt'}
            , function (response) {
                tblistado.clear();
                tblistado.rows.add(response).draw();
            });
    });

    // Add event listener for opening and closing details
    addEventListenerOpenDetailRowDatatable('tblistado', tblistado, 'td.details-control',
        function (row, data, dataIndex) {
            updateRowsCallback(row, data, dataIndex);
        });

    function updateRowsCallback(row, data, dataIndex) {
        $(row).find('button[rel=ver_usuarios]').on('click', function (event) {
            get_list_data_ajax_loading(window.location.pathname, {
                    'action': 'search_user_person',
                    'person_id': data.id
                }
                , function (res_data) {
                    tbverusuarios.clear();
                    tbverusuarios.rows.add(res_data).draw();
                    $("#modalverusuarios").find('input[name=nombres_completos]').val(`${data.nombre} ${data.apellido}`);
                    $("#modalverusuarios").modal("show");
                });
        });
    }
});