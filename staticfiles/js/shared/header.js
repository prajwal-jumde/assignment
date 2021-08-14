$(document).ready(function () {
    $("#userFullName").html(getCookie("user_session"));
});

function logout() {
    document.cookie = "user_full_name=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    document.cookie = "user_session=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    location.href = ROOT_URL;
}

