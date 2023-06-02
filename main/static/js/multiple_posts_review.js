var first = true;

$("#id_content").on("change", (e) => {
    const rawfiles = e.target.files;
  if (rawfiles.length === 0) return;
  if (first) {
    $(".placeholder").remove();
	
    $(".field.slider").prepend(`
        <div class="slideshow-container">
            <div class="slideshow-content">
            </div>
            <a class="prev" onclick="plusSlides(-1)">&#10094;</a>
            <a class="next" onclick="plusSlides(1)">&#10095;</a>
        </div>
    `);
    first = false;
  }

  const files = Array.from(rawfiles).map(file => ({
    data: URL.createObjectURL(file),
    type: file.type
  }));

  const html = files
    .map((file, index) => {
        let tag = `
				<figure class="image is-256x256">   
					<img src="${file.data}" alt="Image" />
				</figure>
				`;
        if (file.type.includes("video")) {
            tag = `<video class="is-clickable" controls="controls" preload="metadata">
                        <source src="${file.data}" type="${file.type}">
                    </video>`;
        }
      return `
            <div class="mySlides fade" style="display: ${
              index === 0 ? "block" : "none"
            }">
                <div class="numbertext" style="z-index: 10">${index + 1} / ${files.length}</div>
                ${tag}
            </div>
            `;
    })
    .join("");

  	$(".slideshow-content").html(html);
});

var slideIndex = 1;

// Next/previous controls
function plusSlides(n) {
	const slides = $(".slideshow-content").children();
	let index = slideIndex + n;
	const len = slides.length;
	if (index > len) {
		index = 1;
	} else if (index < 1) {
		index = len;
	}
	$(slides[slideIndex - 1]).hide();
	$(slides[index - 1]).show();
	slideIndex = index;
}
