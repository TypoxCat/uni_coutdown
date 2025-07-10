let timer = true;
let startTime = Date.now();
let mins = 0;
let secs = 0;
// // // one second interval
let interval = setInterval(updateTimer, 1000);

var scrollCount = 0;
let scrollTimeout;
console.log("✅ Anti-Doomscroll content script is running!");

function blocker(){
    clearInterval(interval);
    const blocker = document.createElement("div");
    blocker.style.position = "fixed";
    blocker.style.top = "0";
    blocker.style.left = "0";
    blocker.style.width = "100%";
    blocker.style.height = "100%";
    blocker.style.backgroundColor = "rgba(0, 0, 0)";
    blocker.style.color = "#fff";
    blocker.style.zIndex = "9999";
    blocker.style.display = "flex";
    blocker.style.flexDirection = "column";
    blocker.style.justifyContent = "center";
    blocker.style.alignItems = "center";
    blocker.style.fontSize = "24px";
    blocker.innerHTML = `
    <p>You've been scrolling for too long</p>
    <p>Take a break. Breathe. Touch some grass 🌱</p>
    <p>The exit button will be out in 20 seconds</p>
    `;
    document.body.appendChild(blocker);

    setTimeout(() => {
        blocker.innerHTML = `
        <p>Okay now u can continue nya</p>
        <button id="dismiss">I'm good now</button>
        `;

        const dismissBtn = blocker.querySelector("#dismiss");
        if (dismissBtn) {
            dismissBtn.addEventListener("click", () => {
                interval = setInterval(updateTimer, 1000);
                blocker.remove();
                startTime = Date.now();
                scrollCount = 0;
                mins = 0;
                secs = 0;
            });
        }
    }, 20000);
};


function updateTimer(){
    if (timer){
        const now = Date.now();
        const total = now - startTime;
        const totalSeconds = Math.floor(total / 1000);
        mins = String(Math.floor((totalSeconds % 3600) / 60)).padStart(2, "0");
        secs = String(totalSeconds % 60).padStart(2, "0");
        console.log(`${mins} and second ${secs} and scroll ${scrollCount}`)
        if(mins >= 1){ 
            console.log("Reset successful")
            startTime = Date.now()
            blocker();
        }
    }
}

window.addEventListener("scroll", () => {
    if (scrollTimeout) clearTimeout(scrollTimeout);
    // Wait for 300ms of no scroll to count 1 "gesture"
    scrollTimeout = setTimeout(() => {
        scrollCount++;
    }, 300);  

    if (scrollCount >= 30) {
        console.log(scrollCount)
        scrollCount = 0;
        mins = 0;
        secs = 0;
        blocker();
    }
});

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.action === "getScrollCount") {
        console.log("content sending data")
        sendResponse({ 
            mins,
            secs,
            scrollCount
        });
    }
    if (msg.action === "resetScroll") {
        console.log("content reset(get the message)")
        startTime = Date.now();
        scrollCount = 0;
        mins = 0;
        secs = 0;
    }   
});