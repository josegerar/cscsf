const compra = {
    datatable: null,
    data: {
        detalleCompra: [],
        bodega_selected: null
    },
    add_sustancia: function (item) {
        if (this.verify_sustance_exist(item)) {
            message_error("Sustancia ya agregada");
            return false;
        }
        if (this.verify_bod_diferent()) {
            message_error("Solo puede agregar sustancias a la compra de una sola bodega seleccionada");
            return false;
        }
        item = this.config_item(item);
        if (item.stock.cupo_disponible <= 0) {
            message_error("La sustancia " + item.stock.value
                + " ha alcanzado su limite de cupo autorizado \n no se puede ingresar");
        } else {
            this.data.detalleCompra.push(item);
        }
        this.list_sustancia();
    },
    add_detalle_compra: function (data = []) {
        $.each(data, function (index, item) {
            item.stock.cupo_disponible = item.stock.cupo_autorizado - item.stock.cupo_consumido;
        });
        this.data.detalleCompra = data;
        this.list_sustancia();
    },
    config_item: function (item) {
        item.cupo_disponible = item.cupo_autorizado - item.cupo_consumido;
        return {
            'id': -1, 'cantidad': 0.0000, 'stock': item,
            'bodega_selected': {'id': parseInt(this.data.bodega_selected.id), 'text': this.data.bodega_selected.text}
        };
    },
    list_sustancia: function () {
        this.datatable.clear();
        this.datatable.rows.add(this.data.detalleCompra).draw();
    },
    update_cantidad_sustancia: function (nueva_cantidad, index) {
        this.data.detalleCompra[index].cantidad = nueva_cantidad;
    },
    delete_sustancia: function (index) {
        this.data.detalleCompra.splice(index, 1);
        this.list_sustancia();
    },
    delete_all_sustancias: function () {
        if (this.data.detalleCompra.length === 0) return false;
        confirm_action(
            'Alerta',
            '¿Esta seguro de eliminar todas las sustancias del detalle?',
            function () {
                compra.data.detalleCompra = [];
                compra.list_sustancia();
            }
        );
    },
    update_bodega_seleted: function (bod_item) {
        if (bod_item) this.data.bodega_selected = bod_item;
    },
    verify_bod_diferent: function () {
        let diferent = false;
        $.each(this.data.detalleCompra, function (index, item) {
            if (item.bodega_selected.id !== parseInt(compra.data.bodega_selected.id)) {
                diferent = true;
                return false;
            }
        });
        return diferent;
    },
    verify_send_data: function (callback, error) {
        let isValidData = true;
        if (this.data.detalleCompra.length === 0) {
            isValidData = false;
            error("¡Debe existir al menos 1 sustancia agregada en la solicitud!");
        } else {
            $.each(this.data.detalleCompra, function (index, item) {
                if (item.cantidad <= 0) {
                    isValidData = false;
                    error(`! La sustancia ${item.stock.value} tiene una cantidad a solicitar invalida, por favor verifique ¡`);
                }
            });
        }
        if (isValidData) callback();
    },
    verify_sustance_exist: function (new_item) {
        let exist = false;
        $.each(this.data.detalleCompra, function (index, item) {
            if (new_item.id === item.id) {
                exist = true;
                return false;
            }
        });
        return exist;
    }
};

$(function () {
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
            {'data': 'stock.value'},
            {'data': 'bodega_selected.text'},
            {'data': 'cantidad'},
            {'data': 'stock.cupo_disponible'},
            {'data': 'stock.cupo_autorizado'},
            {'data': 'stock.unidad_medida'}
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
                    return `Bod. ${data}`;
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


    $('select[name=bodega]').on('change.select2', function (e) {
        let data_select = $(this).select2('data');
        compra.update_bodega_seleted(data_select[0]);
    }).select2({
        'theme': 'bootstrap4',
        'language': 'es'
    });

    $('select[name=bodega]').trigger("change.select2");

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
    activePluginTOuchSpinInput('convocatoria', 1, 1);

    //evento para eliminar todas las sustancias del objeto manejador y el datatable
    $('button[rel="removeall"]').on('click', function (event) {
        compra.delete_all_sustancias();
    });

    //evento para limpiar el cuadro de busqueda de sustancias
    $('button[rel="cleansearch"]').on('click', function (event) {
        $('input[name="search"]').val("");
    });

    //activar el autocomplete en el buscador
    $('input[name=search]').focus().autocomplete({
        source: function (request, response) {
            let code_bod = compra.data.bodega_selected
                ? compra.data.bodega_selected.id.length > 0
                    ? parseInt(compra.data.bodega_selected.id)
                    : 0
                : 0;
            if (code_bod === 0) {
                message_info("Bodega no seleccionada");
                return false;
            }
            let data = {
                'term': request.term,
                'action': "search_sus_compra",
                'code_bod': code_bod
            }
            get_list_data_ajax('/sustancias/', data, function (res_data) {
                response(res_data);
            });
        },
        delay: 400,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();
            compra.add_sustancia(ui.item);
            $(this).val('');
        }
    });

    // Add event listener for opening and closing details
    addEventListenerOpenDetailRowDatatable('tblistado', compra.datatable, 'td.details-control',
        function (row, data, dataIndex) {
            updateRowsCallback(row, data, dataIndex);
        });

    let id_compra = $('#frmCompra').find('input[name=id_compra]').val();

    get_list_data_ajax_loading('/compras/', {'action': 'searchdetail', 'id_comp': id_compra}
        , function (response) {
            compra.add_detalle_compra(response);
        });

    function updateRowsCallback(row, data, dataIndex) {

        activePluguinTouchSpinInputRow(row, "cantidad", data.stock.cupo_disponible,
            0, 0, 0.1);

        $(row).find('input[name="cantidad"]').on('change', function (event) {
            let nueva_cantidad = parseFloat($(this).val());
            compra.update_cantidad_sustancia(nueva_cantidad, dataIndex);
        });

        $(row).find('a[rel="remove"]').on('click', function (event) {
            confirm_action(
                'Notificación',
                '¿Esta seguro de eliminar la sustancia ¡' + data.stock.value + '!?',
                function () {
                    compra.delete_sustancia(dataIndex);
                }
            );
        });
    }
});