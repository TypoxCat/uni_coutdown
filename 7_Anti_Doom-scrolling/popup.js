let startTime;
let timerInterval;

document.addEventListener("DOMContentLoaded", () => {
  const count = document.getElementById("scroll-count")
  const timer = document.getElementById("timer")
  // const time = document.getElementById("active-time")
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const tabId = tabs[0].id;

    // send message to content script
    chrome.tabs.sendMessage(tabId, { action: "getScrollCount" }, (response) => {
      console.log(`✅ Received from content: ${response.scrollCount}`);
      count.textContent = `Scroll: ${response.scrollCount}`;
      timer.textContent = `${response.mins}:${response.secs}`
    });
  });
});

document.getElementById("reset").addEventListener("click", () => {
  if (timerInterval) {
    clearInterval(timerInterval);
    elapsed += Date.now() - startTime;
    timerInterval = null;
  }
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    chrome.scripting.executeScript({
      target: { tabId: tabs[0].id },
      func: () => {
        scrollCount = 0;
        alert("Scroll count reset!");
      },
    });
  });
});