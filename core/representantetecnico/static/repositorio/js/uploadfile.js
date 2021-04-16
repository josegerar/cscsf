$(function () {
    $('#myFile').change(function () {
        if ('files' in this) {
            if (this.files.length > 0) {
                for (let i = 0; i < this.files.length; i++) {
                    let file = this.files[i];
                    if (verifyExtension(file)) {
                        uploadFile(file)
                    }
                }
            }
        }
        $('#myFile').val("");
    });

    function verifyExtension(file) {
        var ext = file.type;
        if (ext !== "application/pdf") {
            message_error("Tipo de archivo no permitido: " + ext);
            return false;
        }
        return true;
    }

    function uploadFile(file) {
        let toastProgressBar = createToast();
        let data = new FormData();
        data.append("csrfmiddlewaretoken", repositorio.cookie);
        data.append("documento", file);
        data.append("action", 'createfile');
        $.ajax({
            'url': window.location.pathname,
            'type': 'POST',
            'data': data,
            'dataType': 'json',
            'processData': false,
            'contentType': false,
            xhr: function () {
                var xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener("progress",
                    function (event) {
                        uploadProgressHandler(event, toastProgressBar)
                    },
                    false
                );
                xhr.upload.addEventListener('loadstart',
                    function (event) {
                        uploadStartHandler(event, toastProgressBar, xhr, file);
                    }, false
                );
                xhr.addEventListener("load", function (event) {
                    loadHandler(event, toastProgressBar);
                }, false);
                xhr.addEventListener("error", function (event) {
                    errorHandler(event, toastProgressBar)
                }, false);
                xhr.addEventListener("abort", function (event) {
                    abortHandler(event, toastProgressBar)
                }, false);

                return xhr;
            }
        }).done(function (data) {
            if (!data.hasOwnProperty('error')) {
                repositorio.datatable.ajax.reload();
            } else {
                message_error(data.error);
            }
        }).fail(function (jqXHR, textStatus, errorThrown) {
            message_error(errorThrown);
        }).always(function (data) {

        });
    }

    function uploadProgressHandler(event, toastProgressBar) {
        var percent = (event.loaded / event.total) * 100;
        var progress = Math.round(percent);
        $(toastProgressBar).find('.progress-bar').css("width", progress + "%").attr('aria-valuenow', progress);
    }

    function loadHandler(event, toastProgressBar) {
        activeCloseToast(toastProgressBar, "Upload complete", false);
    }

    function uploadStartHandler(event, toastProgressBar, xhr, file) {
        $(toastProgressBar).find('.progress-bar').css("width", "0%").attr('aria-valuenow', 0);
        let name = file.name;
        if (name.length > 27){
            name = `${name.substring(0,26)}...`
        }
        $(toastProgressBar).find('strong').text(name);
        $(toastProgressBar).find("button").on('click', function () {
            xhr.abort();
        });
        $(toastProgressBar).toast('show');
    }

    function errorHandler(event, toastProgressBar) {
        activeCloseToast(toastProgressBar, "Upload failed", true);
    }

    function abortHandler(event, toastProgressBar) {
        activeCloseToast(toastProgressBar, "Upload aborted", true);
    }

});