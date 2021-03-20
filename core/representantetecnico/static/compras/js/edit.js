const compra = {
    datatable: null,
    data: {
        sustancias: []
    },
    add_sustancia: function (item) {
        item = this.config_item(item);
        if (item.cantidad_ingreso + item.cantidad > item.cupo_autorizado) {
            message_error("La sustancia " + item.nombre
                + " ha alcanzado su limite de cupo autorizado \n no se puede ingresar");
        } else {
            this.data.sustancias.push(item);
        }
        this.list_sustancia();
    },
    config_item: function (item) {
        let cant = 0;
        $.each(item.stock, function (istock, vstock) {
            if (vstock.bodega.id) vstock.text = "Bod. " + vstock.bodega.nombre;
            else vstock.text = "Lab. " + vstock.laboratorio.nombre;
            cant += parseFloat(vstock.cantidad);
        });
        item.cantidad_ingreso = 0.0001;
        item.cupo_autorizado = parseFloat(item.cupo_autorizado);
        item.cantidad = cant.toFixed(4);
        item.stock_selected = null;
        return item;
    },
    get_stock_item: function (dataIndex) {
        let stock = [];
        $.each(this.data.sustancias[dataIndex].stock, function (istock, vstock) {
            if (vstock.bodega.id) stock.push(vstock);
        });
        return stock;
    },
    list_sustancia: function () {
        this.datatable.clear();
        this.datatable.rows.add(this.data.sustancias).draw();
    },
    update_cantidad_sustancia: function (nueva_cantidad, index) {
        this.data.sustancias[index].cantidad_ingreso = nueva_cantidad;
    },
    delete_sustancia: function (index) {
        this.data.sustancias.splice(index, 1);
        this.list_sustancia();
    },
    delete_all_sustancias: function () {
        if (this.data.sustancias.length === 0) return false;
        confirm_action(
            'Alerta',
            '¿Esta seguro de eliminar todas las sustancias del detalle?',
            function () {
                compra.data.sustancias = [];
                compra.list_sustancia();
            }
        );
    },
    verify_send_data: function (callback, error) {
        if (this.data.sustancias.length === 0) {
            error();
        } else {
            callback();
        }
    },
    set_stock_selected: function (dataIndex, idStock) {
        $.each(this.data.sustancias[dataIndex].stock, function (istock, vstock) {
            if (vstock.id === idStock) {
                compra.data.sustancias[dataIndex].stock_selected = vstock;
            }
        });
    }
};

$(function () {

    const csrfmiddlewaretoken = getCookie('csrftoken');
    var data = {'action': 'searchdetail', 'csrfmiddlewaretoken': csrfmiddlewaretoken}

    //activar datatable a detalle de sustancias
    //asignar datable a objeto manejador de datos de la compra
    compra.datatable = $('#tblistado').DataTable({
        'responsive': true,
        'destroy': true,
        "ordering": false,
        'columns': [
            {
                "className": 'details-control',
                'data': 'id'
            },
            {'data': 'nombre'},
            {'data': 'id'},
            {'data': 'cantidad_ingreso'},
            {'data': 'cantidad'},
            {'data': 'cupo_autorizado'},
            {'data': 'unidad_medida.nombre'}
        ],
        'columnDefs': [
            {
                'targets': [0],
                'orderable': false,
                'render': function (data, type, row) {
                    return '<a rel="remove" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash"></i></a> ';
                }
            },
            {
                'targets': [2],
                'orderable': false,
                'render': function (data, type, row) {
                    return '<div class="form-group form-group-sm"><select name="lugar_ingreso" class="form-control-sm" style="width: 100%"></select></div>';
                }
            },
            {
                'targets': [3],
                'orderable': false,
                'render': function (data, type, row) {
                    return '<input value="' + data + '" type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off"/>';
                }
            }
        ],
        'rowCallback': function (row, data, displayNum, displayIndex, dataIndex) {
            updateRowsCallback(row, data, dataIndex)
        }
    });

    //activar plugin select2 a los select del formulario
    $('.select2').select2({
        'theme': 'bootstrap4',
        'language': 'es'
    });

    //activar plugin datetimepicker para las fechas
    $('#llegada_bodega').datetimepicker({
        'format': 'YYYY-MM-DD',
        'date': moment().format('YYYY-MM-DD'),
        'locale': 'es'
    });

    //activar plugin datetimepicker para las horas
    $('#hora_llegada_bodega').datetimepicker({
        format: 'HH:mm:ss',
        locale: 'es',
        use24hours: true,
        disabledHours: [0, 1, 2, 3, 4, 5, 6, 7, 18, 19, 20, 21, 22, 23, 24],
        enabledHours: [8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
    });

    ////activar plugin TouchSpin para la convocatoria
    $("input[name='convocatoria']").TouchSpin({
        'verticalbuttons': true,
        'min': 1,
        'initval': 1,
        'verticalupclass': 'glyphicon glyphicon-plus',
        'verticaldownclass': 'glyphicon glyphicon-minus'
    });

    //evento para eliminar todas las sustancias del objeto manejador y el datatable
    $('button[rel="removeall"]').on('click', function (event) {
        compra.delete_all_sustancias();
    });

    //evento para limpiar el cuadro de busqueda de sustancias
    $('button[rel="cleansearch"]').on('click', function (event) {
        $('input[name="search"]').val("");
    });

    //activar el autocomplete en el buscador
    autocompleteInput("search", "/sustancias/", "search_substance",
        function (item) {
            compra.add_sustancia(item);
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

    update_datatable(compra.datatable, window.location.pathname, data);

    function updateRowsCallback(row, data, dataIndex) {
        $(row).find('input[name="cantidad"]').TouchSpin({
            'verticalbuttons': true,
            'min': 0.0001,
            'initval': 0.0001,
            'step': 0.1,
            'max': data.cupo_autorizado - data.cantidad,
            'forcestepdivisibility': 'none',
            'decimals': 4,
            'verticalupclass': 'glyphicon glyphicon-plus',
            'verticaldownclass': 'glyphicon glyphicon-minus',
            'buttondown_class': "btn btn-primary btn-sm",
            'buttonup_class': "btn btn-primary btn-sm"
        });
        $(row).find('select[name="lugar_ingreso"]').on('change.select2', function (e) {
            let data_select = $(this).select2('data');
            compra.set_stock_selected(parseInt(dataIndex), parseInt(data_select[0].id));
        }).select2({
            'theme': 'bootstrap4',
            'language': 'es',
            'data': compra.get_stock_item(dataIndex),
            'containerCssClass': "select2-font-size-sm"
        });
        $(row).find('select[name="lugar_ingreso"]').trigger('change.select2');

        $(row).find('input[name="cantidad"]').on('change', function (event) {
            let nueva_cantidad = parseFloat($(this).val());
            compra.update_cantidad_sustancia(nueva_cantidad, dataIndex);
        });
        $(row).find('a[rel="remove"]').on('click', function (event) {
            confirm_action(
                'Notificación',
                '¿Esta seguro de eliminar la sustancia ¡' + data.nombre + '!?',
                function () {
                    compra.delete_sustancia(dataIndex);
                }
            );
        });
    }

});