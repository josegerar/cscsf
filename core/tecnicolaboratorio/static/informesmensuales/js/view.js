function format(d) {
    // `d` is the original data object for the row
    return `<table class="table table-sm table-active" id="tbdesglosedetalleinforme${d.id}" style="font-size: 0.9rem; text-align: center">
                <thead class="">
                <tr>
                    <th scope="col" style="width: 5%;">#</th>
                    <th scope="col" style="width: 20%;">Solicitud</th>
                    <th scope="col" style="width: 15%;">Cantidad solicitada</th>
                    <th scope="col" style="width: 15%;">Cantidad consumida total</th>
                    <th scope="col" style="width: 15%;">Cantidad consumida</th>
                    <th scope="col" style="width: 20%;">Responsable</th>
                    <th scope="col" style="width: 10%;">Documento</th>
                </thead>
                <tbody>
                </tbody>
            </table>`;
}

function active_table_desglose(data) {
    $(`#tbdesglosedetalleinforme${data.id}`).DataTable({
        'responsive': true,
        'autoWidth': true,
        'destroy': true,
        'deferRender': true,
        'paging': false,
        'searching': false,
        'ordering': false,
        'info': false,
        'processing': true,
        'ajax': {
            'url': '/informes-mensuales/desglose-sustancia/',
            'type': 'GET',
            'data': function (d) {
                d.action = "search_desglose_sustancia";
                d.detalle_informe_id = data.id
            },
            'dataSrc': ''
        },
        'columns': [
            {'data': 'id'},
            {'data': 'solicitud'},
            {'data': 'cantidad_solicitada'},
            {'data': 'cantidad_consumida_total'},
            {'data': 'cantidad_consumida'},
            {'data': 'responsable_actividad'},
            {'data': 'documento'}
        ],
        'columnDefs': [
            {
                'targets': [6],
                'render': function (data, type, row) {
                    return `<a target="_blank" href="${data}" class="nav-link" style="cursor: pointer;">Ver</i></a>`;
                }
            }
        ]
    });

}

$(function () {
    const tblistado = $('#tbdetalleinforme').DataTable({
        'scrollX': true,
        'autoWidth': false,
        'destroy': true,
        'deferRender': true,
        'processing': true,
        'ajax': {
            'url': window.location.pathname,
            'type': 'GET',
            'data': function (d) {
                d.action = "informe_detail";
            },
            'dataSrc': ''
        },
        'columns': [
            {
                "className": 'details-control',
                "orderable": false,
                "data": null,
                "defaultContent": ''
            },
            {'data': 'stock.nombre'},
            {'data': 'stock.unidad_medida'},
            {'data': 'stock.cantidad_lab'},
            {'data': 'cantidad'}
        ]
    });

    // Add event listener for opening and closing details
    $('#tbdetalleinforme tbody').on('click', 'td.details-control', function () {
        const tr = $(this).closest('tr');
        const row = tblistado.row(tr);
        if (row.child.isShown()) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        } else {
            // Open this row
            row.child(format(row.data())).show();
            tr.addClass('shown');
            active_table_desglose(row.data());
        }
    });
});