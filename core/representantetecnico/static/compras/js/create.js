//objecto que se encargar de almacenar y manejar la informacion a guardar de la compra publica
const compra = {
    datatable: null,
    data: {
        sustancias: []
    },
    add_sustancia: function (item) {
        item.cantidad = 1;
        let exist = false;
        $.each(this.data.sustancias, function (index, value) {
            if (item.id === value.id) {
                value.cantidad += item.cantidad;
                exist = true;
                return false;
            }
        });
        if (!exist) {
            this.data.sustancias.push(item);
        }
        this.list_sustancia();
    },
    list_sustancia: function () {
        this.datatable.clear();
        this.datatable.rows.add(this.data.sustancias).draw();
    },
    update_cantidad_sustancia: function (new_cant, index) {
        let cantidad = parseFloat(new_cant)
        if (cantidad) {
            this.data.sustancias[index].cantidad = cantidad;
        }
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
        console.log(this.data.sustancias.length)
        if (this.data.sustancias.length === 0) {
            error();
        } else {
            callback();
        }
    }
};

$(function () {
    //activar datatable a detalle de sustancias
    let tblistado = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': false,
        'destroy': true,
        'columns': [
            {'data': 'id'},
            {'data': 'nombre'},
            {'data': 'cantidad'},
            {'data': 'tipo_presentacion.nombre'}
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
                'min': 1.00,
                'initval': 1.00,
                'step': 0.1,
                'decimals': 2,
                'verticalupclass': 'glyphicon glyphicon-plus',
                'verticaldownclass': 'glyphicon glyphicon-minus'
            });
            $(row).find('input[name="cantidad"]').on('change', function (event) {
                compra.update_cantidad_sustancia($(this).val(), dataIndex);
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

    //asignar datable a objeto manejador de datos de la compra
    compra.datatable = tblistado;

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
        format: 'h:mm:ss',
        'locale': 'es'
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

    //activar el autocomplete en el buscador
    $('input[name="search"]').autocomplete({
        source: function (request, response) {
            let csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken");
            let data = {'action': 'search_substance', 'term': request.term}
            if (csrfmiddlewaretoken.length > 0) {
                data['csrfmiddlewaretoken'] = csrfmiddlewaretoken[0].value
            }
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function (data, textStatus, jqXHR) {
                    response(data);
                }
            });
        },
        delay: 500,
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
            //disableEnableForm(form, true);
            console.log(parameters);
            submit_with_ajax(
                window.location.pathname, parameters
                , 'Confirmación'
                , '¿Estas seguro de realizar la siguiente acción?'
                , function (data) {
                    location.href = '/dashboard/';
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