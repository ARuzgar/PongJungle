$(document).ready(function () {
	
	//var chatLocation =localStorage['chatPosition'];
	//if(chatLocation){
	//	var chatPosition=JSON.parse(chatLocation);
	//	const container = document.querySelector("#chat");
	//	container.style.left = chatPosition["chatPositionX"];
	//	container.style.top = chatPosition["chatPositionY"];
	//}
	var activeUser = localStorage['activeUser'];
	var lastLocation = localStorage['lastLocation'];
	if(lastLocation)
	{
		if(activeUser){
			checkToken();
			var Location = JSON.parse(lastLocation);
			openIntro(Location["lastLocation"]);
		}
		else{
			openIntro("login");

		}
		
	}
	else{
		console.log("lel");
		openIntro("login");
	}
	if(activeUser)
	{
		checkToken();
		var t_activeUser = JSON.parse(activeUser);
		loginSuccess(t_activeUser["token"]);
	}
	else if(JSON.parse(lastLocation)["lastLocation"] != "login"){
		//openIntro("login");

	}
	
	var Curl = window.location.href;
	const urlParams = new URLSearchParams(new URL(Curl).search);
	const code = urlParams.get('code');
	if(code)
	{
		auth42API(code);
	}
	$("#login42").on('click',function(e){
		window.location.href="https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-272a7d972a922c63919b4411aff1da6abf64ec93eb38804b51427a0c0fbf86ea&redirect_uri=https%3A%2F%2Fpeng.com.tr%2Flogin%2F&response_type=code";
	});
	$("#searchUser").on('click',function(e){
		var activeUser = localStorage['activeUser'];
		SearchUser(JSON.parse(activeUser)["token"].access);
	})
	$("#MatchHistory").on('click',function(e){
		openIntro("matchHistory")
		MatchHistory();
	})
	

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
	document.getElementById("emailSetting").addEventListener("focusout", function() {
		var email = document.getElementById("emailSetting").value;
		var emailFormat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
		var errorEmail = document.getElementById("errorEmailUpdate");

		if (!email.match(emailFormat)) {
			errorEmail.textContent = "Lütfen geçerli bir eposta adresi girin.";
		} else {
			errorEmail.textContent = "";
		}
	});

	document.getElementById("passwordSetting").addEventListener("focusout", function() {
		var password = document.getElementById("passwordSetting").value;
		var passwordFormat = /^(?=.*\d)(?=.*[a-zA-Z]).{8,}$/;
		var errorPassword = document.getElementById("errorPasswordUpdate");

		if (!password.match(passwordFormat)) {
			errorPassword.textContent = "Parolanız en az 8 karakter uzunluğunda olmalı ve en az 1 harf ve 1 sayı içermelidir.";
		} else {
			errorPassword.textContent = "";
		}
	});
});
async function MatchHistory(username){

	var user = await getUserInfo();
    var player = username || user.username; // Eğer username belirtilmemişse user.username kullan

	fetch('https://peng.com.tr/backend/match/?username='+encodeURIComponent(player), {	
		method: 'GET',
        headers: {},
		
	})
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error(data.message);
        }
    })
    .then(data => {
		if(data.data.length > 0){
			document.getElementById("noMatch").style.display="none";
			document.getElementById("matchTable").style.display="";
			var table= document.getElementById("matchTableBody");
			var html="";
			for(var i=0; i< data.data.length;i++){
				html+="<tr><td>"+data.data[i].who_win+"</td>\n"+"<td>"+data.data[i].date_played+"</td>\n"+"<td>"+data.data[i].game_type+"</td></tr>\n"
			}
			table.innerHTML=html;
		}
		else
		{
			document.getElementById("matchTable").style.display="none";
			document.getElementById("noMatch").style.display="";
		}
		
    })
    .catch(error => {
        console.error('Error:', error);
		document.getElementById("matchTable").style.display="none";
		document.getElementById("noMatch").style.display="";
    });

}
function checkToken(){
	
	const activeUserData = JSON.parse(localStorage.getItem('activeUser'));

	fetch('https://peng.com.tr/api42/auth/check/user/', {	
		method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + activeUserData.token.access,
			'Content-Type': 'application/json',
        },
		body: {"refresh_token": activeUserData.token.refresh}
	})
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
			
			localStorage.removeItem("activeUser");
        }
    });
}

//apies

//Friend add

function addFriend(token,friend_user){
	var data = {
		"friend_username":friend_user
	};
	fetch('https://peng.com.tr/api42/auth/friend/add/', {
                method: 'POST',
                headers: {
                    'Authorization': 'Bearer ' + token,
					'Content-Type': 'application/json'
                },
                body: JSON.stringify(data),
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error(data.message);
                }
            })
            .then(data => {
            })
            .catch(error => {
                console.error('Error:', error);
            });
}
// List Friend

