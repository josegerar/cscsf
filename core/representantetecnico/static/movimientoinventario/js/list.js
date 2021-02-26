$(function () {
    var csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken");
    var data = {'action': 'searchdata'}
    if (csrfmiddlewaretoken.length > 0) {
        data['csrfmiddlewaretoken'] = csrfmiddlewaretoken[0].value
    }
    var tblistado = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': false,
        'destroy': true,
        'deferRender': true,
        'columns': [
            {'data': 'id'},
            {'data': 'sustancia.nombre'},
            {'data': 'cantidad'},
            {'data': 'fecha'},
            {'data': 'sustancia.unidad_medida.nombre'},
            {'data': 'tipo_movimiento.descripcion'}
        ]
    });

    update_datatable(tblistado, window.location.pathname, data);

    $('#btnSync').on('click', function () {
        update_datatable(tblistado, window.location.pathname, data);
    });
});