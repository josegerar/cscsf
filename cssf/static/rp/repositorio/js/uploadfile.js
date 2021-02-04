$(function () {
    $('#myFile').change(function () {
        if ('files' in this) {
            if (this.files.length > 0) {
                for (var i = 0; i < this.files.length; i++) {
                    var file = this.files[i];
                    if (verifyExtension(file)) {
                        uploadFile(file)
                    }
                }
                $(this).val('');
            }
        }
    });

    function verifyExtension(file) {
        var ext = file.type;
        if (ext !== "application/pdf") {
            message_error("Tipo de archivo no permitido: " + ext);
            return true;
        }
        return false;
    }

    function uploadFile(file) {
        var csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken");
        var data = new FormData();
        if (csrfmiddlewaretoken.length > 0) {
            data.append("csrfmiddlewaretoken", csrfmiddlewaretoken[0].value);
        }
        data.append("file", file);
        data.append("action", 'newfile');
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
                    uploadProgressHandler,
                    false
                );
                xhr.addEventListener("load", loadHandler, false);
                xhr.addEventListener("error", errorHandler, false);
                xhr.addEventListener("abort", abortHandler, false);

                return xhr;
            }
        }).done(function (data) {
            if (!data.hasOwnProperty('error')) {
                listarArchivos(data.content, data.urlrepository);
            } else {
                message_error(data.error);
            }
        }).fail(function (jqXHR, textStatus, errorThrown) {
            message_error(errorThrown);
        }).always(function (data) {

        });
    }

    function uploadProgressHandler(event) {
        $("#loaded_n_total").html("Uploaded " + event.loaded + " bytes of " + event.total);
        var percent = (event.loaded / event.total) * 100;
        var progress = Math.round(percent);
        $("#uploadProgressBar").html(progress + " percent na ang progress");
        $("#uploadProgressBar").css("width", progress + "%");
        $("#status").html(progress + "% uploaded... please wait");
    }

    function loadHandler(event) {
        $("#status").html(event.target.responseText);
        $("#uploadProgressBar").css("width", "0%");
    }

    function errorHandler(event) {
        $("#status").html("Upload Failed");
    }

    function abortHandler(event) {
        $("#status").html("Upload Aborted");
    }

});