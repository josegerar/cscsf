$(function () {
    const data = {'action': 'searchdata', 'csrfmiddlewaretoken': getCookie("csrftoken")};

    const tbstock = $('#tbstock').DataTable({
        'responsive': true,
        'autoWidth': false,
        'destroy': true,
        'paging': false,
        'searching': false,
        'ordering': false,
        'columns': [
            {'data': 'cantidad'},
            {'data': 'cantidad'},
            {'data': 'cantidad'}
        ],
        'columnDefs': [
            {
                'targets': [0],
                'render': function (data, type, row) {
                    if (row.bodega) {
                        return "bodega";
                    } else if (row.laboratorio) {
                        return "laboratorio";
                    } else {
                        return "";
                    }
                }
            },
            {
                'targets': [1],
                'render': function (data, type, row) {
                    if (row.bodega) {
                        return row.bodega.nombre;
                    } else if (row.laboratorio.id) {
                        return row.laboratorio.nombre;
                    } else {
                        return "";
                    }
                }
            }
        ]
    });

    const tblistado = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': false,
        'destroy': true,
        'columns': [
            {
                "className": 'details-control',
                'data': 'id'
            },
            {'data': 'nombre'},
            {'data': 'descripcion'},
            {'data': 'cupo_autorizado'},
            {'data': 'unidad_medida.nombre'},
            {'data': 'id'},
            {'data': 'id'}
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
                'orderable': false,
                'render': function (data, type, row) {
                    return '<a rel="viewstocksubstance" class="btn btn-info"><i class="fas fa-eye"></i></a> ';
                }
            },
            {
                'targets': [6],
                'orderable': false,
                'render': function (data, type, row) {
                    let buttons = '<a href="/sustancias/update/' + row.id + '/" class="btn btn-primary"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/sustancias/delete/' + row.id + '/" type="button" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            }
        ],
        'rowCallback': function (row, data, displayNum, displayIndex, dataIndex) {
            updateRowsCallback(row, data, dataIndex);
        }
    });

    // Add event listener for opening and closing details
    addEventListenerOpenDetailRowDatatable('tblistado', tblistado, 'td.details-control',
        function (row, data, dataIndex) {
            updateRowsCallback(row, data, dataIndex);
        });

    update_datatable(tblistado, window.location.pathname, data);

    $('#btnSync').on('click', function (event) {
        update_datatable(tblistado, window.location.pathname, data);
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
            activeSelectionRowDatatable(row, tblistado);
            update_cantiad_total(data.stock);
            tbstock.clear();
            tbstock.rows.add(data.stock).draw();
        });
        $(row).find('a[rel=ver_observacion]').on('click', function (event) {
            verObservacion(`Descripcion de la sustancia ${data.nombre}`, data.descripcion, "Descripción:");
        });
    }
});