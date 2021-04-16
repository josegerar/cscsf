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
                icon: "fas fa-folder-plus",
                callback: function (itemKey, opt, e) {
                    //modalNewFolder
                    $('#modalNewFolder').modal('show');
                    // close the menu after clicking an item
                    return true;
                }
            },
            "upload": {
                name: "Subir archivo",
                icon: "fas fa-upload",
                callback: function (itemKey, opt, e) {
                    $("#myFile").click();
                    return true;
                }
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
    $.contextMenu({
        selector: '.item-repository-file',
        callback: function (key, options) {
            window.console && console.log(key, options);
        },
        items: {
            "dowload": {
                name: "Descargar",
                icon: "fas fa-download",
                callback: function (itemKey, opt, e) {
                    const row = repositorio.datatable.row(this);
                    const data = row.data();
                    repositorio.descargar_archivo(data.url, data.nombre);
                    // close the menu after clicking an item
                    return true;
                }
            },
            "delete": {
                name: "Eliminar",
                icon: "delete",
                callback: function (itemKey, opt, e) {
                    const row = repositorio.datatable.row(this);
                    const data = row.data();
                    repositorio.delete_item(data);
                    // close the menu after clicking an item
                    return true;
                }
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
    $.contextMenu({
        selector: '.item-repository-folder',
        callback: function (key, options) {
            window.console && console.log(key, options);
        },
        items: {
            "delete": {
                name: "Eliminar",
                icon: "delete",
                callback: function (itemKey, opt, e) {
                    const row = repositorio.datatable.row(this);
                    const data = row.data();
                    repositorio.delete_item(data);
                    // close the menu after clicking an item
                    return true;
                }
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
    $.contextMenu({
        selector: '.item-recicler',
        callback: function (key, options) {
            window.console && console.log(key, options);
        },
        items: {
            "restore": {
                name: "Restaurar",
                icon: "fas fa-download",
                callback: function (itemKey, opt, e) {
                    const row = repositorio.datatable.row(this);
                    const data = row.data();
                    repositorio.restaurar_item(data);
                    // close the menu after clicking an item
                    return true;
                }
            },
            "delete": {
                name: "Eliminar",
                icon: "delete",
                callback: function (itemKey, opt, e) {
                    const row = repositorio.datatable.row(this);
                    const data = row.data();
                    repositorio.delete_item(data);
                    // close the menu after clicking an item
                    return true;
                }
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