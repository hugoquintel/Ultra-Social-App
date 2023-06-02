$(".follow").click(function() {
    const name = $(this).attr("name");
    var option = parseInt($(this).attr("option"));
    const id = $(this).attr("user-id");
    
    $.get(`/${name}/follow/${option}`, function(data, status){
        if (option == 1){
            $(`.follow[user-id="${id}"]`).attr("class", "button is-light is-medium mb-3 follow")
            $(`.follow[user-id="${id}"]`).text("Followed").prepend(`<i class="fa-solid fa-check mr-2">`)
        }
        else{
            $(`.follow[user-id="${id}"]`).attr("class", "button is-light is-medium mb-3 follow")
            $(`.follow[user-id="${id}"]`).text("Follow")
        }
        // $(`.follow[user-id="${id}"] i`).attr("class", option ? "fa-solid fa-heart" : None)
        
    });
    
    if (option === 1){
        $(this).attr("option", 0)
    }
    else{
        $(this).attr("option", 1)
    }
    
    
})