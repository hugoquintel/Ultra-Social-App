$(function () {
    $(".side-navbar-setting__button").click(function () {
        $(this).next(".side-navbar-setting-list").fadeToggle(0);
    });
});

settingBtn = document.querySelector('.js-side-navbar-setting__button')
settingBtn.onclick = function () {
    settingBtn.classList.toggle("side-navbar-setting__button--active");
}



