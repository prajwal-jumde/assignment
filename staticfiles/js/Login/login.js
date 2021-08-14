function validate_login() {
    var username = $('#username').val();
    var password = $('#password').val();

    var reqBody = JSON.stringify({
        "username": username,
        "password": password,
    });

    $.ajax({
        type: "post",
        url: "check-cred/",
        data: reqBody,
        success: function (data) {
        console.log(data)
        window.location.replace(ROOT_URL + "advance-search/") ;
            
        },
        error: function (err) {
            console.log(err)
            $("#hide-error").removeClass("hide");
        }
    })
}

$(document).ready(function () {
    $('input').keypress(function (event) {
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if (keycode == '13') {
            validate_login();
        }
    });
});  