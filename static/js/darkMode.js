const darkMode = document.querySelector('#darkMode');
const nav = document.querySelector('#nav');
const body = document.querySelector("body");
const staff = document.querySelector("#staff");
const click = document.querySelector("#click");
const click2 = document.querySelector("#click2");
const close = document.querySelector(".popUpHeader .close-btn");

// Const specific to Splash Page
const container = document.querySelector('.darkModeContainer');
const splashText = document.querySelectorAll('#content');
const icn = document.querySelectorAll('.icon');
const h1 = document.querySelector('h1');

// Const specific to Index Page
const popUpButtonCircle = document.querySelector('.popUpButtonCircle');
const popUpButton = document.querySelector('.popUpButton');
const popUp = document.querySelectorAll('.popUp');
const sidebar = document.querySelector('#sidebar');
const sidebarText = document.querySelectorAll('#sidebar ul li a');
const title = document.querySelectorAll("body .indexh2");

// Const specific to Announcement Page
const announcement = document.querySelector('.announcement');
const log = document.querySelector('#log');

//Const specific to Medication Page
const generate = document.querySelector('#generate');
const tableContent = document.querySelectorAll("td");
const chart = document.querySelectorAll("#chart");

//Const specific to About Page
const countour = document.querySelectorAll('#card-header');
const aboutTitle = document.querySelectorAll('h5');
const cardBody = document.querySelectorAll('#card-body');
const please = document.querySelector('#plz');

//Const specific to faq Page
const faqH = document.querySelectorAll("#faqH");
const faqText = document.querySelectorAll('#faqText');
const faqBtn = document.querySelectorAll('#faqBtn');
const card = document.querySelectorAll('.card');

window.onload = function(){
	dark();
};

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

