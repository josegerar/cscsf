const informe = {
    datatable: null,
    datatable_desgloses: null,
    data: {
        detalleInforme: [],
        laboratorio: null
    },
    add_details: function (details) {
        $.each(details, function (index, item) {
            item.cantidad_consumida = parseFloat(item.cantidad_consumida);
            item.cantidad_lab = parseFloat(item.cantidad_lab);
            item.is_saved = true;
        });
        this.data.detalleInforme = details;
        this.list_sustancias();
    },
    add_sustancia: function (item) {
        item = this.config_item(item);
        if (this.verify_sustance_exist(item)) {
            message_error("Sustancia ya agregada");
            return false;
        }
        this.data.detalleInforme.push(item);
        this.list_sustancias();
    },
    config_item: function (item) {
        return {
            'id': -1, 'cantidad_consumida': 0, 'cantidad_lab': parseFloat(item.cantidad_lab),
            'sustancia': {'id': item.sustancia_id, 'nombre': item.value}, 'is_saved': false,
            'unidad_medida': item.unidad_medida
        }
    },
    list_sustancias: function () {
        this.datatable.clear();
        this.datatable.rows.add(this.data.detalleInforme).draw();
    },
    listConsumosSustanciaDetalleInforme: function (id_detalle) {
        get_list_data_ajax_loading('/informes-mensuales/desglose-sustancia/', {
                'action': 'search_desglose_sustancia',
                'detalle_informe_id': id_detalle
            },
            function (res_data) {
                informe.datatable_desgloses.clear();
                informe.datatable_desgloses.rows.add(res_data).draw();
            });
    },
    update_laboratorio_seleted: function (lab_item) {
        if (lab_item) this.data.laboratorio = lab_item;
    },
    verify_sustance_exist: function (new_item) {
        let exist = false;
        $.each(this.data.detalleInforme, function (index, item) {
            if (new_item.sustancia.id === item.sustancia.id) {
                exist = true;
                return false;
            }
        });
        return exist;
    }
}
$(function () {

    const csrfmiddlewaretoken = getCookie("csrftoken");

    informe.datatable = $('#tblistado').DataTable({
        'responsive': true,
        'destroy': true,
        "ordering": false,
        "autoWidth": true,
        'columns': [
            {
                "className": 'details-control',
                'data': 'id'
            },
            {'data': 'sustancia.nombre'},
            {'data': 'unidad_medida'},
            {'data': 'cantidad_lab'},
            {'data': 'cantidad_consumida'},
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
                    if (row.sustancia.id > 0 && row.is_saved) {
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
        'destroy': true,
        'paging': false,
        'searching': false,
        'ordering': false,
        'info': false,
        'columns': [
            {'data': 'solicitud'},
            {'data': 'cantidad_solicitada'},
            {'data': 'responsable_actividad'},
            {'data': 'cantidad_consumida_total'},
            {'data': 'cantidad_consumida'},
            {'data': 'id'},
            {'data': 'id'},
        ],
        'columnDefs': [
            {
                'targets': [5],
                'render': function (data, type, row) {
                    return (parseFloat(row.cantidad_solicitada) - parseFloat(row.cantidad_consumida_total)).toFixed(4)
                }
            },
            {
                'targets': [6],
                'render': function (data, type, row) {
                    return '<button rel="remove_desglose" type="button" class="btn btn-danger"><i class="fas fa-trash"></i></button>'
                }
            }
        ],
        'rowCallback': function (row, data, displayNum, displayIndex, dataIndex) {
            updateRowsCallbackDesgloses(row, data, dataIndex);
        }
    });

    get_list_data_ajax_loading(window.location.pathname, {'action': 'informe_detail'}, function (res_data) {
        informe.add_details(res_data);
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
                'action': "search_substance_lab",
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
    addEventListenerOpenDetailRowDatatable('tblistado', informe.datatable, 'td.details-control',
        function (row, data, dataIndex) {
            updateRowsCallback(row, data, dataIndex);
        });

    $('#frmAgregarDesglose').find('input[rel=cantidad]').TouchSpin({
        'verticalbuttons': true,
        'min': 0,
        'initval': 0,
        'decimals': 4,
        'step': 0.1,
        'verticalupclass': 'glyphicon glyphicon-plus',
        'verticaldownclass': 'glyphicon glyphicon-minus'
    });

    $('#frmAgregarDesglose').find('input[name=csrfmiddlewaretoken]').val(csrfmiddlewaretoken);

    function updateRowsCallback(row, data, dataIndex) {

        activePluguinTouchSpinInputRow(row, "cantidad", parseFloat(data.cantidad_lab), 0, 0, 0.1);

        $(row).find('a[rel="remove"]').on('click', function (event) {
            confirm_action(
                'Notificación',
                '¿Esta seguro de eliminar la sustancia ¡' + data.value + '!?',
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
            get_list_data_ajax_loading('/informes-mensuales/desglose-sustancia/', {
                    'action': 'search_desglose_sustancia',
                    'detalle_informe_id': data.id
                },
                function (res_data) {
                    informe.datatable_desgloses.clear();
                    informe.datatable_desgloses.rows.add(res_data).draw();
                    $('#frmDetalleConsumoSustanciaInforme').find('h5').text(`Lista de desgloses de sustancia ${data.sustancia.nombre}`)
                    $('#frmDetalleConsumoSustanciaInforme').find('input[name="sustancia_id"]').val(data.sustancia.id);
                    $('#frmDetalleConsumoSustanciaInforme').find('input[name="sustancia_nombre"]').val(data.sustancia.nombre);
                    $('#frmDetalleConsumoSustanciaInforme').find('input[name="id_detalle"]').val(data.id);
                    $('#modalDetalleConsumoSustanciaInforme').modal({
                        backdrop: 'static',
                        show: true
                    });
                });
        });
    }

    //evento para agregar un nuevo desglose de consumo de sustancia del informe
    $('#frmDetalleConsumoSustanciaInforme').find('button[rel="add_consumo"]').on('click', function (event) {
        let sustancia_id = $('#frmDetalleConsumoSustanciaInforme').find('input[name="sustancia_id"]').val();
        let sustancia_nombre = $('#frmDetalleConsumoSustanciaInforme').find('input[name="sustancia_nombre"]').val();
        let id_detalle = $('#frmDetalleConsumoSustanciaInforme').find('input[name="id_detalle"]').val();

        $('#frmAgregarDesglose').find('input[name="id_detalle"]').val(id_detalle);

        get_list_data_ajax_loading('/solicitudes/', {
                'action': 'search_solicitudes_recibidas',
                'sustancia_id': parseInt(sustancia_id),
                'lab_id': parseFloat(informe.data.laboratorio.id),
                'det_inf': id_detalle
            },
            function (res_data) {
                if (res_data.length <= 0) {
                    message_info("No existen solicitudes recibidas de esta sustancia o ya ha sido agregada al listado actual");
                    return false;
                }

                $('#frmAgregarDesglose').find('select[name="solicitud_detalle"]').select2({
                    'theme': 'bootstrap4',
                    'language': 'es',
                    'data': res_data,
                    'dropdownParent': $("#modalAgregarDesglose")
                });
                $('#frmAgregarDesglose').find('select[name="solicitud_detalle"]').on('change.select2', function (e) {
                    let data_select = $(this).select2('data');
                    let cantidad_solicitada = parseFloat(data_select[0].cantidad_solicitada);
                    let cantidad_consumida = parseFloat(data_select[0].cantidad_consumida);

                    $('#frmAgregarDesglose').find('h5').text(`Registrar consumo de sustancia ${sustancia_nombre}`)
                    $('#frmAgregarDesglose').find('input[name="investigador"]').val(data_select[0].consumidor);
                    $('#frmAgregarDesglose').find('input[name="cantidad_solicitada"]').val(cantidad_solicitada);
                    $('#frmAgregarDesglose').find('input[name="cantidad_consumida"]').val(cantidad_consumida);
                    $('#frmAgregarDesglose').find('input[name="cantidad"]').trigger("touchspin.updatesettings", {
                        max: cantidad_solicitada - cantidad_consumida
                    });
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
                    let id_detalle = $('#frmDetalleConsumoSustanciaInforme').find('input[name="id_detalle"]').val();
                    informe.listConsumosSustanciaDetalleInforme(id_detalle);
                }, function (error) {
                    console.log(error);
                }
            );
        });
    }
});