$(".like").click(function() {
    const id = $(this).attr("post-id");
    $.get(`/post/${id}/likeindex`, function(data, status){
        liked = data.liked - 1
        $(`.post__card-content-like[post-id="${id}"]`).text(`${data.current_likes} Likes`)
        $(`.like[post-id="${id}"] i`).attr("class", liked ? "fa-solid fa-heart" : "fa-regular fa-heart")
});
})

$(".favorite").click(function() {
    const id = $(this).attr("post-id");
    $.get(`/post/${id}/favorite`, function(data, status){
        favorited = data.favorited
        $(`.post__card-content-favorite[post-id="${id}"]`).text(`${favorited ? "Saved" : "Save"}`)
        $(`.favorite[post-id="${id}"] i`).attr("class", favorited ? "fa-solid fa-bookmark" : "fa-regular fa-bookmark")
});
})