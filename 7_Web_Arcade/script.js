const game = document.getElementById("snake");
const scor = document.getElementById("score");
let blocksize = 33;
let total_row = 15;
let total_col = 15;
let context;

let cat_x = 3 * blocksize;
let cat_y = 7 * blocksize;
let catBody = [];
let catLen = 0;
const catImg = new Image();
catImg.src = "cat.png";
const catClosed = new Image();
catClosed.src = "cat-closed.png"

let speedX = 0;
let speedY = 0;

let fish_x;
let fish_y;
let ate = 0;
const fishImg = new Image();
fishImg.src = "fih.png";


let gameOver = false;
let isEating = false;

window.onload = function () {
    // set board
    game.height = total_row * blocksize;
    game.width = total_col * blocksize;
    context = game.getContext("2d"); //render in canvas as 2d
    boardPattern();
    context.drawImage(catImg, cat_x, cat_y, blocksize, blocksize);
    placeFish();
    document.addEventListener("keyup", changeDirection); //if click run changeDirection
    setInterval(update, 1000 / 6); //change the number in back to adjust speed
}

function boardPattern(){
    // if sum even use dark
    for(let row = 0; row < total_row; row++){
        for(let col = 0; col < total_col; col++){
            let sum = row + col;

            context.fillStyle = (sum % 2 === 0) ? "#FFDCDC" : "#FFF2EB";
            context.fillRect(col * blocksize, row * blocksize, blocksize, blocksize);
        }
    }
}

function update() {
    if(gameOver){
        return;
    }

    boardPattern();

    // Move the cat
    cat_x += speedX * blocksize;
    cat_y += speedY * blocksize;

    // Check collision
    if (
        cat_x < 0 || 
        cat_x >= total_col * blocksize || 
        cat_y < 0 || 
        cat_y >= total_row * blocksize
    ) {
        gameOver = true;
        
        alert("Game Over! The cat hit the wall.");
    }

    for (let i = 1; i < catBody.length; i++) {
        if (cat_x === catBody[i][0] && cat_y === catBody[i][1]) {
            gameOver = true;
            alert("Game Over! The cat bit itself.");
            return;
        }
    }

    // if ate
    if (cat_x == fish_x && cat_y == fish_y) {
        placeFish();
        catLen++;
        isEating = true;
        ate++;
        scor.textContent = ate;

        // Reset eating state after 200ms
        setTimeout(() => {
            isEating = false;
        }, 200);
    }

    context.fillStyle = "#f9c5d1";
    for (let i = 0; i < catBody.length; i++) {
        context.fillRect(catBody[i][0], catBody[i][1], blocksize, blocksize);
    }

    // Move the body: add current head position at the front
    catBody.unshift([cat_x, cat_y]);

    // Trim body to match current length
    if (catBody.length > catLen) {
        catBody.pop();
    }
    
    // set the food
    context.drawImage(fishImg, fish_x, fish_y, blocksize, blocksize);

    // Draw the cat head
    context.drawImage(catImg, cat_x, cat_y, blocksize, blocksize);

    // Draw cat head based on state
    if (isEating) {
        context.drawImage(catClosed, cat_x, cat_y, blocksize, blocksize);
    } else {
        context.drawImage(catImg, cat_x, cat_y, blocksize, blocksize);
    }

}

function placeFish(){
    // place fih in random position
    // Math.random return 0-1, multiply with total_col and floor it to get the whole index, multiply with blocksize
    let valid = false;

    while (!valid) {
        fish_x = Math.floor(Math.random() * total_col) * blocksize;
        fish_y = Math.floor(Math.random() * total_row) * blocksize;

        valid = true;

        // Check if fish is inside cat body
        for (let i = 0; i < catBody.length; i++) {
            if (fish_x === catBody[i][0] && fish_y === catBody[i][1]) {
                valid = false;
                break;
            }
        }

        // Also make sure it doesn't spawn on the cat's current head
        if (fish_x === cat_x && fish_y === cat_y) {
            valid = false;
        }
    }
}

function changeDirection(e){
    if (e.code == "ArrowUp" && speedY != 1) { 
        speedX = 0;
        speedY = -1;
    }
    else if (e.code == "ArrowDown" && speedY != -1) {
        speedX = 0;
        speedY = 1;
    }
    else if (e.code == "ArrowLeft" && speedX != 1) {
        speedX = -1;
        speedY = 0;
    }
    else if (e.code == "ArrowRight" && speedX != -1) { 
        speedX = 1;
        speedY = 0;
    }
}

let highScore = 0;

// Play/Restart Button Logic
document.getElementById("playBtn").addEventListener("click", () => {
    // Update high score if needed
    if (ate > highScore) {
        highScore = ate;
        document.getElementById("highscore").textContent = highScore;
    }

    // Reset everything
    cat_x = 5 * blocksize;
    cat_y = 9 * blocksize;
    speedX = 0;
    speedY = 0;
    catBody = [];
    catLen = 0;
    ate = 0;
    isEating = false;
    gameOver = false;
    scor.textContent = 0;

    placeFish(); // put fish somewhere new
    update(); // refresh display
});
