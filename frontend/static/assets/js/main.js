$(document).ready(function () {
	var chatLocation =localStorage['chatPosition'];
	if(chatLocation){
		var chatPosition=JSON.parse(chatLocation);
		const container = document.querySelector("#chat");
		container.style.left = chatPosition["chatPositionX"];
		container.style.top = chatPosition["chatPositionY"];
	}
	var lastLocation = localStorage['lastLocation'];
	if(lastLocation)
	{
		var Location = JSON.parse(lastLocation);
		openIntro(Location["lastLocation"]);
	}
	else{
		openIntro("home");
	}
	var activeUser = localStorage['activeUser'];
	if(activeUser)
	{
		var t_activeUser = JSON.parse(activeUser);
		loginSuccess(t_activeUser["username"]);
	}
	var auth42 = localStorage["42auth"];
	if(auth42)
	{
		var t_auth42 = JSON.parse(auth42);
		if(t_auth42["42auth"] )
		{
			fetch('https://peng.com.tr/api42/auth/query/')  // UserInfoAPI'den veri çekmek için belirlenen API URL'sini kullanabilirsiniz
    		.then(response => response.json())
    		.then(data => {
    		    console.log(data);
				if(data.success=="true")
    		    	loginSuccess(data.username);
				else if(activeUser)
					localStorage.removeItem("activeUser");


    		    // Verileri kullanmak için burada işlemler yapabilirsiniz
    		})
    		.catch(error => {
    		    console.error('Veri alınamadı: ', error);
    		});
			localStorage.removeItem("42auth");
		}
	}
	$("#logOut").on('click',function(e){
		localStorage.removeItem("activeUser");
		openIntro("login");
		login_menu=document.getElementById("menuLogin");
		login_menu.innerHTML="<a href='#' onclick=\"openIntro('login')\">Login</a>"
		fetch('https://peng.com.tr/api42/auth/logout/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
		})
		.then(response => {
			if (response.ok) {
				return response.json();
			} else {
				throw new Error('Network response was not ok.');
			}
		})
		.then(data => {
			// Gelen veriyi kontrol et
			if (data && data.message) {
				console.log('No message found in response data.');
				//loginSuccess(username);
			} else {
				console.log('No message found in response data.');
			}
		})
		.catch(error => {
			console.error('Error:', error);
		});

	});
	$("#logDeneme").on('click',function(e){
		fetch('https://peng.com.tr/api42/auth/deneme/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
		})
		.then(response => {
			if (response.ok) {
				return response.json();
			} else {
				throw new Error('Network response was not ok.');
			}
		})
		.then(data => {
			// Gelen veriyi kontrol et
			if (data && data.message) {
				console.log('No message found in response data.');
				//loginSuccess(username);
			} else {
				console.log('No message found in response data.');
			}
		})
		.catch(error => {
			console.error('Error:', error);
		});

	});
	$("#login42").on('click',function(e){
		localStorage["42auth"] = JSON.stringify({"42auth": true});;
	});
	$('#loginForm').on('submit', function (e) {
		e.preventDefault();

    	var formData = {
			username: document.getElementById('usernameLogin').value,
			password: document.getElementById('passwordLogin').value
		};
		fetch('https://peng.com.tr/api42/auth/login/', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(formData),
		})
		.then(response => {
		if (response.ok) {
			return response.json();
		} else {
			if (response.status === 400) {
				showErrorMessage('Invalid username or password.');
			}
			throw new Error('Network response was not ok.');
		}
		})
		.then(data => {
		// Gelen veriyi kontrol et
		if (data && data.message) {
			var username=data.message;
			console.log(data);
			// console.log(data.message);
			// console.log(data.email);
			// console.log(data.username);
			loginSuccess(username);
			openIntro("profile");
		} else {
			console.log('No message found in response data.');
		}
		})
		.catch(error => {
		console.error('Error:', error);
		});
	});

	
	document.getElementById("emailRegister").addEventListener("focusout", function() {
		var email = document.getElementById("emailRegister").value;
		var emailFormat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
		var errorEmail = document.getElementById("errorEmail");
	
		if (!email.match(emailFormat)) {
			errorEmail.textContent = "Lütfen geçerli bir eposta adresi girin.";
		} else {
			errorEmail.textContent = "";
		}
	});
	
	document.getElementById("passwordRegister").addEventListener("focusout", function() {
		var password = document.getElementById("passwordRegister").value;
		var passwordFormat = /^(?=.*\d)(?=.*[a-zA-Z]).{8,}$/;
		var errorPassword = document.getElementById("errorPassword");
	
		if (!password.match(passwordFormat)) {
			errorPassword.textContent = "Parolanız en az 8 karakter uzunluğunda olmalı ve en az 1 harf ve 1 sayı içermelidir.";
		} else {
			errorPassword.textContent = "";
		}
	});
	$('#signupForm').on('submit', function (e) {
		e.preventDefault();
		var errorEmail = document.getElementById("errorEmail");
		var errorPassword = document.getElementById("errorPassword");
		
		if (errorEmail.textContent || errorPassword.textContent) {
			alert("Lütfen formu doğru şekilde doldurun.");
		}
		else{
			var formData = {
				username: document.getElementById('usernameRegister').value,
				//fullname: document.getElementById('fullnameRegister').value, 
				email: document.getElementById('emailRegister').value,
				password: document.getElementById('passwordRegister').value
			};
			fetch('https://peng.com.tr/api42/auth/signup/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(formData),
			})
			.then(response => {
				if (response.ok) {
					return response.json();
				} else {
					return response.json().then(data => {
						throw new Error(data.error || 'Server error');
					});
				}
			})
			.then(data => {
				if (data) {
					console.log("başarılı",data.message);
					$('#signupForm')[0].reset(); // jQuery ile formu resetleme
					document.getElementById("loginSwitch").click();
				}
			})
			.catch(error => {
				console.error('Error:', error);
			});
		}
    	
	});
});

