function showPassword() {
    var password = document.getElementById("id_password");

    if (password.type === "password"){
        password.type = "text";
    }
    else{
        password.type = "password";
    }
}