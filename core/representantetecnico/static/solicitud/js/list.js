$(function () {
    const data = {'action': 'searchdata', 'csrfmiddlewaretoken': getCookie("csrftoken")};
    const tblistado = $('#tblistado').DataTable({
        'responsive': true,
        'autoWidth': false,
        'destroy': true,
        'columns': [
            {
                "className": 'details-control',
                'data': 'id'
            },
            {'data': 'solicitante'},
            {'data': 'laboratorio'},
            {'data': 'nombre_actividad'},
            {'data': 'documento'},
            {'data': 'fecha_autorizacion'},
            {'data': 'estado'},
            {'data': 'estado'}
        ],
        'columnDefs': [
            {
                'targets': [4],
                'render': function (data, type, row) {
                    return get_tag_url_document(data, 'Ver')
                }
            },
            {
                'targets': [5],
                'render': function (data, type, row) {
                    if (row.hasOwnProperty("fecha_autorizacion")) return row.fecha_autorizacion;
                    else return "No autorizado";
                }
            },
            {
                'targets': [6],
                'render': function (data, type, row) {
                    if (data === 'revision') {
                        return '<label class="btn-danger">Revisión</label>'
                    } else {
                        return data;
                    }
                }
            },
            {
                'targets': [7],
                'render': function (data, type, row) {
                    if (data === 'registrado') {
                        return '<button rel="confirmarSolicitud" class="btn btn-dark btn-flat btn-sm"> <i class="fas fa-save"></i> Aprobar</button>';
                    } else {
                        return "";
                    }
                }
            }
        ],
        'rowCallback': function (row, data, displayNum, displayIndex, dataIndex) {
            updateRowsCallback(row, data, dataIndex)
        }
    });

    const tbdetalles = $('#tbdetallesolicitud').DataTable({
        'responsive': true,
        'autoWidth': true,
        'paging': false,
        'searching': false,
        'ordering': false,
        "info": false,
        'columns': [
            {'data': 'sustancia'},
            {'data': 'cant_sol'},
            {'data': 'cant_ent'},
            {'data': 'cant_con'}
        ]
    });

    const tbobservaciones = $('#tbobservaciones').DataTable({
        'responsive': true,
        'autoWidth': true,
        'paging': false,
        'searching': false,
        'ordering': false,
        "info": false,
        'columns': [
            {'data': 'observacion'}
        ]
    });

    get_list_data_ajax_loading(window.location.pathname, {'action': 'searchdata'}, function (response) {
        console.log(response)
        tblistado.clear();
        tblistado.rows.add(response).draw();
    });

    $('#btnSync').on('click', function (event) {
        get_list_data_ajax_loading(window.location.pathname, {'action': 'searchdata'}, function (response) {
            tblistado.clear();
            tblistado.rows.add(response).draw();
        });
    });

    active_events_filters(['id', 'action', 'type'], function (data) {
        get_list_data_ajax_loading(window.location.pathname, data, function (response) {
            tblistado.clear();
            tblistado.rows.add(response).draw();
        });
    });

    $('#frmAutorizarSolicitud').on('submit', function (event) {
        event.preventDefault();
        let action_save = $(event.originalEvent.submitter).attr('rel');
        let form = this;
        let parameters = new FormData(form);
        if (action_save === 'aprobar') {
            $('#frmSendObs').find('h5').text("Justificacion de Aprovación")
            $('#frmSendObs').find('button[rel=btnEnviarObs]').text("Aprobar solicitud")
            $('#frmSendObs').find('button[rel=btnEnviarObs]').attr("class", "btn btn-primary")
            $('#frmSendObs').find('input[name="id"]').val(parameters.get("id_solicitud"))
            $('#frmSendObs').find('input[name="action"]').val("aprobarSolicitud")
            $('#modalSendObs').modal('show');
        } else if (action_save === 'revisar') {
            $('#frmSendObs').find('h5').text("Justificaciòn de revisiòn")
            $('#frmSendObs').find('button[rel=btnEnviarObs]').text("Revisión")
            $('#frmSendObs').find('button[rel=btnEnviarObs]').attr("class", "btn btn-danger")
            $('#frmSendObs').find('input[name="id"]').val(parameters.get("id_solicitud"))
            $('#frmSendObs').find('input[name="action"]').val("revisionSolicitud")
            $('#modalSendObs').modal('show');
        }
    });

    $('#frmSendObs').on('submit', function (event) {
        event.preventDefault();
        let form = this;
        let parameters = new FormData(form);
        parameters.append("tipoobs", "rp")
        disableEnableForm(form, true);
        submit_with_ajax(
            window.location.pathname, parameters
            , 'Confirmación'
            , '¿Estas seguro de realizar la siguiente acción?'
            , function (data) {
                $('#modalAutorizarSolicitud').modal('hide');
                $('#modalSendObs').modal('hide');
                location.reload();
            }, function () {
                disableEnableForm(form, false);
            }
        );
    });

    addEventListenerOpenDetailRowDatatable('tblistado', tblistado, 'td.details-control',
        function (row, data, dataIndex) {
            updateRowsCallback(row, data, dataIndex);
        });

    function updateRowsCallback(row, data, dataIndex) {
        $(row).find('button[rel="confirmarSolicitud"]').on('click', function (event) {
            get_list_data_ajax_loading(window.location.pathname, {'action': 'search_detalle', 'id_sl': data.id}
                , function (response) {
                    $('#modalAutorizarSolicitud').find('input[name=id_solicitud]').val(data.id);
                    let observaciones = [];
                    observaciones.push({'observacion': data.obs_bd});
                    observaciones.push({'observacion': data.obs_rp});
                    tbobservaciones.clear();
                    tbobservaciones.rows.add(observaciones).draw();
                    if (response.length > 0) {
                        tbdetalles.clear();
                        tbdetalles.rows.add(response).draw();
                    }
                    $('#modalAutorizarSolicitud').modal('show');
                });
        });
    }
});