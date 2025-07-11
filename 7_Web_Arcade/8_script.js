const cat = document.getElementById("cat");
const obstacle = document.getElementById("obstacle");
const game = document.getElementById("window");
const scoreDisplay = document.getElementById("score")
const highScoreDisplay = document.getElementById("highscore");

let score = 0;
let highScore = 0;
let gameInterval = null;
let hasScored = false; // Simple flag to track if we've scored for current obstacle cycle

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
    if (gameInterval === null){
        startGame();
        randomizeObstacle(); // Randomize obstacle image on start
    }

    if (e.code === 'Space' && gameInterval !== null){
        jump();
    }
})

function randomizeObstacle() {
    const randomIndex = Math.floor(Math.random() * 4);
    const obstacleImages = [
        "8_imgs/cockroach.png",
        "8_imgs/bath.png",
        "8_imgs/syringe.png",
        "8_imgs/vacuum.png"
    ];
    obstacle.style.backgroundImage = `url('${obstacleImages[randomIndex]}')`;
}

function startGame() {
    score = 0;
    hasScored = false; // Reset scoring flag
    scoreDisplay.textContent = score;
    obstacle.style.animation = "obs-block 1.2s infinite linear";

    if (gameInterval) clearInterval(gameInterval);

    gameInterval = setInterval(() => {
        // Collision check - accounting for borders
        const catRect = cat.getBoundingClientRect();
        const obsRect = obstacle.getBoundingClientRect();
        
        // Adjust for borders and add small margin for better gameplay
        const margin = 4; // pixels of margin for better collision detection
        
        const catLeft = catRect.left + margin;
        const catRight = catRect.right - margin;
        const catTop = catRect.top + margin;
        const catBottom = catRect.bottom - margin;
        
        const obsLeft = obsRect.left;
        const obsRight = obsRect.right;
        const obsTop = obsRect.top;
        const obsBottom = obsRect.bottom;

        const isColliding = !(
            catTop > obsBottom ||
            catBottom < obsTop ||
            catRight < obsLeft ||
            catLeft > obsRight
        );

        if (isColliding) {
            gameOver();
        } else {
            // Check if obstacle has passed the cat (score when obstacle is avoided)
            // If obstacle has passed the cat and we haven't scored for this cycle yet
            if (obsRect.right < catRect.left && !hasScored) {
                score++;
                hasScored = true; // Mark that we've scored for this obstacle
                scoreDisplay.textContent = score;
            }
            
            // Reset scoring flag when obstacle starts a new cycle (goes back to right side)
            if (obsRect.left > 700) { // When obstacle is near the starting position
                hasScored = false;
            }
            if (obsRect.left > 1069) { // When obstacle is near the starting position
                hasScored = false;
                randomizeObstacle(); // Randomize obstacle image for next cycle
            }
        }
    }, 50); // Check more frequently for smoother detection
}

function gameOver() {
    if (score > highScore) {
        highScore = score;
        highScoreDisplay.textContent = highScore;
        }
    clearInterval(gameInterval);
    gameInterval = null; // Reset to null so game stops
    alert("💀 Game Over! Score: " + score);
    score = 0; // Reset score
    scoreDisplay.textContent = score;
    obstacle.style.animation = "none"; // Stop the obstacle animation
    obstacle.style.backgroundImage = '';
}

// Play/Restart Button Logic
document.getElementById("playBtn").addEventListener("click", () => {
    randomizeObstacle(); // Randomize obstacle image on start
    startGame();
});