dragElement();


function showErrorMessage(message) {
	const errorDiv = document.createElement('div');
	errorDiv.innerHTML = "<h4 style='margin: 1rem 0 1rem 0;'>"+message+"</h4>";
	errorDiv.classList.add('d-flex', 'justify-content-center', 'align-items-center','error-message');

	const form = document.getElementById('loginForm');
	form.insertBefore(errorDiv, form.firstChild);
}

function loginSuccess(username){
	data={"username":username}
	localStorage['activeUser'] = JSON.stringify(data);
	login_menu=document.getElementById("menuLogin");
	profile_name=document.getElementById("profileName");
	if(login){
		login_menu.innerHTML="<a href='#' onclick=\"openIntro('profile')\">Profile</a>"
		profile_name.innerHTML=username;
	}

}


let isChatExtended = false;

function chatExtend(reverse = false) {
	const chatMessages = document.querySelector(".notifications");
	const chatChilds = chatMessages.querySelectorAll('*');
	const chatElement = document.querySelector("#chat");
   

		if (reverse) {
			anime({
				targets: chatMessages,
				translateY:-40,
				scale:0,
				opacity: {value:[1, 0],duration: 200},
				easing: 'easeInOutQuad',
				duration: 1000
			});
			anime({
				targets: chatChilds,
				opacity: [1, 0],
				easing: 'easeInOutQuad',
				duration: 1000,
				delay: 200
			});
			
			isChatExtended = false;
		} else {
			chatMessages.style.display = 'inline-block';
			anime({
				targets: chatMessages,
				translateY:0,
				scale:1,
				opacity: [0, 1],
				easing: 'easeInOutQuad',
				duration: 1000
			});
			anime({
				targets: chatChilds,
				opacity: [0, 1],
				easing: 'easeInOutQuad',
				duration: 1000,
				delay: 200
			});
			isChatExtended = true;
		}
	
}

function toggleChatAnimation() {
	if (isChatExtended) {
		chatExtend(true); // Tersine animasyonu başlat
	} else {
		chatExtend(); // Normal animasyonu başlat
	}
}

function dragElement() {
	const container = document.querySelector("#chat");
	var isMoved = false;
	
	container.addEventListener("mousedown", (event) => {
		isMoved = false;
		//const initialX = event.clientX - container.getBoundingClientRect().left;
		//const initialY = event.clientY - container.getBoundingClientRect().top;
//
		//function onMouseMove(event) {
		//	isMoved = true;
		//	container.style.left = event.clientX - initialX + 'px';
		//	container.style.top = event.clientY - initialY + 'px';
		//}

		function onMouseUp() {
			//document.removeEventListener('mousemove', onMouseMove);
			document.removeEventListener('mouseup', onMouseUp);
			
			if (isMoved) {
				var Temp = { chatPositionX: container.style.left, chatPositionY: container.style.top };
				localStorage['chatPosition'] = JSON.stringify(Temp);
			} else {
				toggleChatAnimation();
			}
		}

		//document.addEventListener('mousemove', onMouseMove);
		document.addEventListener('mouseup', onMouseUp);
	});
}
function showSentence(block) {
	var listItems = block.getElementsByClassName("animationText");


	function delayItems(i) {
		setTimeout(function () {
			titlesAnimation(listItems[i]);
			if (++i < listItems.length) delayItems(i);
		}, 300);
	}
	delayItems(0);

}

