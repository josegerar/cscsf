$(function () {
    const data = {'action': 'searchdata', 'csrfmiddlewaretoken': getCookie("csrftoken")};
    const tblistado = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': false,
        'destroy': true,
        'deferRender': true,
        'columns': [
            {'data': 'id'},
            {'data': 'stock.sustancia.nombre'},
            {'data': 'cantidad'},
            {'data': 'fecha'},
            {'data': 'stock.sustancia.unidad_medida.nombre'},
            {'data': 'tipo_movimiento.descripcion'}
        ]
    });

    update_datatable(tblistado, window.location.pathname, data);

    $('#btnSync').on('click', function () {
        update_datatable(tblistado, window.location.pathname, data);
    });
});