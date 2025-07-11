const cat = document.getElementById("cat");
const obstacle = document.getElementById("obstacle");
const game = document.getElementById("window");
const scoreDisplay = document.getElementById("score")
const highScoreDisplay = document.getElementById("highscore");

let score = 0;
let highScore = 0;
let gameInterval = null;

// jump when got class jump for 3 milisecs
function jump() {
    if(!cat.classList.contains("jump")){

        cat.classList.add('jump');

        setTimeout(() => {
            cat.classList.remove('jump');
            void cat.offsetWidth;
        }, 300);
    }
}

document.addEventListener('keydown', (e) => {
    if (gameInterval = null){
        startGame();
    }
    if (e.code = 'space'){
        jump();
    }
})

function startGame() {
    score = 0;
    scoreDisplay.textContent = score;
    obstacle.style.backgroundImage = "url('8_imgs/cockroach.png')";
    obstacle.style.animation = "obs-block 1.2s infinite linear";

    if (gameInterval) clearInterval(gameInterval);

    gameInterval = setInterval(() => {
        // Collision check
        const catRect = cat.getBoundingClientRect();
        const obsRect = obstacle.getBoundingClientRect();

        const isColliding = !(
            catRect.top > obsRect.bottom ||
            catRect.bottom < obsRect.top ||
            catRect.right < obsRect.left ||
            catRect.left > obsRect.right
        );

        if (isColliding) {
            gameOver();
        } else {
            score++;
            scoreDisplay.textContent = score;
            if (score > highScore) {
                highScore = score;
                highScoreDisplay.textContent = highScore;
            }
        }
    }, 300); // Check collision every 300ms
}

function gameOver() {
  clearInterval(gameInterval);
  alert("💀 Game Over! Score: " + score);
}

// Play/Restart Button Logic
document.getElementById("playBtn").addEventListener("click", () => {
    // Update high score if needed
    if (score > highScore) {
        highScore = score;
        document.getElementById("highscore").textContent = highScore;
    }

    startGame();

});