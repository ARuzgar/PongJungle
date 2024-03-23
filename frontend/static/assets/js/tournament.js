
$("#tournamentForm").on('submit', function (e) {
    e.preventDefault();
    const form = document.getElementById('tournamentForm');
    const canvas = document.getElementById('gameCanvasT');
    const ctx = canvas.getContext('2d');
    let Players = [];
    Array.from(form.elements).forEach(function(input) {
        if (input.type === 'text') {
            Players.push(input.value);
        }
    });
    openIntro("pongTournament");
    tournamentLoop(Players);
    console.log(Players);
});

async function tournamentLoop(Players){
    const canvas = document.getElementById('gameCanvasT');
    const ctx = canvas.getContext('2d');
    const scale = window.devicePixelRatio;
    const paddleWidth = 15 * scale;
    const paddleHeight = 150 * scale;
    const paddleSpeed = 10* scale;
    const ballSize=3 * scale;
    const speed=10*scale;
    const accelerationFactor = 0.2;
    const maxSpeedIncreaseFactor = 3;
    const scoreElement1 = document.getElementById('player1-score');
    const scoreElement2 = document.getElementById('player2-score');
    const playerName1 = document.getElementById('player1Name');
    const playerName2 = document.getElementById('player2Name');
    while (Players.length > 1) {
        let winners = [];
        for (let i = 0; i < Players.length; i += 2) {
            const player1 = Players[i];
            const player2 = Players[i + 1];
            const randomDirection = Math.random() < 0.5 ? -1 : 1;
            let player1Score = 0;
            let player2Score = 0;
            
            let paddle1Y = canvas.height / 2 - paddleHeight / 2;
            let paddle2Y = canvas.height / 2 - paddleHeight / 2;
            let ballX = canvas.width / 2;
            let ballY = canvas.height / 2;
            let ballSpeedX = speed;
            let ballSpeedY = speed;
            let gameEnded = false;
            let Rwinner;
            scoreElement1.textContent = player1Score;
            scoreElement2.textContent = player2Score;
            playerName1.textContent = player1;
            playerName2.textContent = player2;
            ballSpeedX = speed * randomDirection;
            ballSpeedY = speed * randomDirection;

            let gameFinish = new Promise((resolve, reject) => {
                    window.draw=function () {
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
                    if (ballY + ballSize < 0 || ballY > canvas.height) {
                        ballSpeedY = -ballSpeedY;
                    }
                    if (ballX < paddleWidth && ballY > paddle1Y && ballY < paddle1Y + paddleHeight) {
                        ballSpeedX = -ballSpeedX;
                        ballSpeedX *= 1 + accelerationFactor;
                        ballSpeedY *= 1 + accelerationFactor;
                        ballSpeedX = Math.min(ballSpeedX, speed * maxSpeedIncreaseFactor);
                        ballSpeedY = Math.min(ballSpeedY, speed * maxSpeedIncreaseFactor);
                    }

                    if (ballX > canvas.width - paddleWidth && ballY > paddle2Y && ballY < paddle2Y + paddleHeight) {
                        ballSpeedX = -ballSpeedX;
                        ballSpeedX *= 1 + accelerationFactor;
                        ballSpeedY *= 1 + accelerationFactor;
                        ballSpeedX = Math.min(ballSpeedX, speed * maxSpeedIncreaseFactor);
                        ballSpeedY = Math.min(ballSpeedY, speed * maxSpeedIncreaseFactor);
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
                
                    if (player === 1) {
                        player1Score++;
                        scoreElement1.textContent = player1Score;
                    } else {
                        player2Score++;
                        scoreElement2.textContent = player2Score;
                    }
                
                    if (player1Score === 5 || player2Score === 5) {
                        gameEnded = true;
                        endGame();

                    }
                }
            
                function endGame() {
                    cancelAnimationFrame(requestId);
                    if (player1Score === 5) {
                        writeText(canvas,ctx,"Player 1 won!");
                        Rwinner = player1;
                    } else {
                        writeText(canvas,ctx,"Player 2 won!");
                        Rwinner = player2;
                    
                    }
                    resolve (Rwinner);
                }
            
                canvas.addEventListener('keydown', function(event) {
                    switch(event.key) {
                        case 'w':
                        case 'ArrowUp':
                        case 's':
                        case 'ArrowDown':
                            event.preventDefault();
                            break;
                        case 'Enter':
                            draw();
                            break;
                        case 'Escape':
                            cancelAnimationFrame(requestId);
                            break;
                    }        
                });
                let keysState = {
                    'w': false,
                    's': false,
                    'ArrowUp': false,
                    'ArrowDown': false,
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
                
                }
                
            })

            let winner = await gameFinish;
            winners.push(winner);
            console.log(winners);
            writeText(canvas, ctx, "Winner is " + winner + " Press 'Enter' to Start Next Match");
        }
        Players = winners.slice();

    }
    writeText(canvas, ctx, "Tournament Winner is: " + Players[0] + " 🎉");
    saveWinnerT(Players[0]);

}

$(document).ready(function () {
    const canvas = document.getElementById('gameCanvasT');
    const ctx = canvas.getContext('2d');
    const text = "Press 'Enter' to Start";
    
    var scale = window.devicePixelRatio;  
            
    canvas.width = Math.floor(600 * scale*2); 
    canvas.height = Math.floor(400 * scale*2); 

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
async function saveWinnerT(winner){
    const user=await getUserInfo();
    var data = {
		"username":user.username,
        "who_win": winner,
        "game_type":"Tournament"
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