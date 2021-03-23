const solicitud = {
    datatable: null,
    data: {
        sustancias: []
    },
    add_sustancia: function (item) {
        this.config_item(item);
        if (item.cantidad_bodegas_total <= 0) {
            message_error("La sustancia seleccionada no tiene stock suficente en bodega");
            return false;
        }
        this.data.sustancias.push(item);
        this.list_sustancia();
    },
    config_item: function (item) {
        let cantidad = 0;
        $.each(item.stock, function (istock, vstock) {
            if (vstock.bodega) {
                vstock.text = "Bod. " + vstock.bodega.nombre;
                cantidad += parseFloat(vstock.cantidad);
            } else if (vstock.laboratorio) vstock.text = "Lab. " + vstock.laboratorio.nombre;
        });
        item.cantidad_solicitud = 0;
        item.cupo_autorizado = parseFloat(item.cupo_autorizado);
        item.cantidad_bodega = 0;
        item.cantidad_bodegas_total = cantidad;
        item.stock_selected = null;
        return item;
    },
    get_bodegas_item: function (dataIndex) {
        let stock = [];
        $.each(this.data.sustancias[dataIndex].stock, function (istock, vstock) {
            if (vstock.bodega && parseFloat(vstock.cantidad) > 0) stock.push(vstock);
        });
        return stock;
    },
    list_sustancia: function () {
        this.datatable.clear();
        this.datatable.rows.add(this.data.sustancias).draw();
    },
    update_cantidad_sustancia: function (nueva_cantidad, index) {

    },
    delete_sustancia: function (index) {
        this.data.sustancias.splice(index, 1);
        this.list_sustancia();
    },
    delete_all_sustancias: function () {

    },
    verify_send_data: function (callback, error) {

    },
    set_stock_selected: function (dataIndex, idStock, row) {
        if (solicitud.data.sustancias[dataIndex].stock_selected &&
            solicitud.data.sustancias[dataIndex].stock_selected.id === idStock) {
            return false;
        }
        $.each(this.data.sustancias[dataIndex].stock, function (istock, vstock) {
            if (vstock.id === idStock) {
                solicitud.data.sustancias[dataIndex].stock_selected = vstock;
                solicitud.data.sustancias[dataIndex].cantidad_bodega = parseFloat(vstock.cantidad);
                return false;
            }
        });
        $(row).find('label[rel=cantidad_bodega]').text(solicitud.data.sustancias[dataIndex].cantidad_bodega);
    }
}

$(function () {

    solicitud.datatable = $('#tblistado').DataTable({
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
            {'data': 'cantidad_solicitud'},
            {'data': 'cantidad_bodega'},
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
                    return '<div class="form-group form-group-sm"><select name="bodega_salida" class="form-control-sm" style="width: 100%"></select></div>';
                }
            },
            {
                'targets': [3],
                'orderable': false,
                'render': function (data, type, row) {
                    return '<input value="' + data + '" type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off"/>';
                }
            },
            {
                'targets': [4],
                'orderable': false,
                'render': function (data, type, row) {
                    return `<label style="font-weight: 500;" rel="cantidad_bodega">${data}</label>`;
                }
            }
        ],
        'rowCallback': function (row, data, displayNum, displayIndex, dataIndex) {
            updateRowsCallback(row, data, dataIndex);
        }
    });

    //activar plugin select2 a los select del formulario
    $('.select2').select2({
        'theme': 'bootstrap4',
        'language': 'es'
    });

    autocompleteInput("search", "/sustancias/", "search_substance",
        function (item) {
            console.log(item);
            solicitud.add_sustancia(item);
        });

    // Add event listener for opening and closing details
    addEventListenerOpenDetailRowDatatable('tblistado', solicitud.datatable, 'td.details-control',
        function (row, data, dataIndex) {
            updateRowsCallback(row, data, dataIndex);
        });

    function updateRowsCallback(row, data, dataIndex) {

        activePluguinTouchSpinInputRow(row, "cantidad", data.cupo_autorizado - data.cupo_consumido,
            0, 0, 0.1);

        $(row).find('select[name="bodega_salida"]').on('change.select2', function (e) {

            let data_select = $(this).select2('data');

            solicitud.set_stock_selected(parseInt(dataIndex), parseInt(data_select[0].id), row);

            $(row).find('input[name="cantidad"]').trigger("touchspin.updatesettings", {
                max: solicitud.data.sustancias[dataIndex].cantidad_bodega
            });

        }).select2({
            'theme': 'bootstrap4',
            'language': 'es',
            'data': solicitud.get_bodegas_item(dataIndex),
            'containerCssClass': "select2-font-size-sm"
        });

        if (data.stock_selected && data.cantidad_bodega) {
            $(row).find('select[name="lugar_ingreso"]').val(data.stock_selected.id);
        }

        $(row).find('select[name="bodega_salida"]').trigger('change.select2');

        $(row).find('input[name="cantidad"]').on('change', function (event) {
            let nueva_cantidad = parseFloat($(this).val());
            //compra.update_cantidad_sustancia(nueva_cantidad, dataIndex);
        });
        $(row).find('a[rel="remove"]').on('click', function (event) {
            confirm_action(
                'Notificación',
                '¿Esta seguro de eliminar la sustancia ¡' + data.nombre + '!?',
                function () {
                    solicitud.delete_sustancia(dataIndex);
                }
            );
        });
    }
});