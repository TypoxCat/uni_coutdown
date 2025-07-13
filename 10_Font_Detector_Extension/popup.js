// if start button is clicked, if user selects text, display font information
const btn = document.getElementById("start");
let running = false;

// Load running state from localStorage to save on off state
if (localStorage.getItem("fontDetectorRunning") === "true") {
    running = true;
    btn.textContent = "ON";
    btn.style.backgroundColor = "lightgreen";
} else {
    running = false;
    btn.textContent = "OFF";
    btn.style.backgroundColor = "";
}

btn.addEventListener("click", function() {
    if (!running){
        btn.textContent = "ON";
        running = true;
        btn.style.backgroundColor = "lightgreen";
        localStorage.setItem("fontDetectorRunning", "true")
        // Send message to content script to start listening for text selection
        chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, { action: "startListening" }).catch(() => {
                console.log("Content script not ready yet");
            });
        });
        console.log("Font Detector Extension is running and listening for text selection.");
    }
    else {
        btn.textContent = "OFF";
        running = false;
        btn.style.backgroundColor = "";
        localStorage.setItem("fontDetectorRunning", "false");
        // Send message to content script to stop listening for text selection
        chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, { action: "stopListening" }).catch(() => {
                console.log("Content script not ready yet");
            });
        });
        console.log("Font Detector Extension has stopped listening for text selection.");
    }
});

// Listen for messages from content script
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === "textSelected") {
        console.log("Selected text:", request.text);
    }
});