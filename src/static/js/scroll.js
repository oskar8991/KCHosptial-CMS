window.onclick = function(evt) {
   if(evt.target.id == "click2" || evt.target.id == "click"){
   		return
   } else {
   		closePopUp();
   }
};

function closePopUp (){
	click.checked = false;
	click2.checked = false;

}

var controller = new ScrollMagic.Controller();	//init scrollMagic
function animate(elem, dur, hook) {
	$(document).ready(function() {
		var scene = new ScrollMagic.Scene({
			triggerElement: elem,
			duration: dur,
			triggerHook: hook
		})
		.setClassToggle(elem, 'fade-in')
		.addTo(controller);
	});
} 

animate('#image1', '80%', 0.55);
animate('#image2', '110%', 0.75);
animate('#image3', '80%', 0.55);
animate('#image4', '70%', 0.55);
animate('#image5', '70%', 0.55);
animate('#image1', '80%', 0.55);
animate('#image1', '80%', 0.55);