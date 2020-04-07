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

$(document).ready(function(){
	var controller = new ScrollMagic.Controller();	//init scrollMagic

	var scene = new ScrollMagic.Scene ({
		triggerElement: '#image1',
		duration: '80%',
		triggerHook: 0.55
	})

	.setClassToggle('#image1', 'fade-in')
	
	// .addIndicators({
	// 	colorTrigger: 'black',
	// 	colorStart: 'green',
	// 	colorEnd: 'red'
	// })	//for testing purposes

	.addTo(controller);
});

$(document).ready(function(){
	var controller = new ScrollMagic.Controller();	//init scrollMagic

	var scene = new ScrollMagic.Scene ({
		triggerElement: '#image2',
		duration: '110%',
		triggerHook: 0.75
	})

	.setClassToggle('#image2', 'fade-in')

	.addTo(controller);
});

$(document).ready(function(){
	var controller = new ScrollMagic.Controller();	//init scrollMagic

	var scene = new ScrollMagic.Scene ({
		triggerElement: '.popUpButton',
		duration: '40%',
		triggerHook: 0.5
	})

	.setClassToggle('.popUpButton', 'fade-in')
	.addTo(controller);
});

$(document).ready(function(){
	var controller = new ScrollMagic.Controller();	//init scrollMagic

	var scene = new ScrollMagic.Scene ({
		triggerElement: '#ul5',
		duration: '125%',
		triggerHook: 0.4
	})

	.setClassToggle('.childliverdisease', 'fade-in')
	.addTo(controller);
});

$(document).ready(function(){
	var controller = new ScrollMagic.Controller();	//init scrollMagic

	var scene = new ScrollMagic.Scene ({
		triggerElement: '#image3',
		duration: '80%',
		triggerHook: 0.55
	})

	.setClassToggle('#image3', 'fade-in')

	.addTo(controller);
});

$(document).ready(function(){
	var controller = new ScrollMagic.Controller();	//init scrollMagic

	var scene = new ScrollMagic.Scene ({
		triggerElement: '#image4',
		duration: '70%',
		triggerHook: 0.55
	})

	

	.setClassToggle('#image4', 'fade-in')

	.addTo(controller);
});

$(document).ready(function(){
	var controller = new ScrollMagic.Controller();	//init scrollMagic

	var scene = new ScrollMagic.Scene ({
		triggerElement: '#image5',
		duration: '70%',
		triggerHook: 0.55
	})

	.setClassToggle('#image5', 'fade-in')

	.addTo(controller);
});

