$(document).ready(function(){
    const modal = $('.modal')

    $('.showModal').click(function(event) {
        modal.addClass('is-active')
    })

    $('.closeModal').click(function(event) {
        modal.removeClass('is-active')
    })

});