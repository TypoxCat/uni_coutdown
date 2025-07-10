const count = document.getElementById("scroll-count");
const timess = document.getElementById("timer");

// every time i open the popup
document.addEventListener("DOMContentLoaded", () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        const tabId = tabs[0].id;

        // send message to content script
        chrome.tabs.sendMessage(tabId, { action: "getScrollCount" }, (response) => {
            console.log(`✅ Received from content`);
            count.textContent = `Scroll: ${response.scrollCount}`;
            timess.textContent = `${response.mins}:${response.secs}`
        });
    });
});

document.getElementById("reset").addEventListener("click", () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        const tabId = tabs[0].id;
        // Tell content script to reset the timer and scroll count
        chrome.tabs.sendMessage(tabId, { action: "resetScroll" }, () => {
            alert("Scroll count and timer reset!");

            // Refresh values in popup
            chrome.tabs.sendMessage(tabId, { action: "getScrollCount" }, (response) => {
                count.textContent = `Scroll: ${response.scrollCount}`;
                timess.textContent = `${response.mins}:${response.secs}`;
            });
        });
    });
});