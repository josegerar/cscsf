const solicitud = {
    datable: null,
    data: {
        sustancias: []
    },
    add_sustancia: function (item) {
        console.log(item);
        this.data.sustancias.push(this.config_item(item));
        this.list_sustancia();
    },
    config_item: function (item) {
        $.each(item.stock, function (istock, vstock) {
            if (vstock.bodega.id) vstock.text = "Bod. " + vstock.bodega.nombre;
            else vstock.text = "Lab. " + vstock.laboratorio.nombre;
        });
        item.cantidad_solicitud = 0.0001;
        item.cantidad_bodega = 0;
        item.stock_selected = null;
        return item;
    },
    get_bodegas_item: function (dataIndex) {
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

    },
    delete_sustancia: function (index) {

    },
    delete_all_sustancias: function () {

    },
    verify_send_data: function (callback, error) {

    },
    set_stock_selected: function (dataIndex, idStock) {
        console.log(dataIndex, idStock);
        // $.each(this.data.sustancias[dataIndex].stock, function (istock, vstock) {
        //     if (vstock.id === idStock) {
        //         solicitud.data.sustancias[dataIndex].stock_selected = vstock;
        //         solicitud.data.sustancias[dataIndex].cantidad_bodega = parseFloat(vstock.cantidad).toFixed(4);
        //         return false;
        //     }
        // });
        // this.list_sustancia();
    }
}

$(function () {

    solicitud.datatable = $('#tblistado').DataTable({
        'responsive': true,
        'destroy': true,
        "ordering": false,
        'columns': [
            {'data': 'id'},
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
            }
        ],
        'rowCallback': function (row, data, displayNum, displayIndex, dataIndex) {

            activePluguinTouchSpinInputRow(row, "cantidad", parseFloat(data.cupo_autorizado).toFixed(4));

            $(row).find('select[name="bodega_salida"]').on('change.select2', function (e) {
                let data = $(this).select2('data');
                solicitud.set_stock_selected(parseInt(dataIndex), parseInt(data[0].id));
            }).select2({
                'theme': 'bootstrap4',
                'language': 'es',
                'data': solicitud.get_bodegas_item(dataIndex),
                'containerCssClass': "select2-font-size-sm"
            });
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
                        //compra.delete_sustancia(dataIndex);
                    }
                );
            });
        }
    });

    //activar plugin select2 a los select del formulario
    $('.select2').select2({
        'theme': 'bootstrap4',
        'language': 'es'
    });

    autocompleteInput("search", "/sustancias/", "search_substance",
        function (item) {
            solicitud.add_sustancia(item);
        });

});