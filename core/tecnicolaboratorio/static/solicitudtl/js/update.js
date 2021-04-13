const solicitud = {
    datatable: null,
    data: {
        detalleSolicitud: [],
        bodega_selected: null,
        lab_selected: null
    },
    add_sustancia: function (item) {
        if (this.verify_sustance_exist(item)) {
            message_error("Sustancia ya agregada");
            return false;
        }
        if (this.verify_bod_diferent()) {
            message_error("Solo puede agregar sustancias al informe de una sola bodega seleccionado");
            return false;
        }
        if (this.verify_lab_diferent()) {
            message_error("Solo puede agregar sustancias al informe de un solo laboratorio seleccionado");
            return false;
        }
        item = this.config_item(item);
        if (item.cantidad_bodegas_total <= 0) {
            message_error("La sustancia seleccionada no tiene stock suficente en bodega");
            return false;
        }
        this.data.detalleSolicitud.push(item);
        this.list_sustancia();
    },
    add_detalle_solicitud: function (data = []) {
        $.each(data, function (index, item) {
            item.cantidad_solicitud = parseFloat(item.cantidad_solicitud);
            item.sustancia.cantidad_bodega = parseFloat(item.sustancia.cantidad_bodega);
            item.sustancia.cupo_autorizado = parseFloat(item.sustancia.cupo_autorizado);
        });
        this.data.detalleSolicitud = data;
    },
    config_item: function (item) {
        item.cupo_autorizado = parseFloat(item.cupo_autorizado);
        item.cantidad_bodega = parseFloat(item.cantidad_bodega);
        return {
            'id': -1,
            'sustancia': item,
            'cantidad_solicitud': 0,
            'bodega_selected': {'id': parseInt(this.data.bodega_selected.id), 'text': this.data.bodega_selected.text},
            'lab_selected': {'id': parseInt(this.data.lab_selected.id), 'text': this.data.lab_selected.text},
        };
    },
    get_detalles: function () {
        return this.data.detalleSolicitud;
    },
    list_sustancia: function () {
        this.datatable.clear();
        this.datatable.rows.add(this.data.detalleSolicitud).draw();
    },
    update_bodega_seleted: function (bod_item) {
        if (bod_item) this.data.bodega_selected = bod_item;
    },
    update_laboratorio_seleted: function (lab_item) {
        if (lab_item) this.data.lab_selected = lab_item;
    },
    update_cantidad_sustancia: function (nueva_cantidad, index) {
        this.data.detalleSolicitud[index].cantidad_solicitud = nueva_cantidad;
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
    verify_bod_diferent: function () {
        let diferent = false;
        $.each(this.data.detalleSolicitud, function (index, item) {
            if (item.bodega_selected.id !== parseInt(solicitud.data.bodega_selected.id)) {
                diferent = true;
                return false;
            }
        });
        return diferent;
    },
    verify_lab_diferent: function () {
        let diferent = false;
        $.each(this.data.detalleSolicitud, function (index, item) {
            if (item.lab_selected.id !== parseInt(solicitud.data.lab_selected.id)) {
                diferent = true;
                return false;
            }
        });
        return diferent;
    },
    verify_send_data: function (callback, error) {
        let isValidData = true;
        if (this.data.detalleSolicitud.length === 0) {
            isValidData = false;
            error("¡Debe existir al menos 1 sustancia agregada en la solicitud!");
        } else {
            $.each(this.data.detalleSolicitud, function (index, item) {
                if (item.cantidad_solicitud <= 0) {
                    isValidData = false;
                    error(`! La sustancia ${item.sustancia.value} tiene una cantidad a solicitar invalida, por favor verifique ¡`);
                }
            });
        }
        if (isValidData) callback();
    },
    verify_sustance_exist: function (new_item) {
        let exist = false;
        $.each(this.data.detalleSolicitud, function (index, item) {
            if (new_item.id === item.sustancia.id) {
                exist = true;
                return false;
            }
        });
        return exist;
    }
}

$(function () {
    let data_loaded = false;
    let id_solicitud = $('#formCrearSolicitud').find('input[name=id_solicitud]').val();
    solicitud.datatable = $('#tblistado').DataTable({
        'responsive': true,
        "ordering": false,
        "autoWidth": true,
        'deferRender': true,
        'processing': true,
        'ajax': {
            'url': '/solicitudes/',
            'type': 'GET',
            'data': function (d) {
                d.action = 'searchdetail';
                d.id_sol = id_solicitud;
            },
            "dataSrc": function (json) {
                data_loaded = true;
                solicitud.add_detalle_solicitud(json);
                return solicitud.get_detalles();
            }
        },
        'columns': [
            {
                "className": 'show-data-hide-control',
                'data': 'id'
            },
            {'data': 'sustancia.value'},
            {'data': 'cantidad_solicitud'},
            {'data': 'bodega_selected.text'},
            {'data': 'sustancia.cantidad_bodega'},
            {'data': 'sustancia.unidad_medida'}
        ],
        'columnDefs': [
            {
                'targets': [0],
                'render': function (data, type, row) {
                    return '<a rel="remove" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash"></i></a> ';
                }
            },
            {
                'targets': [2],
                'render': function (data, type, row) {
                    return '<input value="' + data + '" type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off"/>';
                }
            },
            {
                'targets': [4],
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

    $('select[name=bodega]').on('change.select2', function (e) {
        let data_select = $(this).select2('data');
        solicitud.update_bodega_seleted(data_select[0]);
    }).select2({
        'theme': 'bootstrap4',
        'language': 'es'
    });

    $('select[name=laboratorio]').on('change.select2', function (e) {
        let data_select = $(this).select2('data');
        solicitud.update_laboratorio_seleted(data_select[0]);
    }).select2({
        'theme': 'bootstrap4',
        'language': 'es'
    });

    $('select[name=bodega]').trigger("change.select2");
    $('select[name=laboratorio]').trigger("change.select2");

    $('input[name=search]').focus().autocomplete({
        source: function (request, response) {
            if (!data_loaded) {
                message_info("Cargando...");
                return false;
            }
            let code_bod = solicitud.data.bodega_selected
                ? solicitud.data.bodega_selected.id.length > 0
                    ? parseInt(solicitud.data.bodega_selected.id)
                    : 0
                : 0;
            if (code_bod === 0) {
                message_info("Bodega no seleccionada");
                return false;
            }
            let code_lab = solicitud.data.lab_selected
                ? solicitud.data.lab_selected.id.length > 0
                    ? parseInt(solicitud.data.lab_selected.id)
                    : 0
                : 0;
            if (code_lab === 0) {
                message_info("Laboratorio no seleccionado");
                return false;
            }
            let data = {
                'term': request.term,
                'action': "search_sus_bod_lab",
                'code_bod': code_bod,
                'code_lab': code_lab
            }
            get_list_data_ajax('/sustancias/', data, function (res_data) {
                response(res_data);
            });
        },
        delay: 400,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();
            solicitud.add_sustancia(ui.item);
            $(this).val('');
        }
    });

    // Add event listener for opening and closing details
    addEventListenerOpenDetailRowDatatable('tblistado', solicitud.datatable
        , 'td.show-data-hide-control',
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

        activePluguinTouchSpinInputRow(row, "cantidad", data.sustancia.cupo_autorizado,
            0, data.cantidad_solicitud, 0.1);

        $(row).find('input[name="cantidad"]').on('change', function (event) {
            let nueva_cantidad = parseFloat($(this).val());
            solicitud.update_cantidad_sustancia(nueva_cantidad, dataIndex);
        });
        $(row).find('a[rel="remove"]').on('click', function (event) {
            confirm_action(
                'Notificación',
                '¿Esta seguro de eliminar la sustancia ¡' + data.sustancia.value + '!?',
                function () {
                    solicitud.delete_sustancia(dataIndex);
                }
            );
        });
    }
});