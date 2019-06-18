function popup(message) {
    M.toast({
        html: '<span>' + message + '</span>' +
            '<button onClick="dissmiss_popup(this.parentElement)"' +
            'class="btn-flat toast-action">Close</button>'
    });
}


function dissmiss_popup(toastElement) {
    M.Toast.getInstance(toastElement).dismiss();
}