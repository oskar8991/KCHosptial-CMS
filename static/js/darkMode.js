const darkMode = document.querySelector('#darkMode');
const navLink = document.getElementById("nav").querySelectorAll("a");
const nav = document.querySelector('#nav');
const body = document.querySelector("body");


darkMode.addEventListener('change', function(e) {
	
	if(darkMode.checked){
		[].forEach.call(navLink, function(link) {
			link.style.color = "white";
		});

		nav.style.backgroundColor = "#060d13";
		body.style.color = "white";
		body.style.backgroundColor = "#0d1a26";

	}
	else {
		[].forEach.call(navLink, function(link) {
			link.style.color = "black";
		});
		nav.style.backgroundColor = "#39ac73";
		body.style.color = "black";
		body.style.backgroundColor = "white";
	}	
});