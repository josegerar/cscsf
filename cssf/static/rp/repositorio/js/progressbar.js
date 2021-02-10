function createToast() {
    var toastContainer = $('#toastContainer');
    var toast = $('<div class="toast" data-autohide="false" role="alert" aria-live="assertive" aria-atomic="true"></div>');
    var toastheader = $('<div class="toast-header"></div>');
    var toastbody = $('<div class="toast-body"></div>');
    var icon = $('<i class="rounded mr-2 fas fa-circle"></i>');
    var title = $('<strong class="mr-auto text-primary"></strong>');
    var time = $('<small class="text-muted">5 mins ago</small>');
    var btnclose = $('<button type="button" class="ml-2 mb-1 close">&times;</button>');
    var progressContainer = $('<div class="progress"></div>');
    var progressbar = $('<div class="progress-bar" role="progressbar" style="width: 0%" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>');
    toastheader.append(icon).append(title).append(time).append(btnclose);
    toastbody.append(progressContainer);
    progressContainer.append(progressbar);
    toast.append(toastheader).append(toastbody);
    toastContainer.append(toast);
    return toast;
}

function closeToast(toast) {
    setTimeout(function () {
        $(toast).toast('dispose');
    }, 1500);
}

function activeCloseToast(toast, mesage, error) {
    if (error) {
        $(toast).find('i').prop("class", 'fas fa-exclamation-triangle');
        $(toast).find('i').prop("style", 'color: red;');
    }
    $(toast).find('.toast-body').append(mesage);
    closeToast(toast);
}