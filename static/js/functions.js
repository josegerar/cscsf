function message_error(obj) {
    let html = '';
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

function message_info(message = '') {
    console.log(message)
    Swal.fire({
        'title': '¡Notificacion!',
        'html': `<p>${message}</p>`,
        'icon': 'info'
    });
}

function disableEnableForm(form, yesNo) {
    let f = form, s, opacity;
    s = f.style;
    opacity = yesNo ? '40' : '100';
    s.opacity = s.MozOpacity = s.KhtmlOpacity = opacity / 100;
    s.filter = 'alpha(opacity=' + opacity + ')';
    for (let i = 0; i < f.length; i++) f[i].disabled = yesNo;
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function submit_with_ajax(
    url = window.location.pathname,
    parameters = new FormData(),
    title = "",
    content = "",
    callback,
    cancelOrError) {
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
                            cancelOrError()
                        }
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        message_error(errorThrown);
                        cancelOrError();
                    }).always(function (data) {

                    });
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {
                    cancelOrError();
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
        html += '<a target="_blank" href="' + data + '">' + comment + '</a>'
    } else {
        html += 'No registrado';
    }
    return html
}

function confirm_action(title, content, callback) {
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
                    callback();
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

async function send_petition_server(
    method = 'POST',
    formdata = new FormData(),
    url = window.location.pathname,
    csrfmiddlewaretoken = document.querySelector('[name=csrfmiddlewaretoken]').value) {

    // Opciones por defecto estan marcadas con un *
    const response = await fetch(url, {
        method: method, // *GET, POST, PUT, DELETE, etc.
        mode: 'same-origin', // no-cors, *cors, same-origin
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
            'X-CSRFToken': csrfmiddlewaretoken
        },
        body: formdata // body data type must match "Content-Type" header
    });
    return response.json(); // parses JSON response into native JavaScript objects
}

function encodeQueryString(params = {}) {
    const keys = Object.keys(params)
    return keys.length
        ? "?" + keys
        .map(key => encodeURIComponent(key)
            + "=" + encodeURIComponent(params[key]))
        .join("&")
        : ""
}

function autocompleteInput(nameInput = "", urlSend = "", actionName = "", selectItemCallBack) {
    //activar el autocomplete en el buscador
    $(`input[name=${nameInput}`).focus().autocomplete({
        source: function (request, response) {
            let data = {'action': actionName, 'term': request.term}
            const url = `${urlSend}${encodeQueryString(data)}`;
            fetch(url, {
                'method': 'GET',
                'credentials': 'include',
                'Content-Type': 'application/json',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
                },
            })
                .then(res => res.json())
                .then((json) => {
                    response(json);
                });
        },
        delay: 400,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();
            selectItemCallBack(ui.item);
            $(this).val('');
        }
    });
}

function activePluguinTouchSpinInputRow(row, nameInput = "", maxValue = 0) {
    $(row).find(`input[name=${nameInput}]`).TouchSpin({
        'verticalbuttons': true,
        'min': 0.0001,
        'initval': 0.0001,
        'step': 0.1,
        'max': maxValue,
        'forcestepdivisibility': 'none',
        'decimals': 4,
        'verticalupclass': 'glyphicon glyphicon-plus',
        'verticaldownclass': 'glyphicon glyphicon-minus',
        'buttondown_class': "btn btn-primary btn-sm",
        'buttonup_class': "btn btn-primary btn-sm"
    });
}