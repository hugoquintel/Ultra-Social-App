inputs = document.getElementsByClassName("img-input");
var content = document.getElementsByClassName("newstory-content")[0];


inputs[0].onchange = e =>{
    const [file] = e.target.files;
    src = URL.createObjectURL(file);
    console.log(file.type)
    // content.innerHTML = `sad`
    if (file.type.includes("video")) {
        content.innerHTML = `<video class="is-clickable" controls="controls" preload="metadata">
                                <source src="${src}" type="${file.type}">
                            </video>`;
    }
    else{
        content.innerHTML = `<figure class="image is-256x256">
                                <img src="${src}" type="${file.type}">
                            </figure>;`
    }
}