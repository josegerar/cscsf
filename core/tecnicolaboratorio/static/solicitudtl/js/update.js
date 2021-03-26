const solicitud = {
    datatable: null,
    data: {
        detalleSolicitud: []
    },
    add_sustancia: function (item) {
        item = this.config_item(item);
        if (item.stock.sustancia.cantidad_bodegas_total <= 0) {
            message_error("La sustancia seleccionada no tiene stock suficente en bodega");
            return false;
        }
        this.data.detalleSolicitud.push(item);
        this.list_sustancia();
    },
    add_detalle_solicitud: function (data = []) {
        $.each(data, function (index, item) {
            item.cantidad = parseFloat(item.cantidad);
            item.stock.sustancia.cupo_autorizado = parseFloat(item.stock.sustancia.cupo_autorizado)
            item.stock.sustancia.cantidad_bodega = 0;
            item.stock_selected = null;
        });
        this.data.detalleSolicitud = data;
        this.list_sustancia();
    },
    config_item: function (item) {
        let cantidad = 0;
        $.each(item.stock, function (istock, vstock) {
            if (vstock.bodega) cantidad += parseFloat(vstock.cantidad);
        });
        item.cupo_autorizado = parseFloat(item.cupo_autorizado);
        item.cantidad_bodega = 0;
        item.cantidad_bodegas_total = cantidad;
        item.stock_selected = null;
        return {'id': -1, 'cantidad': 0.0000, 'stock': {'sustancia': item, 'cantidad': 0.0000}};
    },
    get_bodegas_item: function (dataIndex) {
        let stock = [];
        $.each(this.data.detalleSolicitud[dataIndex].stock.sustancia.stock, function (istock, vstock) {
            if (vstock.bodega && parseFloat(vstock.cantidad) > 0) {
                if (!vstock.text) vstock.text = "Bod. " + vstock.bodega.nombre;
                stock.push(vstock);
            }
        });
        return stock;
    },
    list_sustancia: function () {
        this.datatable.clear();
        this.datatable.rows.add(this.data.detalleSolicitud).draw();
    },
    update_cantidad_sustancia: function (nueva_cantidad, index) {
        this.data.detalleSolicitud[index].cantidad = nueva_cantidad;
    },
    delete_sustancia: function (index) {
        this.data.detalleSolicitud.splice(index, 1);
        this.list_sustancia();
    },
    delete_all_sustancias: function () {
        if (this.data.detalleSolicitud.length === 0) return false;
        confirm_action(
            'Alerta',
            '¿Esta seguro de eliminar todas las sustancias del detalle?',
            function () {
                solicitud.data.detalleSolicitud = [];
                solicitud.list_sustancia();
            }
        );
    },
    verify_send_data: function (callback, error) {
        let isValidData = true;
        if (this.data.detalleSolicitud.length === 0) {
            isValidData = false;
            error("¡Debe existir al menos 1 sustancia agregada en la solicitud!");
        } else {
            $.each(this.data.detalleSolicitud, function (index, item) {
                if (item.cantidad <= 0) {
                    isValidData = false;
                    error(`! La sustancia ${item.nombre} tiene una cantidad a solicitar invalida, por favor verifique ¡`);
                }
            });
        }
        if (isValidData) callback();
        else error("Ha ocurrido un error");
    },
    set_stock_selected: function (dataIndex, idStock, row) {
        if (solicitud.data.detalleSolicitud[dataIndex].stock.sustancia.stock_selected &&
            solicitud.data.detalleSolicitud[dataIndex].stock.sustancia.stock_selected.id === idStock) {
            return false;
        }
        $.each(this.data.detalleSolicitud[dataIndex].stock.sustancia.stock, function (istock, vstock) {
            if (vstock.id === idStock) {
                solicitud.data.detalleSolicitud[dataIndex].stock.sustancia.stock_selected = vstock;
                solicitud.data.detalleSolicitud[dataIndex].stock.sustancia.cantidad_bodega = parseFloat(vstock.cantidad);
                return false;
            }
        });
        $(row).find('label[rel=cantidad_bodega]').text(solicitud.data.detalleSolicitud[dataIndex].stock.sustancia.cantidad_bodega);
    }
}

$(function () {

    const data = {'action': 'searchdetail', 'csrfmiddlewaretoken': getCookie('csrftoken')}

    solicitud.datatable = $('#tblistado').DataTable({
        'responsive': true,
        'destroy': true,
        "ordering": false,
        'columns': [
            {
                "className": 'details-control',
                'data': 'id'
            },
            {'data': 'stock.sustancia.nombre'},
            {'data': 'id'},
            {'data': 'cantidad'},
            {'data': 'stock.sustancia.cantidad_bodega'},
            {'data': 'stock.sustancia.unidad_medida.nombre'}
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
                    return `<label style="font-weight: 400;" rel="cantidad_bodega">${data}</label>`;
                }
            }
        ],
        'rowCallback': function (row, data, displayNum, displayIndex, dataIndex) {
            updateRowsCallback(row, data, dataIndex);
        }
    });

    get_async_data_callback(window.location.pathname, data,
        function (response) {
            solicitud.add_detalle_solicitud(response);
        },
        function (error) {
            message_error(error);
        });

    //activar plugin select2 a los select del formulario
    $('.select2').select2({
        'theme': 'bootstrap4',
        'language': 'es'
    });

    autocompleteInput("search", "/sustancias/", {'action': "search_substance"},
        function (item) {
            solicitud.add_sustancia(item);
        });

    // Add event listener for opening and closing details
    addEventListenerOpenDetailRowDatatable('tblistado', solicitud.datatable, 'td.details-control',
        function (row, data, dataIndex) {
            updateRowsCallback(row, data, dataIndex);
        });

    //evento para limpiar el cuadro de busqueda de sustancias
    $('button[rel="cleansearch"]').on('click', function (event) {
        $('input[name="search"]').val("");
    });

    //evento para eliminar todas las sustancias del objeto manejador y el datatable
    $('button[rel="removeall"]').on('click', function (event) {
        solicitud.delete_all_sustancias();
    });

    function updateRowsCallback(row, data, dataIndex) {

        activePluguinTouchSpinInputRow(row, "cantidad", data.stock.sustancia.cupo_autorizado,
            0, data.cantidad, 0.1);

        $(row).find('select[name="bodega_salida"]').on('change.select2', function (e) {
            let data_select = $(this).select2('data');
            solicitud.set_stock_selected(parseInt(dataIndex), parseInt(data_select[0].id), row);
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
            solicitud.update_cantidad_sustancia(nueva_cantidad, dataIndex);
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