$(document).ready(function () {
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    const text = "Press 'Enter' to Start";
    
    var scale = window.devicePixelRatio;  
            
    canvas.width = Math.floor(600 * scale); 
    canvas.height = Math.floor(400 * scale); 

    writeText(canvas,ctx,text);
    
});
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
function pong(){
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');

    const paddleWidth = 20;
    const paddleHeight = 100;
    const paddleSpeed = 10;
    const ballSize=8;
    let player1Score = 0;
    let player2Score = 0;
    const scoreElement1 = document.getElementById('player1-score');
    const scoreElement2 = document.getElementById('player2-score');
    let paddle1Y = canvas.height / 2 - paddleHeight / 2;
    let paddle2Y = canvas.height / 2 - paddleHeight / 2;
    let ballX = canvas.width / 2;
    let ballY = canvas.height / 2;
    let ballSpeedX = 3;
    let ballSpeedY = 3;
    let gameEnded = false;
    


    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw paddles
        ctx.fillStyle = 'white';
        ctx.fillRect(0, paddle1Y, paddleWidth, paddleHeight);
        ctx.fillRect(canvas.width - paddleWidth, paddle2Y, paddleWidth, paddleHeight);

        // Draw ball
        ctx.beginPath();
        ctx.arc(ballX, ballY, ballSize, 0, Math.PI * 2);
        ctx.fill();

        // Ball movement
        ballX += ballSpeedX;
        ballY += ballSpeedY;

        // Collision detection
        if (ballY < 0 || ballY > canvas.height) {
            ballSpeedY = -ballSpeedY;
        }
        if (ballX < paddleWidth && ballY > paddle1Y && ballY < paddle1Y + paddleHeight) {
            ballSpeedX = -ballSpeedX;
        }
        if (ballX > canvas.width - paddleWidth && ballY > paddle2Y && ballY < paddle2Y + paddleHeight) {
            ballSpeedX = -ballSpeedX;
        }

        // Game over condition
        if (ballX < 0 || ballX > canvas.width) {
            if (ballX < 0) {
                updateScore(2);
            } else if (ballX > canvas.width) {
                updateScore(1);
            }
            ballX = canvas.width / 2;
            ballY = canvas.height / 2;
            ballSpeedX = 2;
            ballSpeedY = 2;
        }

        requestAnimationFrame(draw);
    }

    function updateScore(player) {
        if (gameEnded) {
            return; // Oyun zaten bitmişse skor güncellemelerini engelle
        }
    
        if (player === 1) {
            player1Score++;
            scoreElement1.textContent = player1Score;
        } else {
            player2Score++;
            scoreElement2.textContent = player2Score;
        }
    
        if (player1Score === 10 || player2Score === 10) {
            gameEnded = true;
            endGame();
        }
    }

    function endGame() {
        // Oyun bittiğinde yapılacak işlemler
        if (player1Score === 10) {
            writeText(canvas,ctx,"Player 1 won!");
        } else {
            writeText(canvas,ctx,"Player 2 won!");
        }
    }

    document.addEventListener('keydown', function(event) {
        switch(event.key) {
            case 'w':
            case 'ArrowUp':
            case 's':
            case 'ArrowDown':
                event.preventDefault();
                break;
        }
        if (event.key === 'w') {
            if (paddle1Y - paddleHeight / 2 > 0) {
                paddle1Y -= paddleSpeed;
            }
        } else if (event.key === 's') {
            if (paddle1Y + (paddleHeight / 2 + 30) < canvas.height) {
                paddle1Y += paddleSpeed;
            }
        } if (event.key === 'ArrowUp') {
            if (paddle2Y - paddleHeight / 2 > 0) {
                paddle2Y -= paddleSpeed;
            }
        } else if (event.key === 'ArrowDown') {
            if (paddle2Y + (paddleHeight / 2 + 30) < canvas.height) {
                paddle2Y += paddleSpeed;
            }
        } else if (event.key === 'Enter') {
            draw();
        } else if (event.key === 'Escape') {
            cancelAnimationFrame(window.draw);
        }
        
    });
}

