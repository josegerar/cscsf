//objecto que se encargar de almacenar y manejar la informacion a guardar de la compra publica
const compra = {
    datatable: null,
    data: {
        sustancias: []
    },
    add_sustancia: function (item) {
        item.cantidad_ingreso = 0.0001;
        item.cantidad = parseFloat(item.cantidad);
        item.cupo_autorizado = parseFloat(item.cupo_autorizado);
        let exist = false;
        $.each(this.data.sustancias, function (index, value) {
            if (item.id === value.id) {
                value.cantidad_ingreso += item.cantidad_ingreso;
                exist = true;
                return false;
            }
        });
        if (!exist) {
            if (item.cantidad_ingreso + item.cantidad > item.cupo_autorizado) {
                message_error("La sustancia " + item.nombre
                    + " ha alcanzado su limite de cupo autorizado \n no se puede ingresar");
            } else {
                this.data.sustancias.push(item);
            }
        }
        this.list_sustancia();
    },
    list_sustancia: function () {
        this.datatable.clear();
        this.datatable.rows.add(this.data.sustancias).draw();
    },
    update_cantidad_sustancia: function (nueva_cantidad, index) {
        this.data.sustancias[index].cantidad_ingreso = nueva_cantidad;
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
                compra.data.sustancias = [];
                compra.list_sustancia();
            }
        );
    },
    verify_send_data: function (callback, error) {
        if (this.data.sustancias.length === 0) {
            error();
        } else {
            callback();
        }
    }
};

$(function () {
    //token csrf django
    const csrfmiddlewaretoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    //activar datatable a detalle de sustancias
    //asignar datable a objeto manejador de datos de la compra
    compra.datatable = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': false,
        'destroy': true,
        'columns': [
            {'data': 'id'},
            {'data': 'nombre'},
            {'data': 'cantidad_ingreso'},
            {'data': 'cantidad'},
            {'data': 'cupo_autorizado'},
            {'data': 'unidad_medida.nombre'}
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
                    return '<input value="' + data + '" type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off"/>';
                }
            }
        ],
        'rowCallback': function (row, data, displayNum, displayIndex, dataIndex) {
            $(row).find('input[name="cantidad"]').TouchSpin({
                'verticalbuttons': true,
                'min': 0.0001,
                'initval': 0.0001,
                'step': 0.1,
                'max': data.cupo_autorizado - data.cantidad,
                'forcestepdivisibility': 'none',
                'decimals': 4
            });
            $(row).find('input[name="cantidad"]').on('change', function (event) {
                let nueva_cantidad = parseFloat($(this).val());
                compra.update_cantidad_sustancia(nueva_cantidad, dataIndex);
            });
            $(row).find('a[rel="remove"]').on('click', function (event) {
                confirm_action(
                    'Notificación',
                    '¿Esta seguro de eliminar la sustancia ¡' + data.nombre + '!?',
                    function () {
                        compra.delete_sustancia(dataIndex);
                    }
                );
            });
        }
    });

    //activar plugin select2 a los select del formulario
    $('.select2').select2({
        'theme': 'bootstrap4',
        'language': 'es'
    });

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
    $("input[name='convocatoria']").TouchSpin({
        'verticalbuttons': true,
        'min': 1,
        'initval': 1,
        'verticalupclass': 'glyphicon glyphicon-plus',
        'verticaldownclass': 'glyphicon glyphicon-minus'
    });

    //evento para eliminar todas las sustancias del objeto manejador y el datatable
    $('button[rel="removeall"]').on('click', function (event) {
        compra.delete_all_sustancias();
    });

    //evento para limpiar el cuadro de busqueda de sustancias
    $('button[rel="cleansearch"]').on('click', function (event) {
        $('input[name="search"]').val("");
    });

    //activar el autocomplete en el buscador
    $('input[name="search"]').focus().autocomplete({
        source: function (request, response) {
            let data = new FormData();
            data.append('action', 'search_substance');
            data.append('term', request.term);
            send_petition_server('POST', data, window.location.pathname, csrfmiddlewaretoken)
                .then(data => {
                    response(data);
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

    //envio de datos al servidor
    $('form').on('submit', function (event) {
        event.preventDefault();
        let form = this;
        compra.verify_send_data(function () {
            let parameters = new FormData(form);
            parameters.append('sustancias', JSON.stringify(compra.data.sustancias));
            disableEnableForm(form, true);
            submit_with_ajax(
                window.location.pathname, parameters
                , 'Confirmación'
                , '¿Estas seguro de realizar la siguiente acción?'
                , function (data) {
                    location.href = '/compras/';
                }, function () {
                    disableEnableForm(form, false);
                }
            );
        }, function () {
            confirm_action(
                'Notificacion',
                '¡Deben existir sustancias en el detalle para guardar la informacón de la compra!',
                function () {
                }
            );
        });
    });
});