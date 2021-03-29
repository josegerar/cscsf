const informe = {
    datatable: null,
    data: {
        sustancias: [],
        laboratorio: null
    },
    add_sustancia: function (item) {
        if (this.verify_sustance_exist(item)) {
            message_error("Sustancia ya agregada");
            return false;
        }
        if (this.verify_lab_diferent()) {
            message_error("Solo puede agregar sustancias al informe de un laboratorio seleccionado");
            return false;
        }
        item = this.config_item(item);
        this.data.sustancias.push(item);
        this.list_sustancias();
    },
    config_item: function (item) {
        item["laboratorio"] = {'id': informe.data.laboratorio.id, 'text': informe.data.laboratorio.text}
        item["cantidad_consumida"] = 0;
        return item
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
                informe.data.sustancias = [];
                informe.list_sustancia();
            }
        );
    },
    list_sustancias: function () {
        this.datatable.clear();
        this.datatable.rows.add(this.data.sustancias).draw();
    },
    update_laboratorio_seleted: function (lab_item) {
        if (lab_item) this.data.laboratorio = lab_item;
    },
    update_cantidad_sustancia: function (nueva_cantidad, index) {
        this.data.sustancias[index].cantidad_consumida = nueva_cantidad;
    },
    verify_sustance_exist: function (new_item) {
        exist = false;
        $.each(this.data.sustancias, function (index, item) {
            if (new_item.id === item.id) {
                exist = true;
                return false;
            }
        });
        return exist;
    },
    verify_lab_diferent: function () {
        diferent = false;
        $.each(this.data.sustancias, function (index, item) {
            if (parseInt(item.laboratorio.id) !== parseInt(informe.data.laboratorio.id)) {
                diferent = true;
                return false;
            }
        });
        return diferent;
    },
    verify_send_data: function (callback, error) {
        let isValidData = true;
        $.each(this.data.sustancias, function (index, item) {
            if (item.cantidad_consumida <= 0) {
                isValidData = false;
                error(`! La sustancia ${item.value} tiene una cantidad a ingresar invalida, por favor verifique ¡`);
            }
        });
        if (isValidData) callback();
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
            {'data': 'value'},
            {'data': 'laboratorio.text'},
            {'data': 'unidad_medida'},
            {'data': 'cantidad_lab'},
            {'data': 'cantidad_consumida'}
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
                'targets': [5],
                'orderable': false,
                'render': function (data, type, row) {
                    return '<input value="' + data + '" type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off"/>';
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
            let url = `/sustancias/${encodeQueryString(data)}`;
            fetch(url, {
                'method': 'GET',
                'credentials': 'include',
                'Content-Type': 'application/json',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
                },
            })
                .then(res => res.json())
                .then((json) => {
                    response(json);
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

    //evento para limpiar el cuadro de busqueda de sustancias
    $('button[rel="cleansearch"]').on('click', function (event) {
        $('input[name="search"]').val("");
    });

    //evento para eliminar todas las sustancias del objeto manejador y el datatable
    $('button[rel="removeall"]').on('click', function (event) {
        informe.delete_all_sustancias();
    });

    $('select[name=laboratorio]').on('change.select2', function (e) {
        let data_select = $(this).select2('data');
        informe.update_laboratorio_seleted(data_select[0]);
    });

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
    }
});