function dark(){
	$(function(){
	    var test = localStorage.input === 'true'? true: false;
	    $('input[name=darkMode]').prop('checked', test || false);
	    dark();
	});

	$('input[name=darkMode]').on('change', function() {
	    localStorage.input = $('input[name=darkMode]').is(':checked');
	});


	if (window.location.href.indexOf('home') >= 0){
		if($('input[name=darkMode]').is(':checked')) {
			[].forEach.call(splashText, function(txtS) {
					txtS.style.background = "#060d13";
					txtS.style.borderColor = "#060d13";
				});
			[].forEach.call(icn, function(iconSplash) {
					iconSplash.style.backgroundColor = "#1f4261";
				});

			h1.style.color = "#ebebeb";
			container.style.backgroundColor = "#060d13";
			container.style.borderColor = "#060d13";			
			body.style.color = "#ebebeb";
			body.style.backgroundColor = "#0d1a26";
		} else {
			[].forEach.call(splashText, function(txtS) {
					txtS.style.background = "white";
					txtS.style.borderColor = "#206040";
				});
			[].forEach.call(icn, function(iconSplash) {
					iconSplash.style.backgroundColor = "#39ac73";
				});

			h1.style.color = "#206040";
			container.style.backgroundColor = "#39ac73";
			container.style.borderColor = "#206040";			
			body.style.color = "black";
			body.style.backgroundColor = "white";
		}
	} else {
		var navLink = document.getElementById("nav").querySelectorAll("a");
		if (window.location.href.indexOf('index') >= 0){
			var menubar = document.getElementById("collapse").querySelectorAll(".menubar .bar");
			if($('input[name=darkMode]').is(':checked')) {
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
				
				staff.style.background = "#060d13";
				sidebar.style.background = "#1a344c";
				popUpButtonCircle.style.background = "#ebebeb";
				popUpButton.style.background = "#ebebeb";
				popUpButton.style.color = "black";
				nav.style.backgroundColor = "#060d13";
				body.style.color = "#ebebeb";
				body.style.backgroundColor = "#0d1a26";
	    	} else {
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

				staff.style.background = "white";
				sidebar.style.background = "#d9f2e6";
				popUpButtonCircle.style.background = "#39ac73";
				popUpButton.style.background = "#39ac73";
				nav.style.backgroundColor = "#39ac73";
				body.style.color = "black";
				body.style.backgroundColor = "white";
	    	}

		} else if (window.location.href.indexOf('announcements') >= 0) {
			if($('input[name=darkMode]').is(':checked')) {
				[].forEach.call(navLink, function(link) {
					link.style.color = "#ebebeb";
				});

				staff.style.background = "#060d13";
				log.style.color = "white";
				announcement.style.color = 'white';
				nav.style.backgroundColor = "#060d13";
				body.style.color = "#ebebeb";
				body.style.backgroundColor = "#0d1a26";
			} else {
				[].forEach.call(navLink, function(link) {
					link.style.color = "black";
				});

				staff.style.background = "white";
				log.style.color = "black";
				announcement.style.color = 'black';
				nav.style.backgroundColor = "#39ac73";
				body.style.color = "black";
				body.style.backgroundColor = "white";
			}

		} else if (window.location.href.indexOf('medication') >= 0) {
			var tableHeader = document.getElementById("tableh").querySelectorAll("#tableh th");
			if($('input[name=darkMode]').is(':checked')) {
				[].forEach.call(navLink, function(link) {
					link.style.color = "#ebebeb";
				});
				[].forEach.call(tableHeader, function(tbl) {
					tbl.style.color = "white";
				});
				[].forEach.call(tableContent, function(content) {
					content.style.color = "white";
				});
				[].forEach.call(chart, function(chrt) {
					chrt.style.color = "white";
				});

				staff.style.background = "#060d13";
				generate.style.background = "#060d13";
				nav.style.backgroundColor = "#060d13";
				body.style.color = "#ebebeb";
				body.style.backgroundColor = "#0d1a26";
			} else {
				[].forEach.call(navLink, function(link) {
					link.style.color = "black";
				});
				[].forEach.call(tableHeader, function(tbl) {
					tbl.style.color = "black";
				});
				[].forEach.call(tableContent, function(content) {
					content.style.color = "black";
				});
				[].forEach.call(chart, function(chrt) {
					chrt.style.color = "black";
				});

				staff.style.background = "white";
				generate.style.background = "#39ac73";
				nav.style.backgroundColor = "#39ac73";
				body.style.color = "black";
				body.style.backgroundColor = "white";
			}
		} else if (window.location.href.indexOf('about') >= 0) {
			if($('input[name=darkMode]').is(':checked')) {
				[].forEach.call(navLink, function(link) {
					link.style.color = "#ebebeb";
				});
				[].forEach.call(aboutTitle, function(abt) {
					abt.style.background = "#060d13";
				});
				[].forEach.call(cardBody, function(crd) {
					crd.style.backgroundColor = "#1f4261";
				});
				[].forEach.call(countour, function(ctr) {
					ctr.style.background = "#060d13";
				});

				staff.style.background = "#060d13";
				plz.style.color = "white";
				nav.style.backgroundColor = "#060d13";
				body.style.color = "#ebebeb";
				body.style.backgroundColor = "#0d1a26";
			} else {
				[].forEach.call(navLink, function(link) {
					link.style.color = "black";
				});
				[].forEach.call(aboutTitle, function(abt) {
					abt.style.background = "#b3e6cc";
				});
				[].forEach.call(cardBody, function(crd) {
					crd.style.backgroundColor = "white";
				});
				[].forEach.call(countour, function(ctr) {
					ctr.style.background = "#b3e6cc";
				});

				staff.style.background = "white";
				plz.style.color = "black";
				nav.style.backgroundColor = "#39ac73";
				body.style.color = "black";
				body.style.backgroundColor = "white";
			}

		} else if (window.location.href.indexOf('faq') >= 0) {
			if($('input[name=darkMode]').is(':checked')) {
				[].forEach.call(navLink, function(link) {
					link.style.color = "#ebebeb";
				});
				[].forEach.call(faqText, function(cntr) {
					cntr.style.background = "#1f4261";
				});
				[].forEach.call(faqH, function(faqH) {
					faqH.style.background = "#060d13";
				});
				[].forEach.call(card, function(crd) {
					crd.style.background = "#060d13";
				});
				[].forEach.call(faqBtn, function(btn) {
					btn.style.color = "white";
				});

				staff.style.background = "#060d13";
				plz.style.color = "white";
				nav.style.backgroundColor = "#060d13";
				body.style.color = "#ebebeb";
				body.style.backgroundColor = "#0d1a26";
			}
			else {
				[].forEach.call(navLink, function(link) {
					link.style.color = "black";
				});
				[].forEach.call(faqText, function(cntr) {
					cntr.style.background = "#d9f2e6";
				});
				[].forEach.call(faqH, function(faqH) {
					faqH.style.background = "#b3e6cc";
				});
				[].forEach.call(card, function(crd) {
					crd.style.background = "#d9f2e6";
				});
				[].forEach.call(faqBtn, function(btn) {
					btn.style.color = "black";
				});

				staff.style.background = "white";
				plz.style.color = "black";
				nav.style.backgroundColor = "#39ac73";
				body.style.color = "black";
				body.style.backgroundColor = "white";
			}
		}
	}
}
