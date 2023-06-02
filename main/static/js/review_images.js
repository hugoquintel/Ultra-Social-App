inputs = document.getElementsByClassName("img-input");
var images = document.getElementsByClassName("img-review");

// images[0].onchange = evt => {
//     const [file] = document.getElementsByClassName('img-review')[0].files
//     if (file) {
//         document.getElementsByClassName('img-input')[0].src = URL.createObjectURL(file)
//     }
// }

function preview(event, index) {
  const [file] = event.target.files;
  images[index].src = URL.createObjectURL(file);
}

for (const index in images) {
  inputs[index].onchange = e => preview(e, index);
}
