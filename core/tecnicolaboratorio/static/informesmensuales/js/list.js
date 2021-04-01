$(function () {
    const data = {'action': 'searchdata'}
    const tblistado = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': false,
        'destroy': true,
        'columns': [
            {
                "className": 'details-control',
                'data': 'id'
            },
            {'data': 'laboratorio'},
            {'data': 'mes'},
            {'data': 'year'},
            {'data': 'id'},
            {'data': 'id'},
            {'data': 'id'},
            {'data': 'id'}
        ],
        'columnDefs': [
            {
                'targets': [4],
                'orderable': false,
                'render': function (data, type, row) {
                    return '<button rel="ver_detalles" class="btn btn-success btn-flat" >Ver</button>'
                }
            },
            {
                'targets': [5],
                'orderable': false,
                'render': function (data, type, row) {
                    if (row.is_editable) {
                        return '<button rel="archivar_informe" class="btn btn-secondary btn-flat" > <i class="fas fa-archive"></i></button> ';
                    }
                    return "Informe archivado";
                }
            },
            {
                'targets': [6],
                'orderable': false,
                'render': function (data, type, row) {
                    if (row.is_editable) {
                        return '<a href="/informes-mensuales/update/' + row.id + '/" class="btn btn-primary btn-flat"><i class="fas fa-edit"></i></a> ';
                    }
                    return "";
                }
            },
            {
                'targets': [7],
                'orderable': false,
                'render': function (data, type, row) {
                    if (row.is_editable) {
                        return '<a href="/informes-mensuales/delete/' + row.id + '/" class="btn btn-danger btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    }
                    return "";
                }
            }
        ],
        'rowCallback': function (row, data, displayNum, displayIndex, dataIndex) {
            updateRowsCallback(row, data, dataIndex)
        }
    });

    get_list_data_ajax_loading(window.location.pathname, data, function (response) {
        if (response.length > 0) {
            tblistado.clear();
            tblistado.rows.add(response).draw();
        }
    });

    function updateRowsCallback(row, data, dataIndex) {
        $(row).find('button[rel=archivar_informe]').on('click', function (event) {
            let parameters = new FormData();
            parameters.append("action", "archivar_informe");
            parameters.append("informe_id", data.id);
            parameters.append("csrfmiddlewaretoken", getCookie("csrftoken"));
            submit_with_ajax(
                window.location.pathname, parameters
                , 'Confirmación'
                , `¿Estas seguro de realizar la siguiente acción? Una vez archivado, 
                ya no podra realizar operaciones de edicción o eliminación del informe`
                , function (data) {
                    get_list_data_ajax_loading(window.location.pathname, data, function (response) {
                        if (response.length > 0) {
                            tblistado.clear();
                            tblistado.rows.add(response).draw();
                        }
                    });
                }, function () {
                    disableEnableForm(form, false);
                }
            );
        });
    }
});