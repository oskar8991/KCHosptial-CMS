const darkMode = document.querySelector('#darkMode');
const popUpButtonCircle = document.querySelector('.popUpButtonCircle');
const popUpButton = document.querySelector('.popUpButton');
const popUp = document.querySelectorAll('.popUp');
const navLink = document.getElementById("nav").querySelectorAll("a");
const nav = document.querySelector('#nav');
const sidebar = document.querySelector('#sidebar');
const sidebarText = document.querySelectorAll('#sidebar ul li a');
const body = document.querySelector("body");
const title = document.querySelectorAll("body .indexh2");
const menubar = document.getElementById("collapse").querySelectorAll(".menubar .bar");

darkMode.addEventListener('change', function(e) {
	
	if(darkMode.checked){
		[].forEach.call(navLink, function(link) {
			link.style.color = "#ebebeb";
		});
		[].forEach.call(menubar, function(bar) {
			bar.style.background = "#ebebeb";
		});
		[].forEach.call(title, function(titles) {
			titles.style.color = "black";
			titles.style.backgroundColor = "#ebebeb";
		});
		[].forEach.call(sidebarText, function(txt) {
			txt.style.color = "white";
		});
		[].forEach.call(popUp, function(pop) {
			pop.style.background = "#1a344c";
		});

		$(document).ready(function(){
  				$(sidebarText).hover(function(){
    				$(this).css("color", "#060d13");
    			}, function(){
    		$(this).css("color", "white");
  			});
		});
		
		sidebar.style.background = "#1a344c";
		popUpButtonCircle.style.background = "#ebebeb";
		popUpButton.style.background = "#ebebeb";
		popUpButton.style.color = "black";
		nav.style.backgroundColor = "#060d13";
		body.style.color = "#ebebeb";
		body.style.backgroundColor = "#0d1a26";
	}
	else {
		[].forEach.call(navLink, function(link) {
			link.style.color = "black";
		});
		[].forEach.call(menubar, function(bar) {
			bar.style.background = "black";
		});
		[].forEach.call(title, function(titles) {
			titles.style.color = "black";
			titles.style.backgroundColor = "#39ac73";
		});
		[].forEach.call(sidebarText, function(txt) {
			txt.style.color = "black";
		});
		[].forEach.call(popUp, function(pop) {
			pop.style.background = "white";
		});

		$(document).ready(function(){
  				$(sidebarText).hover(function(){
    				$(this).css("color", "#39ac73");
    			}, function(){
    		$(this).css("color", "black");
  			});
		});

		sidebar.style.background = "#d9f2e6";
		popUpButtonCircle.style.background = "#39ac73";
		popUpButton.style.background = "#39ac73";
		nav.style.backgroundColor = "#39ac73";
		body.style.color = "black";
		body.style.backgroundColor = "white";
	}	
});
