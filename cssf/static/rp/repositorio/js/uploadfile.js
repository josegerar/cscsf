$(function () {
    $('#myFile').change(function () {
        var input = this;
        var url = $(this).val();
        console.log(this);
        var txt = "";
        if ('files' in this) {
            if (this.files.length > 0) {
                for (var i = 0; i < this.files.length; i++) {
                    var file = this.files[i];
                    console.log(file);
                    uploadFile(file)
                }
            }
        }
    });

    function verifyExtension(file) {
        var ext = $(this).val().split('.').pop();
        console.log($(this)[0].files);
        if ($(this).val() !== '') {
            if (ext !== "pdf") {
                $(this).val('');
                console.log($(this)[0].files);
                alert("Tipo de archivo no permitido: " + ext);
            }
        }

    }

    function uploadFile(file) {
        var csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken");
        var data = new FormData();
        if (csrfmiddlewaretoken.length > 0) {
            data.append("csrfmiddlewaretoken", csrfmiddlewaretoken[0].value);
        }
        console.log(file);
        data.append("file", file);
        data.append("action", 'newfile');
        data.forEach(function (value, key) {
            console.log(key + ": " + value)
        });
        $.ajax({
            'url': window.location.pathname,
            'type': 'POST',
            'data': data,
            'dataType': 'json',
            'processData': false,
            'contentType': false
        }).done(function (data) {
            listarArchivos(data)
        }).fail(function (jqXHR, textStatus, errorThrown) {

        }).always(function (data) {

        });
    }
});