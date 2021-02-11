$(function () {
    $('#viewFileModal').find(".modal-dialog").css("max-width", "100%");
    $('#viewFileModal').find(".modal-dialog").css("margin", "0");
    $('#viewFileModal').find(".modal-content").css("border", "0");
    $('#viewFileModal').find(".modal-body").css("padding", "0");

});

function viewFile(data) {
    var url = data.itemdata.url + data.itemdata.nombre_real;
    fileExists(url, (response, err, exists) => {
        if (exists) {
            var file = document.getElementById("viewFilePDF");
            var clone = file.cloneNode(true);
            clone.setAttribute('src', url);
            file.parentNode.replaceChild(clone, file)
            $('#viewFileModal').find('h5').text(data.itemdata.nombre_real);
            $('#viewFileModal').modal('show');
            $('#viewFileModal').on('hide.bs.modal', function (e) {
                if (data.parent) {
                    data.itemdata = data.parent;
                    delete data.parent;
                    history.pushState(data, null, window.location.origin + data.urlrepository + data.itemdata.id + '/');
                } else {
                    history.pushState(null, null, window.location.origin + data.urlrepository);
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
