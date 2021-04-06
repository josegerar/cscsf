const sustancias = {
    datatable: null,
    data: {
        nombre: null,
        unidad_medida: null,
        descripcion: null,
        cupo_autorizado: 0.0000,
        desgloses: []
    },
    init: function () {
        get_list_data_ajax_loading('/sustancias/', {'action': 'list_desglose'}
            , function (response) {
                if (response.length === 0) message_info("No hay bodegas o laboratorios registrados");
                sustancias.data.desgloses = response;
                sustancias.list_desgloses();
            });
    },
    list_desgloses: function () {
        this.datatable.clear();
        this.datatable.rows.add(this.data.desgloses).draw();
    },
    update_cantidad_desglose: function (cantidad, index) {
        this.data.desgloses[index].cantidad_ingreso = cantidad;
        this.update_cantiad_total();
    },
    update_cantiad_total: function () {
        setTimeout(() => {
            let cantidad = 0;
            $.each(sustancias.data.desgloses, function (index, item) {
                cantidad += item.cantidad_ingreso
            });
            $('#id_cantidad_total').val(cantidad.toFixed(4));
        }, 1);
    }
}

$(function () {
    sustancias.datatable = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': true,
        'destroy': true,
        'columns': [
            {
                "className": 'details-control',
                'data': 'tipo'
            },
            {'data': 'nombre'},
            {'data': 'cantidad_ingreso'}
        ],
        'columnDefs': [
            {
                'targets': [2],
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

    sustancias.init();

    $("input[name='cupo_autorizado']")
        .on('change', function (event) {
            sustancias.data.cupo_autorizado = parseFloat($(this).val());
        })
        .TouchSpin({
            'verticalbuttons': true,
            'min': 0.00,
            'initval': 0.00,
            'step': 0.1,
            'decimals': 4,
            'verticalupclass': 'glyphicon glyphicon-plus',
            'verticaldownclass': 'glyphicon glyphicon-minus'
        });

    //activar plugin select2 a los select del formulario
    $('.select2').select2({
        'theme': 'bootstrap4',
        'language': 'es'
    });

    // Add event listener for opening and closing details
    addEventListenerOpenDetailRowDatatable('tblistado', sustancias.datatable, 'td.details-control',
        function (row, data, dataIndex) {
            updateRowsCallback(row, data, dataIndex);
        });

    function updateRowsCallback(row, data, dataIndex) {
        $(row).find('input[name="cantidad"]').TouchSpin({
            'verticalbuttons': true,
            'min': 0.0000,
            'initval': 0.0000,
            'step': 0.1,
            'forcestepdivisibility': 'none',
            'decimals': 4
        });
        $(row).find('input[name="cantidad"]').on('change', function (event) {
            let nueva_cantidad = parseFloat($(this).val());
            sustancias.update_cantidad_desglose(nueva_cantidad, dataIndex);
        });
    }
});