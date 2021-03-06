let data_loaded = false;
const informe = {
    datatable: null,
    datatable_desgloses: null,
    data: {
        detalle_informe_selected: {'id': 0},
        detalleInforme: [],
        desglose_detalle: [],
        laboratorio: null
    },
    add_details: function (details) {
        $.each(details, function (index, item) {
            item.cantidad = parseFloat(item.cantidad);
            item.stock.cantidad_lab = parseFloat(item.stock.cantidad_lab);
            item.is_saved = true;
        });
        this.data.detalleInforme = details;
    },
    add_desglose_detalle: function (data) {
        let cantidad_total = 0;
        $.each(data, function (index, item) {
            item.cantidad_consumida = parseFloat(item.cantidad_consumida);
            item.cantidad_consumida_total = parseFloat(item.cantidad_consumida_total);
            item.cantidad_solicitada = parseFloat(item.cantidad_solicitada);
            cantidad_total += item.cantidad_consumida;
        });
        this.data.desglose_detalle = data;
        this.update_input_cantidad_desglose(cantidad_total);
    },
    add_sustancia: function (item) {
        item = this.config_item(item);
        if (this.verify_lab_diferent()) {
            message_error("Solo puede agregar sustancias al informe de un laboratorio seleccionado");
            return false;
        }
        if (this.verify_sustance_exist(item)) {
            message_error("Sustancia ya agregada");
            return false;
        }
        this.data.detalleInforme.push(item);
        this.list_sustancias();
    },
    clean_form_add_desglose: function () {
        $('#frmAgregarDesglose').find('input[name="documento"]').val("");
        $('#frmAgregarDesglose').find('input[name="cantidad"]').val(0);
        $('#frmAgregarDesglose').find('input[name="investigador"]').val("");
        $('#frmAgregarDesglose').find('input[name="cantidad_solicitada"]').val(0);
        $('#frmAgregarDesglose').find('input[name="cantidad_consumida"]').val(0);
        $('#frmAgregarDesglose').find('input[name="cantidad"]').trigger("touchspin.updatesettings", {
            max: 0
        });
    },
    config_item: function (item) {
        return {
            'id': -1, 'cantidad': 0,
            "laboratorio": {'id': parseInt(informe.data.laboratorio.id), 'text': informe.data.laboratorio.text},
            'stock': {
                'id': item.id,
                'nombre': item.value,
                'cantidad_lab': parseFloat(item.cantidad_lab),
                'unidad_medida': item.unidad_medida
            },
            'is_saved': false,
        }
    },
    get_detalles: function () {
        return this.data.detalleInforme;
    },
    get_deglose_detalle: function () {
        return this.data.desglose_detalle;
    },
    list_sustancias: function () {
        this.datatable.clear();
        this.datatable.rows.add(this.data.detalleInforme).draw();
    },
    update_cantidad_sustancia: function (nueva_cantidad, index) {
        this.data.detalleInforme[index].cantidad = nueva_cantidad;
    },
    update_input_cantidad_desglose: function (value) {
        $('#frmDetalleConsumoSustanciaInforme').find('input[name=cantidad_desglose_total]').val(value);
    },
    update_laboratorio_seleted: function (lab_item) {
        if (lab_item) this.data.laboratorio = lab_item;
    },
    verify_lab_diferent: function () {
        let diferent = false;
        $.each(this.data.sustancias, function (index, item) {
            if (item.laboratorio.id !== parseInt(informe.data.laboratorio.id)) {
                diferent = true;
                return false;
            }
        });
        return diferent;
    },
    verify_send_data: function (callback, error) {
        if (!data_loaded) {
            error("Cargando...");
            return false;
        }
        let isValidData = true;
        $.each(this.data.detalleInforme, function (index, item) {
            if (item.cantidad <= 0) {
                isValidData = false;
                error(`! La sustancia ${item.stock.nombre} tiene una cantidad a ingresar incorrecta, por favor verifique ¡`);
            }
        });
        if (isValidData) callback();
    },
    verify_sustance_exist: function (new_item) {
        let exist = false;
        $.each(this.data.detalleInforme, function (index, item) {
            if (new_item.stock.id === item.stock.id) {
                exist = true;
                return false;
            }
        });
        return exist;
    }
}
$(function () {
    let data_loaded_desglose = false;
    const informe_id = $('#frmCrearInforme').find('input[name=id_informe]').val();
    const csrfmiddlewaretoken = getCookie("csrftoken");

    informe.datatable = $('#tblistado').DataTable({
        'responsive': true,
        "ordering": false,
        "autoWidth": true,
        'deferRender': true,
        'processing': true,
        'ajax': {
            'url': '/informes-mensuales/',
            'type': 'GET',
            'data': function (d) {
                d.action = 'informe_detail';
                d.informe_id = informe_id;
            },
            "dataSrc": function (json) {
                data_loaded = true;
                informe.add_details(json);
                return informe.get_detalles();
            }
        },
        'columns': [
            {
                "className": 'show-data-hide-control',
                'data': 'id'
            },
            {'data': 'stock.nombre'},
            {'data': 'stock.unidad_medida'},
            {'data': 'stock.cantidad_lab'},
            {'data': 'cantidad'},
            {'data': 'id'}
        ],
        'columnDefs': [
            {
                'targets': [0],
                'render': function (data, type, row) {
                    return '<a rel="remove" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash"></i></a> ';
                }
            },
            {
                'targets': [4],
                'render': function (data, type, row) {
                    return '<input value="' + data + '" type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off"/>';
                }
            },
            {
                'targets': [5],
                'render': function (data, type, row) {
                    if (row.id > 0 && row.is_saved) {
                        return '<a rel="movimientos" class="btn btn-dark btn-flat"><i class="fas fa-people-carry"></i></a>';
                    } else {
                        return ""
                    }
                }
            }
        ],
        'rowCallback': function (row, data, displayNum, displayIndex, dataIndex) {
            updateRowsCallback(row, data, dataIndex);
        }
    });

    informe.datatable_desgloses = $('#tbdesglosesustanciainforme').DataTable({
        'responsive': true,
        'autoWidth': true,
        'paging': false,
        'searching': false,
        'ordering': false,
        'info': false,
        'deferRender': true,
        'processing': true,
        'ajax': {
            'url': '/informes-mensuales/desglose-sustancia/',
            'type': 'GET',
            'data': function (d) {
                d.action = 'search_desglose_sustancia';
                d.detalle_informe_id = informe.data.detalle_informe_selected.id;
            },
            "dataSrc": function (json) {
                data_loaded_desglose = true;
                informe.add_desglose_detalle(json);
                return informe.get_deglose_detalle();
            }
        },
        'columns': [
            {'data': 'solicitud'},
            {'data': 'cantidad_solicitada'},
            {'data': 'responsable_actividad'},
            {'data': 'cantidad_consumida_total'},
            {'data': 'cantidad_consumida'},
            {'data': 'id'},
            {'data': 'documento'},
            {'data': 'id'},
        ],
        'columnDefs': [
            {
                'targets': [5],
                'render': function (data, type, row) {
                    let cantidad_solicitada = parseFloat(row.cantidad_solicitada)
                    let cantidad_consumida_total = parseFloat(row.cantidad_consumida_total)
                    if (cantidad_solicitada > 0 && cantidad_consumida_total > 0)
                        return (cantidad_solicitada - cantidad_consumida_total).toFixed(4)
                    return 0
                }
            },
            {
                'targets': [6],
                'orderable': false,
                'render': function (data, type, row) {
                    return get_tag_url_document(data, 'Ver')
                }
            },
            {
                'targets': [7],
                'render': function (data, type, row) {
                    return '<button rel="remove_desglose" type="button" class="btn btn-danger"><i class="fas fa-trash"></i></button>'
                }
            }
        ],
        'rowCallback': function (row, data, displayNum, displayIndex, dataIndex) {
            updateRowsCallbackDesgloses(row, data, dataIndex);
        }
    });

    //activar plugin select2 a los select del formulario
    $('.select2').select2({
        'theme': 'bootstrap4',
        'language': 'es'
    });

    $('select[name="laboratorio"]').on('change.select2', function (e) {
        let data_select = $(this).select2('data');
        informe.update_laboratorio_seleted(data_select[0]);
    }).trigger('change.select2');

    $('input[name=search]').focus().autocomplete({
        source: function (request, response) {
            if (!data_loaded) {
                message_info("Cargando...");
                return false;
            }
            let code_lab = informe.data.laboratorio
                ? informe.data.laboratorio.id.length > 0
                    ? parseInt(informe.data.laboratorio.id)
                    : 0
                : 0;
            if (code_lab === 0) {
                message_info("Laboratorio no seleccionado");
                return false;
            }
            let data = {
                'term': request.term,
                'action': "search_sus_lab",
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
            informe.add_sustancia(ui.item);
            $(this).val('');
        }
    });

    // Add event listener for opening and closing details
    addEventListenerOpenDetailRowDatatable('tblistado', informe.datatable
        , 'td.show-data-hide-control',
        function (row, data, dataIndex) {
            updateRowsCallback(row, data, dataIndex);
        });

    $('#frmAgregarDesglose').find('input[rel=cantidad]').TouchSpin({
        'verticalbuttons': true,
        'min': 0,
        'initval': 0,
        'decimals': 4,
        'step': 0.1,
        'max': 0,
        'verticalupclass': 'glyphicon glyphicon-plus',
        'verticaldownclass': 'glyphicon glyphicon-minus'
    });

    $('#frmAgregarDesglose').find('input[name=csrfmiddlewaretoken]').val(csrfmiddlewaretoken);

    function updateRowsCallback(row, data, dataIndex) {

        activePluguinTouchSpinInputRow(row, "cantidad", parseFloat(data.stock.cantidad_lab), 0, 0, 0.1);

        $(row).find('a[rel="remove"]').on('click', function (event) {
            confirm_action(
                'Notificación',
                '¿Esta seguro de eliminar la sustancia ¡' + data.stock.nombre + '!?',
                function () {
                    informe.delete_sustancia(dataIndex);
                }
            );
        });

        $(row).find('input[name="cantidad"]').on('change', function (event) {
            let nueva_cantidad = parseFloat($(this).val());
            informe.update_cantidad_sustancia(nueva_cantidad, dataIndex);
        });

        $(row).find('a[rel="movimientos"]').on('click', function (event) {
            informe.data.detalle_informe_selected = data;
            data_loaded_desglose = false;
            informe.datatable_desgloses.ajax.reload();
            $('#frmDetalleConsumoSustanciaInforme').find('h5').text(`Lista de desgloses de sustancia ${data.stock.nombre}`)
            $('#frmDetalleConsumoSustanciaInforme').find('input[name="stock_id"]').val(data.stock.id);
            $('#frmDetalleConsumoSustanciaInforme').find('input[name="sustancia_nombre"]').val(data.stock.nombre);
            $('#frmDetalleConsumoSustanciaInforme').find('input[name="id_detalle"]').val(data.id);
            $('#frmDetalleConsumoSustanciaInforme').find('input[name="cantidad_consumida_registrada"]').val(data.cantidad);
            $('#modalDetalleConsumoSustanciaInforme').modal({
                backdrop: 'static',
                show: true
            });
        });
    }

    $('#frmDetalleConsumoSustanciaInforme').find('button[rel="btnSyncDesgl"]').on('click', function (event) {
        data_loaded_desglose = false;
        informe.datatable_desgloses.ajax.reload();
    });

    //evento para agregar un nuevo desglose de consumo de sustancia del informe
    $('#frmDetalleConsumoSustanciaInforme').find('button[rel="add_consumo"]').on('click', function (event) {
        if (!data_loaded_desglose) {
            message_info('Cargando...');
            return false;
        }
        let stock_id = $('#frmDetalleConsumoSustanciaInforme').find('input[name="stock_id"]').val();
        let sustancia_nombre = $('#frmDetalleConsumoSustanciaInforme').find('input[name="sustancia_nombre"]').val();
        let id_detalle = $('#frmDetalleConsumoSustanciaInforme').find('input[name="id_detalle"]').val();

        $('#frmAgregarDesglose').find('input[name="id_detalle"]').val(id_detalle);

        get_list_data_ajax_loading('/solicitudes/', {
                'action': 'search_sol_rec',
                'stock_id': parseInt(stock_id),
                'lab_id': parseFloat(informe.data.laboratorio.id),
                'det_inf': id_detalle
            },
            function (res_data) {
                $('#frmAgregarDesglose').find('select[name="solicitud_detalle"]').html("").select2({
                    'theme': 'bootstrap4',
                    'language': 'es',
                    'data': res_data,
                    'dropdownParent': $("#modalAgregarDesglose")
                });
                $('#frmAgregarDesglose').find('select[name="solicitud_detalle"]').on('change.select2', function (e) {
                    let data_select = $(this).select2('data');
                    if (data_select.length > 0 && parseInt(data_select[0].id) > 0) {
                        let cantidad_solicitada = parseFloat(data_select[0].cantidad_solicitada);
                        let cantidad_consumida = parseFloat(data_select[0].cantidad_consumida);

                        $('#frmAgregarDesglose').find('h5').text(`Registrar consumo de sustancia ${sustancia_nombre}`)
                        $('#frmAgregarDesglose').find('input[name="investigador"]').val(data_select[0].consumidor);
                        $('#frmAgregarDesglose').find('input[name="cantidad_solicitada"]').val(cantidad_solicitada);
                        $('#frmAgregarDesglose').find('input[name="cantidad_consumida"]').val(cantidad_consumida);
                        $('#frmAgregarDesglose').find('input[name="cantidad"]').trigger("touchspin.updatesettings", {
                            max: cantidad_solicitada - cantidad_consumida
                        });
                    } else {
                        informe.clean_form_add_desglose();
                    }
                });
                $('#frmAgregarDesglose').find('select[name="solicitud_detalle"]').trigger('change.select2');
                $('#modalAgregarDesglose').modal({
                    backdrop: 'static',
                    show: true
                });
            });
    });

    function updateRowsCallbackDesgloses(row, data, dataIndex) {
        $(row).find('button[rel="remove_desglose"]').on('click', function (event) {
            let parameters = new FormData();
            parameters.append("csrfmiddlewaretoken", csrfmiddlewaretoken);
            submit_with_ajax(
                `/informes-mensuales/desglose-sustancia/delete/${data.id}/`
                , parameters
                , 'Confirmación'
                , '¿Estas seguro de realizar la siguiente acción?'
                , function (data) {
                    informe.datatable_desgloses.ajax.reload();
                }, function (error) {
                    console.error(error);
                }
            );
        });
    }
});