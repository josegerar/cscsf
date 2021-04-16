let data_loaded = false;
const sustancias = {
    datatable: null,
    data: {
        desgloses: []
    },
    add_desgloses: function (data) {
        this.data.desgloses = data;
    },
    get_desgloses: function () {
        return this.data.desgloses;
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
            let cantidad_bodegas = 0;
            let cantidad_labs = 0;
            $.each(sustancias.data.desgloses, function (index, item) {
                if (item.tipo === 'bodega') cantidad_bodegas += item.cantidad_ingreso;
                else if (item.tipo === 'laboratorio') cantidad_labs += item.cantidad_ingreso;
                cantidad += item.cantidad_ingreso
            });
            $('#id_cantidad_total').val(cantidad.toFixed(4));
            $('#id_cantidad_total_bod').val(cantidad_bodegas.toFixed(4));
            $('#id_cantidad_total_lab').val(cantidad_labs.toFixed(4));
        }, 1);
    }
}

$(function () {
    sustancias.datatable = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': true,
        'destroy': true,
        'deferRender': true,
        'processing': true,
        'ajax': {
            'url': '/sustancias/',
            'type': 'GET',
            'data': function (d) {
                d.action = 'list_desgl_blank';
            },
            "dataSrc": function (json) {
                data_loaded = true;
                if (json.length === 0) message_info("No hay bodegas o laboratorios registrados");
                sustancias.add_desgloses(json)
                return sustancias.get_desgloses();
            }
        },
        'columns': [
            {
                "className": 'show-data-hide-control',
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

    $("input[name='cupo_autorizado']").TouchSpin({
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
    addEventListenerOpenDetailRowDatatable('tblistado', sustancias.datatable
        , 'td.show-data-hide-control',
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