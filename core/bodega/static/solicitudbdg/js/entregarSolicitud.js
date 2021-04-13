const solicitud_entrega = {
    data: {
        detalles: []
    },
    datatable: null,
    add_detalle_solicitud_entrega: function (detalles) {
        solicitud_entrega.data.detalles = detalles;
    },
    get_detalles: function () {
        return this.data.detalles;
    },
    update_cantidad_entrega: function (nueva_cantidad, index) {
        this.data.detalles[index].cant_ent = nueva_cantidad;
    }
}

$(function () {
    solicitud_entrega.datatable = $('#tbdetallesolicitud').DataTable({
        'responsive': true,
        'autoWidth': true,
        'destroy': true,
        'deferRender': true,
        'processing': true,
        'ajax': {
            'url': window.location.pathname,
            'type': 'GET',
            'data': function (d) {
                d.action = 'search_detalle';
            },
            "dataSrc": function (json) {
                solicitud_entrega.add_detalle_solicitud_entrega(json);
                return solicitud_entrega.get_detalles();
            }
        },
        'columns': [
            {
                "className": 'show-data-hide-control',
                'data': 'id'
            },
            {'data': 'sustancia'},
            {'data': 'cant_sol'},
            {'data': 'cant_ent'},
            {'data': 'cant_bdg'}
        ],
        'columnDefs': [
            {
                'targets': [3],
                'render': function (data, type, row) {
                    return '<input value="' + data + '" type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off"/>';
                }
            }
        ],
        'rowCallback': function (row, data, displayNum, displayIndex, dataIndex) {
            updateRowsCallbackDetalle(row, data, dataIndex);
        }
    });

    // Add event listener for opening and closing details
    addEventListenerOpenDetailRowDatatable('tbdetallesolicitud'
        , solicitud_entrega.datatable, 'td.show-data-hide-control',
        function (row, data, dataIndex) {
            updateRowsCallbackDetalle(row, data, dataIndex);
        });

    function updateRowsCallbackDetalle(row, data, dataIndex) {
        activePluguinTouchSpinInputRow(row, 'cantidad', parseFloat(data.cant_bdg),
            data.cant_sol, data.cant_sol, 0.1);
        $(row).find('input[name="cantidad"]').on('change', function (event) {
            let nueva_cantidad = parseFloat($(this).val());
            solicitud_entrega.update_cantidad_entrega(nueva_cantidad, dataIndex);
        });
        $(row).find('input[name="cantidad"]').trigger('change');
    }
});