function titlesAnimation(titles) {
	
	//anime({
	//	targets: titles,
	//	background: [
	//		{ value: "linear-gradient(90deg, rgba(180,58,173,1) 0%, rgba(131,58,180,1) 38%, rgba(29,33,253,1) 70%, rgba(115,113,124,0) 100%", duration: 300, delay: 500 },
	//		{ value: "linear-gradient(90deg, rgba(180,58,173,1) 50%, rgba(131,58,180,1) 78%, rgba(29,33,253,1) 100%", duration: 300 },
	//		{ value: "linear-gradient(90deg, rgba(180,58,173,1) 78%, rgba(131,58,180,1) 100%", duration: 0 },
	//		{ value: "linear-gradient(270deg, rgba(180,58,173,1) 78%, rgba(131,58,180,1) 100%, rgba(115,113,124,0) 100%", duration: 0 },
	//		{ value: "linear-gradient(270deg, rgba(180,58,173,1) 50%, rgba(131,58,180,1) 78%, rgba(115,113,124,0) 100%", duration: 200 },
	//		{ value: "linear-gradient(270deg, rgba(180,58,173,1) 0%, rgba(131,58,180,1) 0%, rgba(115,113,124,0) 50%", duration: 200 },
	//		{ value: "linear-gradient(270deg, rgba(180,58,173,1) 0%, rgba(131,58,180,1) 0%, rgba(115,113,124,0) 0%", duration: 200 }
	//	],
	//	easing: "easeInOutQuad"
	//});
	anime({
		targets: titles,
		color: [
			{ value: "rgba(0,0,0,0)", delay: 800 },
			{ value: "rgba(29,33,253,0.4)", duration: 200 },
			{ value: "rgba(131,58,180,0.7)", duration: 200 },
			{ value: "rgba(180,58,173,0.9)", duration: 200 },
			{ value: "rgba(255,255,255,1)", duration: 200 }
		],
		easing: "easeInOutQuad"
	});
}

function openIntro(block) {
	var $content = $('#content'),
		$main = $('#main'),
		$main_articles = $main.children('article'),
		$article = $main_articles.filter('#' + block),
		$activated = $(".active");
	var time = 10;
	var activeUser = localStorage['activeUser'];
	if(block =="login" && activeUser){
		openIntro("profile");
		return;
	}
	if(block == "profile"  && !activeUser){
		openIntro("login");
		return;
	}

	data={"lastLocation":block}
	localStorage['lastLocation'] = JSON.stringify(data);

	$content.removeClass('animation');
	if (!$article[0].classList.contains("active")) {
		$article.show();

		if ($activated != null) {
			time = 600;
			anime({
				targets: ".active",
				maxHeight: '0em',
				opacity: {value:0,duration:200},
				easing: 'easeInOutQuad',
				duration: 400
			});
			setTimeout(function () {
				$activated.removeClass("active");
				//$texts.hide();
			}, 100);
		}


		setTimeout(function () {
			anime({
				targets: "#" + block,
				opacity: 1,
				maxHeight: '30em',
				easing: 'easeInOutQuad'
			});

			$activated.removeClass("active");
			$activated.hide();
			$article.addClass("active");
			showSentence($article[0]);
		}, time);
	}

}
(function ($) {

	var $window = $(window),
		$body = $('body'),
		$wrapper = $('#wrapper'),
		$header = $('#header'),
		$footer = $('#footer'),
		$main = $('#main'),
		$main_articles = $main.children('article');

	// Breakpoints.
	breakpoints({
		xlarge: ['1281px', '1680px'],
		large: ['981px', '1280px'],
		medium: ['737px', '980px'],
		small: ['481px', '736px'],
		xsmall: ['361px', '480px'],
		xxsmall: [null, '360px']
	});

	// Play initial animations on page load.
	$window.on('load', function () {
		window.setTimeout(function () {
			$body.removeClass('is-preload');
		}, 100);
	});

	// Fix: Flexbox min-height bug on IE.
	if (browser.name == 'ie') {

		var flexboxFixTimeoutId;

		$window.on('resize.flexbox-fix', function () {

			clearTimeout(flexboxFixTimeoutId);

			flexboxFixTimeoutId = setTimeout(function () {

				if ($wrapper.prop('scrollHeight') > $window.height())
					$wrapper.css('height', 'auto');
				else
					$wrapper.css('height', '100vh');

			}, 250);

		}).triggerHandler('resize.flexbox-fix');

	}

	// Scroll restoration.
	// This prevents the page from scrolling back to the top on a hashchange.
	if ('scrollRestoration' in history)
		history.scrollRestoration = 'manual';
	else {

		var oldScrollPos = 0,
			scrollPos = 0,
			$htmlbody = $('html,body');

		$window
			.on('scroll', function () {

				oldScrollPos = scrollPos;
				scrollPos = $htmlbody.scrollTop();

			})
			.on('hashchange', function () {
				$window.scrollTop(oldScrollPos);
			});

	}

	// Initialize.

	// Hide main, articles.
	//$main.hide();
	$main_articles.hide();


	// Initial article.
	if (location.hash != ''
		&& location.hash != '#')
		$window.on('load', function () {
			$main._show(location.hash.substr(1), true);
		});

})(jQuery);