function listFriend(token){
	fetch('https://peng.com.tr/api42/auth/friend/list/', {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + token,
        },
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error(data.message);
        }
    })
    .then(data => {
		if(data.data.length > 0){
			document.getElementById("noFriend").style.display="none";
			document.getElementById("friendTable").style.display="";
			var table= document.getElementById("friendTableBody");
			var html="";
			for(var i=0; i< data.data.length;i++){
				html+="<tr><td><a onclick=\"openIntro(\'matchHistory\');MatchHistory(\'"+data.data[i].username+"\')\">"+data.data[i].username+"</a></td>\n"+"<td>"+data.data[i].online_status+"</td></tr>\n"
			}
			table.innerHTML=html;
		}
		else
		{
			document.getElementById("friendTable").style.display="none";
			document.getElementById("noFriend").style.display="";
		}
		
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function SearchUser(token) {
    var queryValue = document.getElementById("searchUserText").value;
    var url = 'https://peng.com.tr/api42/auth/search/user/?query=' + encodeURIComponent(queryValue);

    fetch(url, {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Failed to fetch');
        }
    })
    .then(data => {
		var table = document.getElementById("searchUserTable");
		var users = data.data;
		var html="<tbody>\n"
	  					
		for(var i=0; i< users.length;i++){
			html+="<tr><td id=user"+i+" name="+data.data[i].username+">"+users[i].username+"</td>"+"<td><button type='submit' id='userButton"+i+"' class='btn btn-primary'>Add Friend</button></td></tr>\n"
		}
		html +="</tbody>"
		table.innerHTML=html;
		const buttons = document.querySelectorAll("[id^='userButton']");

		buttons.forEach(button => {
		    button.addEventListener('click', function() {
				button.disabled=true;
		        const userId = parseInt(this.id.replace('userButton', ''), 10);
				var friend_user=document.getElementById("user"+userId).innerHTML;
				addFriend(token,friend_user);
    		});
		});
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
//42 Auth

function auth42API(code){
	data ={
		code: encodeURIComponent(code)
	};
    fetch('https://peng.com.tr/api42/auth/ft_auth/',{
		method: 'POSt',
    	headers: {
    	    'Content-Type': 'application/json'
    	},
		body: JSON.stringify(data)
	})
	.then(response => {
		if (response.ok) {
			return response.json();
		} else {
			throw new Error('42 failed');
		}
		})
    	.then(data => {
			if(data.success=="True")
			{
    	    	loginSuccess(data.data.token);
				openIntro("profile");
				window.location.href="https://peng.com.tr";
			}
    	})
    	.catch(error => {
    	    console.error('Veri alınamadı: ', error);
    	});
}
//Register

$('#signupForm').on('submit', function (e) {
    e.preventDefault();

    var formData = {
        username: document.getElementById('usernameRegister').value,
        fullname: document.getElementById('fullnameRegister').value,
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
        throw new Error('register failed');
    }
    })
    .then(data => {
    // Gelen veriyi kontrol et
    if (data) {
		document.getElementById("loginSwitch").click();
    } else {
        console.log('No message found in response data.');
    }
    })
    .catch(error => {
    console.error('Error:', error);
    });
});

//Login
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
        var token=data.data.token;

        loginSuccess(token);
        openIntro("profile");
    } else {
        console.log('No message found in response data.');
    }
    })
    .catch(error => {
    console.error('Error:', error);
    });
});

//Logout
$("#logOut").on('click',function(e){
	const activeUserData = JSON.parse(localStorage.getItem('activeUser'));
	login_menu=document.getElementById("menuLogin");
	login_menu.innerHTML="<a href='#' onclick=\"openIntro('login')\">Login</a>"
	fetch('https://peng.com.tr/api42/auth/logout/', {	
		method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + activeUserData.token.access,
			'Content-Type': 'application/json',
        },
		body: JSON.stringify({"refresh_token": activeUserData.token.refresh})
	})
	.then(response => {
		if (response.ok) {
			return response.json();
		} else {
			throw new Error('Network response was not ok.');
		}
	})
	.catch(error => {
		console.error('Error:', error);
	});
	
	localStorage.removeItem("activeUser");
	openIntro("login");

});
//Profile Update
$('#profileSettingForm').on('submit', function (e) {
    e.preventDefault();
    const token = JSON.parse(localStorage.getItem('activeUser')).token.access;

    const fileInput = document.getElementById('profilePictureSetting');
	if(fileInput.files.length > 0){
		checkImage();

		const file = fileInput.files[0];
		const maxDimension = 200;

		const img = new Image();
		img.src = URL.createObjectURL(file);
		img.onload = function() {
    		let width = this.width;
    		let height = this.height;

    	let canvas = document.createElement('canvas');
    	let ctx = canvas.getContext('2d');
    	let finalWidth, finalHeight;

    	if (width > height) {
    	    finalWidth = maxDimension;
    	    finalHeight = Math.round(maxDimension * height / width);
    	} else {
    	    finalHeight = maxDimension;
    	    finalWidth = Math.round(maxDimension * width / height);
    	}

    	canvas.width = finalWidth;
    	canvas.height = finalHeight;

    	ctx.drawImage(this, 0, 0, width, height, 0, 0, finalWidth, finalHeight);

		canvas.toBlob((blob) => {
			const file = blobToFile(blob, 'profile_image.jpg');
			const formData = new FormData();
			formData.append("profile_picture", file);
			formData.append("type", file.type);
			formData.append("fullname", document.getElementById("fullNameSetting").value);
			formData.append("email", document.getElementById("emailSetting").value);
			formData.append("password", document.getElementById("passwordSetting").value);		
			updateUserAPI(token, formData);
		}, file.type);
    };
	} else {
		const formData = new FormData();
		formData.append('profile_picture', "");
		formData.append('type', "");
		formData.append('fullname', document.getElementById('fullNameSetting').value);
		formData.append('email', document.getElementById('emailSetting').value);
		formData.append('password', document.getElementById('passwordSetting').value);
	
		updateUserAPI(token,formData);
	}
	function blobToFile(blob, fileName) {
		const file = new File([blob], fileName, { type: blob.type });
		return file;
	}
});

