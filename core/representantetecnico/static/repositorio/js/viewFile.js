$(function () {
    $('#viewFileModal').find(".modal-dialog").css("max-width", "100%");
    $('#viewFileModal').find(".modal-dialog").css("margin", "0");
    $('#viewFileModal').find(".modal-content").css("border", "0");
    $('#viewFileModal').find(".modal-body").css("padding", "0");

});

function viewFile(data) {
    fileExists(data.url, (response, err, exists) => {
        if (exists) {
            let file = document.getElementById("viewFilePDF");
            let clone = file.cloneNode(true);
            clone.setAttribute('src', data.url);
            file.parentNode.replaceChild(clone, file)
            $('#viewFileModal').find('h5').text(data.nombre);
            $('#viewFileModal').modal('show');
            $('#viewFileModal').on('hide.bs.modal', function (e) {
                if (data.parent > 0) {
                    let parent = {'id': data.parent, 'is_dir': true};
                    history.pushState(parent, null, window.location.origin + repositorio.urlrepository + parent.id + '/');
                } else {
                    history.pushState(null, null, window.location.origin + repositorio.urlrepository);
                }
            });
        } else {
            message_error("Archivo no existe")
        }
    });
}

function fileExists(url, callback) {
    $.get(url).done(function (data) {
        callback(data, null, true);
    }).fail(function (err) {
        callback(null, err, false);
    });
}
