$(function () {
    var csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken");
    var data = {'action': 'searchdata'}
    if (csrfmiddlewaretoken.length > 0) {
        data['csrfmiddlewaretoken'] = csrfmiddlewaretoken[0].value
    }

    var tbstock = $('#tbstock').DataTable({
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
                    if (row.bodega.id !== null) {
                        return "bodega";
                    } else if (row.laboratorio.id !== null) {
                        return "laboratorio";
                    } else {
                        return "";
                    }
                }
            },
            {
                'targets': [1],
                'render': function (data, type, row) {
                    if (row.bodega.id !== null) {
                        return row.bodega.nombre;
                    } else if (row.laboratorio.id !== null) {
                        return row.laboratorio.nombre;
                    } else {
                        return "";
                    }
                }
            }
        ]
    });

    var tblistado = $('#tblistado').DataTable({
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
            {'data': 'id'}
        ],
        'columnDefs': [
            {
                'targets': [5],
                'orderable': false,
                'render': function (data, type, row) {
                    let buttons = '<a rel="viewstocksubstance" class="btn btn-success"><i class="fas fa-eye"></i></a> ';
                    buttons += '<a href="/sustancias/update/' + row.id + '/" class="btn btn-primary"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/sustancias/delete/' + row.id + '/" type="button" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a>';
                    return buttons
                }
            }
        ],
        'rowCallback': function (row, data, displayNum, displayIndex, dataIndex) {
            updateRowsCallback(row, data, dataIndex);
        }
    });

    // Add event listener for opening and closing details
    $('#tblistado tbody').on('click', 'td.details-control', function () {
        let tr = $(this).closest('tr');
        let row = tblistado.row(tr);
        let child = row.child();
        let data = row.data();
        if (child) {
            updateRowsCallback(child, data, row.index());
        }
    });

    update_datatable(tblistado, window.location.pathname, data);

    $('#btnSync').on('click', function (event) {
        tbstock.clear();
        update_datatable(tblistado, window.location.pathname, data);
    });

    function updateRowsCallback(row, data, dataIndex) {
        $(row).find('a[rel=viewstocksubstance]').on('click', function (event) {
            tbstock.clear();
            tbstock.rows.add(data.stock).draw();
        });
    }

});