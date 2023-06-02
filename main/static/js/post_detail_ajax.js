$(".like").click(function() {
    const id = $(this).attr("post-id");
    $.get(`/post/${id}/like`, function(data, status){
        liked = data.liked
        $(`.post__card-content-like`).text(`${data.current_likes} Likes`)
        $(`.like i`).attr("class", liked ? "fa-solid fa-heart" : "fa-regular fa-heart")
        console.log(data)
});
})

$(".favorite").click(function() {
    const id = $(this).attr("post-id");
    $.get(`/post/${id}/favorite`, function(data, status){
        favorited = data.favorited
        $(`.post__card-content-favorite`).text(`${favorited ? "Saved" : "Save"}`)
        $(`.favorite i`).attr("class", favorited ? "fa-solid fa-bookmark" : "fa-regular fa-bookmark")
        console.log(data)
});
})

// $("#post-comment").on('submit', function(e){
//     e.preventDefault();
//     const post_id = $('#post-id').val()
//     const user_id = $('#user-id').val()
//     const content = $('.comment-content').val()
//     $.ajax({
//         type: "POST",
//         url:`/post/${post_id}`,
//         data:{

//         }
//     })

//     return false;
// })