let timer = true;
let startTime = Date.now();
let mins;
let secs;
// one second interval
interval = setInterval(updateTimer, 1000);

let scrollCount = 0;
let scrollTimeout;
console.log("✅ Anti-Doomscroll content script is running!");

function blocker(){
    const blocker = document.createElement("div");
    blocker.style.position = "fixed";
    blocker.style.top = "0";
    blocker.style.left = "0";
    blocker.style.width = "100%";
    blocker.style.height = "100%";
    blocker.style.backgroundColor = "rgba(0, 0, 0, 0.8)";
    blocker.style.color = "#fff";
    blocker.style.zIndex = "9999";
    blocker.style.display = "flex";
    blocker.style.flexDirection = "column";
    blocker.style.justifyContent = "center";
    blocker.style.alignItems = "center";
    blocker.style.fontSize = "24px";
    blocker.innerHTML = `
    <p>🚨</p>
    <p>Take a break. Breathe. Touch some grass 🌱</p>
    `;
    document.body.appendChild(blocker);

    setTimeout(() => {
        document.body.removeChild(blocker);
        blocker.innerHTML = `
        <p>🚨 You've been scrolling for too long</p>
        <p>Take a break. Breathe. Touch some grass 🌱</p>
        <button id="dismiss">I'm good now</button>
        `;
        document.body.appendChild(blocker);
        const dismissBtn = blocker.querySelector("#dismiss");
        if (dismissBtn) {
            dismissBtn.addEventListener("click", () => {
                blocker.remove();
                startTime = Date.now();
                scrollCount = 0;
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
        
        if(mins >= 20){ 
            console.log("Reset successful")
            blocker();
            mins = 0;
            secs = 0;
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
        blocker();
    }
});

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.action === "getScrollCount") {
        sendResponse({ scrollCount,
            mins,
            secs
         });
    }
    if (msg.action === "resetScroll") {
        console.log("Reset successful")
        startTime = Date.now();
        scrollCount = 0;
        mins = 0;
        secs = 0;
    }   
});