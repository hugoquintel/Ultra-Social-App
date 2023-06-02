function showPassword(){
    var password = document.getElementById("id_password");
    var password_confirm = document.getElementById("id_confirm_password");

    if (password.type === "password"){
        password.type = "text";
        password_confirm.type = "text";
    }
    else{
        password.type = "password";
        password_confirm.type = "password";
    }
}