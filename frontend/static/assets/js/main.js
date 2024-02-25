class chatUser {
	constructor(id, name, pp, lobby) {
		this.id = id;
		this.name = name;
		this.pp = pp;
		this.lobby = lobby;
	}
}
dragElement();
createChatUsers();

function createChatUsers() {
	const chat = document.querySelector("#chat");

	let Users = [
		new chatUser(0, "penguen", penguinImagePath, null),
		new chatUser(1, "penguen2", penguin2ImagePath, null),
	];

	Users.forEach(User => {
		chat.innerHTML += ("<button type='button' class='btn btn-info chatUser' id='User" + User.id + "'><img class='img-fluid' style='pointer-events: none;' src='" + User.pp + "'></button>");
	});
}

function chatExtend() {
	const chat = document.querySelector("#chat");

	let chatUserBlocks = document.getElementsByClassName("chatUser");
	if (chatUserBlocks[0].style.opacity == 0) {
		anime({
			targets: chatUserBlocks,
			translateY: function (el, i) {
				return 4.5 * (1 + i++) + "em";
			},
			rotate: 360,
			borderRadius: '25%',
			duration: 1000,
			delay: function (el, i, l) {
				return i * 200;
			},
			opacity: 1,
		});
	}
	else {
		anime({
			targets: chatUserBlocks,
			translateY: 0,
			rotate: 0,
			borderRadius: '50%',
			duration: 1000,
			delay: function (el, i, l) {
				return i * 200;
			},
			opacity: 0,
		});
	}
}

function dragElement() {
	const container = document.querySelector("#chat");
	var myCache = localStorage['chatPosition'];
	var isMoved = false;
	if (myCache) {
		var chatPosition = JSON.parse(myCache);
		container.style.left = chatPosition["chatPositionX"];
		container.style.top = chatPosition["chatPositionY"];
	}
	function onMouseDrag({ movementX, movementY }) {
		isMoved = true;
		let getContainerStyle = window.getComputedStyle(container);
		let leftValue = parseInt(getContainerStyle.left);
		let topValue = parseInt(getContainerStyle.top);
		container.style.left = `${leftValue + movementX}px`;
		container.style.top = `${topValue + movementY}px`;
	}
	container.addEventListener("mousedown", () => {
		document.addEventListener("mousemove", onMouseDrag);
	});
	container.addEventListener("mouseup", () => {
		if (!isMoved)
			chatExtend();
		document.removeEventListener("mousemove", onMouseDrag);
		var Temp = { chatPositionX: container.style.left, chatPositionY: container.style.top };
		localStorage['chatPosition'] = JSON.stringify(Temp);
		isMoved = false;
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
	anime({
		targets: titles,
		background: [
			{ value: "linear-gradient(90deg, rgba(180,58,173,1) 0%, rgba(131,58,180,1) 38%, rgba(29,33,253,1) 70%, rgba(115,113,124,0) 100%", duration: 300, delay: 500 },
			{ value: "linear-gradient(90deg, rgba(180,58,173,1) 50%, rgba(131,58,180,1) 78%, rgba(29,33,253,1) 100%", duration: 300 },
			{ value: "linear-gradient(90deg, rgba(180,58,173,1) 78%, rgba(131,58,180,1) 100%", duration: 0 },
			{ value: "linear-gradient(270deg, rgba(180,58,173,1) 78%, rgba(131,58,180,1) 100%, rgba(115,113,124,0) 100%", duration: 0 },
			{ value: "linear-gradient(270deg, rgba(180,58,173,1) 50%, rgba(131,58,180,1) 78%, rgba(115,113,124,0) 100%", duration: 200 },
			{ value: "linear-gradient(270deg, rgba(180,58,173,1) 0%, rgba(131,58,180,1) 0%, rgba(115,113,124,0) 50%", duration: 200 },
			{ value: "linear-gradient(270deg, rgba(180,58,173,1) 0%, rgba(131,58,180,1) 0%, rgba(115,113,124,0) 0%", duration: 200 }
		],
		easing: "easeInOutQuad"
	});
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

	$content.removeClass('animation');
	if (!$article[0].classList.contains("active")) {
		$article.show();

		if ($activated != null) {
			time = 600;
			anime({
				targets: ".active",
				maxHeight: '0em',
				opacity: 0,
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
/*function openIntro(block){
	var	$window = $(window),
		$body = $('body'),
		$inner =$('#inner'),
		$content =$('#content'),
		$main = $('#main'),
		$main_articles = $main.children('article'),
		$article = $main_articles.filter('#' + block);
	var $actives = $(".active");
	console.log($actives);

	$inner.hide();
	$content.removeClass('animation');

	setTimeout(function(){
		
		$actives.removeClass("active").addClass("deactive");
		$main.removeClass('hide').addClass('animation');
	},100);
	
	setTimeout(function(){
		$article.removeClass("deactive").addClass('active');
		
		$article.show();
	},100);
	setTimeout(function(){
		$content.addClass('animation');

	},400);
		
		
		
}*/
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
	openIntro("home");


	// Initial article.
	if (location.hash != ''
		&& location.hash != '#')
		$window.on('load', function () {
			$main._show(location.hash.substr(1), true);
		});

})(jQuery);