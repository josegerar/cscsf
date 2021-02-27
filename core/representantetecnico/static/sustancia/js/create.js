const sustancias = {
    datatable: null,
    data: {
        nombre: null,
        unidad_medida: null,
        descripcion: null,
        cupo_autorizado: 0.0000,
        desgloses: []
    },
    add_desglose: function () {

    },
    list_desgloses: function () {
        let csrfmiddlewaretoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        let data_ajax = {csrfmiddlewaretoken: csrfmiddlewaretoken, action: 'list_desglose'};
        update_datatable(this.datatable, window.location.pathname, data_ajax);
    },
    update_cantidad_desglose: function (cantidad, index) {
        this.data.desgloses[index].cantidad_ingreso = nueva_cantidad;
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

    sustancias.list_desgloses();

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
});