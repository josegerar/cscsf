const sustancias = {
    datatable: null,
    form_data_ajax: null,
    data: {
        nombre: null,
        unidad_medida: null,
        descripcion: null,
        cupo_autorizado: 0.0000,
        desgloses: []
    },
    init: function () {
        this.form_data_ajax = new FormData();
        this.form_data_ajax.append("action", 'list_desglose');
        send_petition_server(undefined, this.form_data_ajax, undefined, undefined)
            .then(function (data) {
                if (data.hasOwnProperty("error")) message_error(data);
                else sustancias.data.desgloses = data;
                sustancias.list_desgloses();
            });
    },
    list_desgloses: function () {
        this.datatable.clear();
        this.datatable.rows.add(this.data.desgloses).draw();
    },
    update_cantidad_desglose: function (cantidad, index) {
        this.data.desgloses[index].cantidad_ingreso = cantidad;
    },
    verify_send_data: function (callback, error) {
        let cantidad = this.get_cantidad_ingreso_total();
        if (cantidad > 0) {
            if (cantidad > this.data.cupo_autorizado) error("La cantidad a ingresar no puede ser mayor al cupo autorizado");
            else callback();
        } else callback();
    },
    get_cantidad_ingreso_total: function () {
        let cantidad = 0;
        $.each(this.data.desgloses, function (index, value) {
            cantidad += value.cantidad_ingreso;
        });
        return cantidad;
    }
}

$(function () {

    sustancias.datatable = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': false,
        'destroy': true,
        'columns': [
            {'data': 'tipo'},
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
});