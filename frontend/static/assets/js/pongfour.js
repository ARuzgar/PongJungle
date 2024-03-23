$(document).ready(function () {
    const canvas = document.getElementById('gameCanvasF');
    const ctx = canvas.getContext('2d');
    const text = "enter";
    
    var scale = window.devicePixelRatio;  
            
    canvas.width = Math.floor(600 * scale*2); 
    canvas.height = Math.floor(400 * scale*2); 

    writeIntro(canvas,ctx);
    
});
function writeIntro(canvas,ctx){
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.font = '50px Arial';
    ctx.fillStyle = 'white';
    ctx.textAlign = 'center';

    ctx.fillText("Press 'Enter' to Start", canvas.width / 2, 50);
    ctx.fillText("Controls:", canvas.width / 2, 110);
    ctx.fillText("player 1(left): w-s", canvas.width / 2, 170);
    ctx.fillText("player 2(right): Up-Down", canvas.width / 2, 240);
    ctx.fillText("player 3(up): 4-6", canvas.width / 2, 300);
    ctx.fillText("player 4(down): j-l", canvas.width / 2, 360);
}
function writeText(canvas,ctx,text){
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.font = '50px Source Sans Pro';
    ctx.fillStyle = 'white';
    ctx.imageSmoothingQuality = 'high';
    const textWidth = ctx.measureText(text).width;
    const x = (canvas.width - textWidth) / 2;
    const y = 50;
    
    ctx.fillText(text, x, y);

}
function pongfour(){
    const canvas = document.getElementById('gameCanvasF');
    const ctx = canvas.getContext('2d');
    const scale = window.devicePixelRatio;
    const paddleWidth = 15 * scale;
    const paddleHeight = 150 * scale;
    const paddleXWidth= 200 * scale;
    const paddleXHeight = 15 * scale;
    const paddleSpeed = 10* scale;
    const ballSize=10 * scale;
    const speed=4*scale;
    const scoreElement1 = document.getElementById('player1-scoreF');
    const scoreElement2 = document.getElementById('player2-scoreF');
    const scoreElement3 = document.getElementById('player3-scoreF');
    const scoreElement4 = document.getElementById('player4-scoreF');
    const accelerationFactor = 0.2;
    const maxSpeedIncreaseFactor = 3;
    const randomDirection = Math.random() < 0.5 ? -1 : 1;
    let player1Score = 0;
    let player2Score = 0;
    let player3Score = 0;
    let player4Score = 0;
    let paddle1Y = canvas.height / 2 - paddleHeight / 2;
    let paddle2Y = canvas.height / 2 - paddleHeight / 2;
    let paddle3X = canvas.width /2 - paddleXWidth / 2;
    let paddle4X = canvas.width / 2 - paddleXWidth / 2;
    let ballX = canvas.width / 2;
    let ballY = canvas.height / 2;
    let ballSpeedX;
    let ballSpeedY;
    let gameEnded = false;
    let scorer = 0;
    
    ballSpeedX = speed * randomDirection;
    ballSpeedY = speed * randomDirection;

    window.draw=function () {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw paddles
        ctx.fillStyle = 'white';
        ctx.fillRect(0, paddle1Y, paddleWidth, paddleHeight);
        ctx.fillRect(canvas.width - paddleWidth, paddle2Y, paddleWidth, paddleHeight);
        ctx.fillRect(paddle3X, 0, paddleXWidth, paddleXHeight);
        ctx.fillRect(paddle4X, canvas.height-paddleXHeight, paddleXWidth, paddleXHeight);

        // Draw ball
        ctx.beginPath();
        ctx.arc(ballX, ballY, ballSize, 0, Math.PI * 2);
        ctx.fill();

        // Ball movement
        ballX += ballSpeedX;
        ballY += ballSpeedY;

        // Collision detection
        if (ballX < paddleWidth && ballY > paddle1Y && ballY < paddle1Y + paddleHeight) {
            ballSpeedX = -ballSpeedX;
            ballSpeedX *= 1 + accelerationFactor;
            ballSpeedY *= 1 + accelerationFactor;
            ballSpeedX = Math.min(ballSpeedX, speed * maxSpeedIncreaseFactor);
            ballSpeedY = Math.min(ballSpeedY, speed * maxSpeedIncreaseFactor);
            scorer=1;
        }
        
        if (ballX > canvas.width - paddleWidth && ballY > paddle2Y && ballY < paddle2Y + paddleHeight) {
            ballSpeedX = -ballSpeedX;
            ballSpeedX *= 1 + accelerationFactor;
            ballSpeedY *= 1 + accelerationFactor;
            ballSpeedX = Math.min(ballSpeedX, speed * maxSpeedIncreaseFactor);
            ballSpeedY = Math.min(ballSpeedY, speed * maxSpeedIncreaseFactor);
            scorer=2;
        }
        
        if (ballY < paddleWidth && ballX > paddle3X && ballX < paddle3X + paddleXWidth) {
            ballSpeedY = -ballSpeedY;
            ballSpeedX *= 1 + accelerationFactor;
            ballSpeedY *= 1 + accelerationFactor;
            ballSpeedX = Math.min(ballSpeedX, speed * maxSpeedIncreaseFactor);
            ballSpeedY = Math.min(ballSpeedY, speed * maxSpeedIncreaseFactor);
            scorer=3;
        }
        
        if (ballY > canvas.height - paddleXHeight && ballX > paddle4X && ballX < paddle4X + paddleXWidth) {
            ballSpeedY = -ballSpeedY;
            ballSpeedX *= 1 + accelerationFactor;
            ballSpeedY *= 1 + accelerationFactor;
            ballSpeedX = Math.min(ballSpeedX, speed * maxSpeedIncreaseFactor);
            ballSpeedY = Math.min(ballSpeedY, speed * maxSpeedIncreaseFactor);
            scorer=4;
        }
        

        // Game over condition
        if (ballX < 0 || ballX >canvas.width) {
            ballX = canvas.width / 2;
            ballY = canvas.height / 2;
            updateScore(scorer);
            scorer=0;
        } else if (ballY > canvas.height || ballY < 0) {
            ballX = canvas.width / 2;
            ballY = canvas.height / 2;
            updateScore(scorer);
            scorer=0;
        }
        if(!gameEnded){
            requestId = requestAnimationFrame(draw);
            handleKeyActions();
        }
    }

    function updateScore(player) {
        if (gameEnded) {
            return;
        }
        const randomDirection = Math.random() < 0.5 ? -1 : 1;
    
        ballSpeedX = speed * randomDirection;
        ballSpeedY = speed * randomDirection;
    
        switch (player){
            case 1:
                player1Score++;
                scoreElement1.textContent = player1Score;
                break;
            case 2:
                player2Score++;
                scoreElement2.textContent = player2Score;
                break;
            case 3:
                player3Score++;
                scoreElement3.textContent = player3Score;
                break;
            case 4:
                player4Score++;
                scoreElement4.textContent = player4Score;
                break;
        }

    
        if (player1Score === 5 || player2Score === 5 || player3Score === 5 || player4Score === 5) {
            gameEnded = true;
            endGame();
            
        }
    }

    function endGame() {
        cancelAnimationFrame(requestId);
        if (player1Score === 5) {
            writeText(canvas,ctx,"Player 1 won!");
            saveWinnerF("Player1");
        }else if(player2Score === 5){
            writeText(canvas,ctx,"Player 2 won!");
            saveWinnerF("Player2");
        }else if(player3Score === 5){
            writeText(canvas,ctx,"Player 3 won!");
            saveWinnerF("Player3");
        }
        else if(player4Score === 5){
            writeText(canvas,ctx,"Player 4 won!");
            saveWinnerF("Player4");
        }
    }

    document.addEventListener('keydown', function(event) {
        switch(event.key) {
            case 'ArrowUp':
            case 'ArrowDown':
                event.preventDefault();
                break;
            case 'Enter':
                draw();
                break;
            case 'Escape':
                cancelAnimationFrame(requestId);
        }        
    });
    let keysState = {
        'w': false,
        's': false,
        'ArrowUp': false,
        'ArrowDown': false,
        'j':false,
        'l':false,
        'Enter':false,
        'Escape':false,
    };
    window.addEventListener('keydown', function(event) {
        keysState[event.key] = true;
    });
    
    window.addEventListener('keyup', function(event) {
        keysState[event.key] = false;
    });
    function handleKeyActions() {
        if (keysState['w']) {
            if (paddle1Y > 0) {
                paddle1Y -= paddleSpeed;
            }
        }
    
        if (keysState['s']) {
            if (paddle1Y + paddleHeight < canvas.height) {
                paddle1Y += paddleSpeed;
            }
        }
    
        if (keysState['ArrowUp']) {
            if (paddle2Y > 0) {
                paddle2Y -= paddleSpeed;
            }
        }
    
        if (keysState['ArrowDown']) {
            if (paddle2Y + paddleHeight < canvas.height) {
                paddle2Y += paddleSpeed;
            }
        }
        if (keysState['4']) {
            if (paddle3X > 0) {
                paddle3X -= paddleSpeed;
            }
        }
        
        if (keysState['6']) {
            if (paddle3X + paddleXWidth < canvas.width) {
                paddle3X += paddleSpeed;
            }
        }
        if (keysState['j']) {
            console.log("j");
            if (paddle4X > 0) {
                paddle4X -= paddleSpeed;
            }
        }
        
        if (keysState['l']) {
            if (paddle4X + paddleXWidth < canvas.width) {
                paddle4X += paddleSpeed;
            }
        }
    
    }
}

async function saveWinnerF(winner){
    const user=await getUserInfo();
    var data = {
		"username":user.username,
        "who_win": winner,
        "game_type":"Four Player"
	};
	fetch('https://peng.com.tr/backend/match/', {
        method: 'POST',
        headers: {
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
        console.log(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
