function message_error(obj) {
    console.log(obj);
    console.log("obj");
    var html = '';
    if (typeof (obj) === 'object') {
        html = '<ul style="text-align: left;">';
        $.each(obj, function (key, value) {
            html += '<li>' + key + ': ' + value + '</li>';
        });
        html += '</ul>';
    } else {
        html = '<p>' + obj + '</p>';
    }
    Swal.fire({
        'title': '¡Error!',
        'html': html,
        'icon': 'error'
    });
}

function disableEnableForm(form, yesNo) {
    var f = form, s, opacity;
    s = f.style;
    opacity = yesNo ? '40' : '100';
    s.opacity = s.MozOpacity = s.KhtmlOpacity = opacity / 100;
    s.filter = 'alpha(opacity=' + opacity + ')';
    for (var i = 0; i < f.length; i++) f[i].disabled = yesNo;
}

function submit_with_ajax(url, parameters, title, content, callback) {
    $.confirm({
        theme: 'material',
        title: title,
        icon: 'fa fa-info',
        content: content,
        columnClass: 'medium',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    $.ajax({
                        'url': url,
                        'type': 'POST',
                        'data': parameters,
                        'dataType': 'json',
                        'processData': false,
                        'contentType': false
                    }).done(function (data) {
                        if (!data.hasOwnProperty('error')) {
                            callback(data);
                        } else {
                            message_error(data.error);
                            disableEnableForm(form, false);
                        }
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        message_error(errorThrown);
                        disableEnableForm(form, false);
                    }).always(function (data) {

                    });
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {

                }
            },
        }
    });
}

function update_datatable(datatable, url, data) {
    $.ajax({
        'url': url,
        'type': 'POST',
        'data': data,
        'dataType': 'json'
    }).done(function (response) {
        console.log(response)
        if (!response.hasOwnProperty('error')) {
            if (response.length > 0) {
                datatable.clear();
                datatable.rows.add(response).draw();
            }
        } else {
            message_error(response.error);
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        message_error(errorThrown);
    }).always(function (data) {

    });
}

function get_tag_url_document(data, comment) {
    let html = '';
    if (data && data.length > 0) {
        html += '<a href="' + data + '">' + comment + '</a>'
    } else {
        html += 'Documento no registrado';
    }
    return html
}