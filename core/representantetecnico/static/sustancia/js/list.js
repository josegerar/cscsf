$(function () {
    const tbstock = $('#tbstock').DataTable({
        'responsive': true,
        'autoWidth': true,
        'paging': false,
        'searching': false,
        'ordering': false,
        'columns': [
            {'data': 'id'},
            {'data': 'type'},
            {'data': 'nombre'},
            {'data': 'cantidad'}
        ]
    });

    const tblistado = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': true,
        'destroy': true,
        'columns': [
            {
                "className": 'details-control',
                'data': 'id'
            },
            {'data': 'nombre'},
            {'data': 'descripcion'},
            {'data': 'cupo_autorizado'},
            {'data': 'unidad_medida'},
            {'data': 'id'},
            {'data': 'id'},
            {'data': 'is_del'}
        ],
        'columnDefs': [
            {
                'targets': [2],
                'render': function (data, type, row) {
                    return '<a rel="ver_observacion" class="btn btn-info"><i class="fas fa-eye"></i></a> '
                }
            },
            {
                'targets': [5],
                'render': function (data, type, row) {
                    return '<a rel="viewstocksubstance" class="btn btn-info"><i class="fas fa-eye"></i></a> ';
                }
            },
            {
                'targets': [6],
                'render': function (data, type, row) {
                    return '<a href="/sustancias/update/' + row.id + '/" class="btn btn-primary"><i class="fas fa-edit"></i></a> ';
                }
            },
            {
                'targets': [7],
                'render': function (data, type, row) {
                    if (data) return '<a href="/sustancias/delete/' + row.id + '/" type="button" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a>';
                    else return "";
                }
            }
        ],
        'rowCallback': function (row, data, displayNum, displayIndex, dataIndex) {
            updateRowsCallback(row, data, dataIndex);
        }
    });

    get_list_data_ajax_loading(window.location.pathname, {'action': 'searchdata'}
        , function (response) {
            tblistado.clear();
            tblistado.rows.add(response).draw();
        });

    active_events_filters(['id', 'action', 'type'], function (data) {
        get_list_data_ajax_loading(window.location.pathname, data
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

    $('#btnSync').on('click', function (event) {
        get_list_data_ajax_loading(window.location.pathname, {'action': 'searchdata'}
            , function (response) {
                tblistado.clear();
                tblistado.rows.add(response).draw();
            });
    });

    function update_cantiad_total_stock(stock = []) {
        setTimeout(() => {
            let cantidad = 0;
            $.each(stock, function (index, item) {
                cantidad += parseFloat(item.cantidad);
            });
            $('#id_cantidad_total').val(cantidad.toFixed(4));
        }, 1);
    }

    function updateRowsCallback(row, data, dataIndex) {
        $(row).find('a[rel=viewstocksubstance]').on('click', function (event) {
            get_list_data_ajax_loading(window.location.pathname, {
                    'action': 'search_stock',
                    'id_s': data.id,
                    'type': 'rt'
                }
                , function (response) {
                    console.log(response)
                    activeSelectionRowDatatable(row, tblistado);
                    update_cantiad_total_stock(response, "#id_cantidad_total")
                    tbstock.clear();
                    tbstock.rows.add(response).draw();
                    $("#modalstock").modal("show");
                });
        });
        $(row).find('a[rel=ver_observacion]').on('click', function (event) {
            verObservacion(`Descripcion de la sustancia ${data.nombre}`, data.descripcion, "Descripción:");
        });
    }
});