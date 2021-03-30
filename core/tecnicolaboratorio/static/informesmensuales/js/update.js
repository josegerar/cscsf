const informe = {
    datatable: null,
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

    $('#frmAgregarDesglose').find('input[name=csrfmiddlewaretoken]').val(getCookie("csrftoken"));

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
            get_list_data_ajax_loading('/solicitudes/', {
                    'action': 'search_solicitudes_recibidas',
                    'sustancia_id': data.sustancia.id,
                    'lab_id': parseFloat(informe.data.laboratorio.id)
                },
                function (res_data) {
                    if (res_data.length === 0) {
                        message_info("No hay solicitudes recibidas con esta sustancia registradas en el sistema");
                        return false;
                    }
                    $('#frmAgregarDesglose').find('select[name="solicitud"]').select2({
                        'theme': 'bootstrap4',
                        'language': 'es',
                        'data': res_data
                    });
                    $('#frmAgregarDesglose').find('select[name="solicitud"]').on('change.select2', function (e) {
                        let data_select = $(this).select2('data');
                        let cantidad_solicitada = parseFloat(data_select[0].cantidad_solicitada);
                        let cantidad_consumida = parseFloat(data_select[0].cantidad_consumida);

                        $('#frmAgregarDesglose').find('input[name="id_detalle"]').val(data_select[0].id);
                        $('#frmAgregarDesglose').find('h5').text(`Registrar consumo de sustancia ${data.sustancia.nombre}`)
                        $('#frmAgregarDesglose').find('input[name="investigador"]').val(data_select[0].consumidor);
                        $('#frmAgregarDesglose').find('input[name="cantidad_solicitada"]').val(cantidad_solicitada);
                        $('#frmAgregarDesglose').find('input[name="cantidad_consumida"]').val(cantidad_consumida);
                        $('#frmAgregarDesglose').find('input[name="cantidad"]').trigger("touchspin.updatesettings", {
                            max: cantidad_solicitada - cantidad_consumida
                        });
                    });
                    $('#frmAgregarDesglose').find('select[name="solicitud"]').trigger('change.select2');
                    $('#modalAgregarDesglose').modal({
                        backdrop: 'static',
                        show: true
                    });
                });
        });
    }
});