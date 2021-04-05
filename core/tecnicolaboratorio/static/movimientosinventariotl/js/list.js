$(function () {
    const tblistado = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': true,
        'columns': [
            {'data': 'id'},
            {'data': 'sustancia'},
            {'data': 'can_mov'},
            {'data': 'mes'},
            {'data': 'anio'},
            {'data': 'lugar'},
            {'data': 'nombre_lugar'},
        ]
    });

    get_list_data_ajax_loading(window.location.pathname, {'action': 'searchdata', 'type': 'lab'}
        , function (response) {
            console.log(response)
            tblistado.clear();
            tblistado.rows.add(response).draw();
        });
});