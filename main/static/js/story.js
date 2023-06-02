var slideIndex = 0;
var slides;
var timeout;
var time = 4000;

function showSlides() {
    var i;
    slides = document.getElementsByClassName("mySlides");

    for (i = 0; i < slides.length; i++) {
       slides[i].style.display = "none";  
    }
    slideIndex++;

    if (slideIndex> slides.length) {
		slideIndex = 1
	}    
    
    slides[slideIndex-1].style.display = "block"; 

	

    timeout = setTimeout(showSlides, time); // Change image every 8 seconds
	
}

function plusSlides(position) {
    slideIndex += position;

    if (slideIndex> slides.length){
		slideIndex = 1
	}

    else if(slideIndex<1){
		slideIndex = slides.length
	}

    for (i = 0; i < slides.length; i++){
       slides[i].style.display = "none";  
    }
 
    slides[slideIndex-1].style.display = "block";

	clearTimeout(timeout);
  	timeout = setTimeout(showSlides, time);
}





function timeAgo(input) {
	const date = (input instanceof Date) ? input : new Date(input);
	const formatter = new Intl.RelativeTimeFormat('en');
	const ranges = {
		years: 3600 * 24 * 365,
		months: 3600 * 24 * 30,
		weeks: 3600 * 24 * 7,
		days: 3600 * 24,
		hours: 3600,
		minutes: 60,
		seconds: 1
	};
	const secondsElapsed = (date.getTime() - Date.now()) / 1000;
	for (let key in ranges) {
		if (ranges[key] < Math.abs(secondsElapsed)) {
			const delta = secondsElapsed / ranges[key];
			return formatter.format(Math.round(delta), key);
		}
	}
  }



$(document).ready(function(){
    const modal = $('.modal')
    slideIndex = 1;

    $('.showModal').click(function(event) {

		let storyid = event.currentTarget.name;
		var len = 0;

		$.ajax({
			type: 'GET',
			url: 'http://127.0.0.1:8000/stories/showmedia/' + storyid,
			dataType: 'json',

			success: function(data){
				$.each(data, function(i, v){
	
					if (v.content.slice(v.content.length - 3) === 'mp4'){
						var div_slide_html =`
											<div class="mySlides fade">
											
												<div class="box">
													<div class="media-left m-0">
														
														<div class="content mb-3">
															<strong class="title is-3">@${v.user__username}</strong> 
															<small class="subtitle is-4 ml-3 m-0">${timeAgo(v.posted)}</small>
														</div>
														
														<progress class="progress progress-bar-js" value="${i}" max="${data.length}"></progress>
													</div>
													
													<div class="numbertext" style="z-index: 10; top: 13%">${i + 1} / ${data.length} </div>

													<video class="is-clickable image" controls="controls" preload="metadata">
														<source src="/media/${v.content}#t=0.5" type="video/mp4">
													</video>
												</div>
												<div class="text">${v.caption}</div>
											</div>
											`
											
					}
					else{
						var div_slide_html =`
											<div class="mySlides fade">
												
												<div class="box">
													<div class="media-left m-0">
														
														<div class="content mb-3">
															<strong class="title is-3">@${v.user__username}</strong> 
															<small class="subtitle is-4 ml-3 m-0">${timeAgo(v.posted)}</small>
															
														</div>
														<progress class="progress progress-bar-js" value="${i}" max="${data.length}"></progress>
													</div>
													
													<figure class="image is-4by5">
														<div class="numbertext" style="z-index: 10">${i + 1} / ${data.length} </div>
														<img src="/media/${v.content}" alt="Image">
													</figure>
												</div>
												<div class="text">${v.caption}</div>
												
											</div>
											`
					}

					$('#jsondata').append(div_slide_html);
				});
			},

			complete: function(){
				slideIndex = 0
				showSlides();
			}

		})
 
        modal.addClass('is-active')
        
    })

    $('.closeModal').click(function(event) {
		const slides = document.getElementById('jsondata');
		slides.innerHTML = '';
        modal.removeClass('is-active')
		clearTimeout(timeout)
    })

});


