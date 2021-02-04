(function ($) {
    'use strict';
    $.contextMenu({
        selector: '#context-menu-file',
        callback: function (key, options) {
            window.console && console.log(key, options);
        },
        items: {
            "newfolder": {
                name: "Nueva carpeta",
                icon: "fa-edit",
                callback: function (itemKey, opt, e) {
                    //modalNewFolder
                    $('#modalNewFolder').modal('show');
                    // close the menu after clicking an item
                    return true;
                }
            },
            "upload": {
                name: "Subir archivo",
                icon: "fa-upload",
                callback: function (itemKey, opt, e) {
                    $("#myFile").click();
                    return true;
                }
            },
            "dowload": {
                name: "Descargar",
                icon: "fa-download"
            },
            "paste": {
                name: "Paste",
                icon: "paste"
            },
            "delete": {
                name: "Delete",
                icon: "delete"
            },
            "sep1": "---------",
            "quit": {
                name: "Quit",
                icon: function () {
                    return 'context-menu-icon context-menu-icon-quit';
                }
            }
        }
    });
})(jQuery);