function updateUserAPI(token,formData){
	
	fetch('https://peng.com.tr/api42/auth/update/user/', {
                method: 'PUT',
                headers: {
                    'Authorization': 'Bearer ' + token,
                },
                body: formData
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error(data.message);
                }
            })
            .then(data => {
				openIntro("profile");
            })
            .catch(error => {
                console.error('Error:', error);
            });
}
//Get User İnfo
async function getUserInfo() {
    const activeUserData = JSON.parse(localStorage.getItem('activeUser'));

    const response =await fetch('https://peng.com.tr/api42/auth/query/user/', {
        method: 'GET',
        headers: {
            'Authorization': "Bearer " + activeUserData.token.access,
            'Content-Type': 'application/json'
        },
    })
	const data = await response.json();
	return data.data;
    
}
//apies ends


//dragElement();


function showErrorMessage(message) {
	const errorDiv = document.createElement('div');
	errorDiv.innerHTML = "<h4 style='margin: 1rem 0 1rem 0;'>"+message+"</h4>";
	errorDiv.classList.add('d-flex', 'justify-content-center', 'align-items-center','error-message');

	const form = document.getElementById('loginForm');
	form.insertBefore(errorDiv, form.firstChild);
}

async function loginSuccess(token){
	data={
		"token":token
	}
	localStorage['activeUser'] = JSON.stringify(data);
	const user=await getUserInfo();
	login_menu=document.getElementById("menuLogin");
	Profile_picture=document.getElementById("profilePicture");
	profile_name=document.getElementById("profileName");
	if(login){
		login_menu.innerHTML="<a href='#' onclick=\"openIntro('profile')\">Profile</a>"
		profile_name.innerHTML=user.username;
		Profile_picture.src=user.profile_picture;
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
		if(!activeUser && block !="login")
		{
			openIntro("login");
			return;
		}
		if(block =="login" && activeUser){
			openIntro("profile");
			return;
		}
		if(block == "profile"  && !activeUser){
			openIntro("login");
			return;
		}
		if(block == "friends")
			listFriend(JSON.parse(localStorage.getItem('activeUser')).token.access);
		if(block =="pongClassic")
			pong();
		if(block =="pongFour")
			pongfour();
		
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

function checkImage(){
	const fileInput = document.getElementById('profilePictureSetting');
    

    if (!fileInput.files) {
        alert('Lütfen bir dosya seçin.');
        return;
    }
	
	const profilePicture = fileInput.files[0];
    const imageType = /image.*/;

    if (!profilePicture.type.match(imageType)) {
        alert('Sadece PNG ve JPEG dosyaları desteklenmektedir.');
        return;
    }

    const reader = new FileReader();

    reader.onload = function(e) {
        const img = new Image();
        img.src = e.target.result;

        img.onload = function() {
            let width = img.width;
            let height = img.height;

            let canvas = document.createElement('canvas');
            let ctx = canvas.getContext('2d');

            if (width > height) {
                canvas.width = 150;
                canvas.height = 150 * (height / width);
                ctx.drawImage(img, 0, (height - width) / 2, width, width, 0, 0, 150, 150);
            } else {
                canvas.width = 150 * (width / height);
                canvas.height = 150;
                ctx.drawImage(img, (width - height) / 2, 0, height, height, 0, 0, 150, 150);
            }

            const dataURL = canvas.toDataURL('image/png');

		};

    };

    reader.readAsDataURL(profilePicture);
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
