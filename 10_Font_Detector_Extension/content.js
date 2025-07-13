// extension is running
console.log("Font Detector Extension is running");

// if popup send startlistening, start detect text selection
const mouseupHandler = function() {
    const selectedText = window.getSelection().toString();
    if (selectedText) {
        // Get font info directly in content script
        const selection = window.getSelection();
        if (selection.rangeCount > 0) {
            const range = selection.getRangeAt(0);
            const element = range.commonAncestorContainer.nodeType === Node.TEXT_NODE 
                ? range.commonAncestorContainer.parentElement 
                : range.commonAncestorContainer;
            
            const computedStyle = window.getComputedStyle(element);
            const fontInfo = {
                fontFamily: computedStyle.fontFamily,
                fontSize: computedStyle.fontSize,
                fontWeight: computedStyle.fontWeight,
                fontStyle: computedStyle.fontStyle
            };
            
            // Create mini popup window
            showFontPopup(fontInfo, selectedText);
        }
    }
};

// Function to create and show mini popup
function showFontPopup(fontInfo, selectedText) {
    // Remove existing popup if any
    const existingPopup = document.getElementById('font-detector-popup');
    if (existingPopup) {
        existingPopup.remove();
    }
    
    // Create popup element
    const popup = document.createElement('div');
    popup.id = 'font-detector-popup';
    popup.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        border: 2px solid #333;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 10000;
        font-family: Arial, sans-serif;
        font-size: 14px;
        max-width: 300px;
        color: black;
    `;
    
    popup.innerHTML = `
        <div style="font-weight: bold; margin-bottom: 10px; color: #333;">Font Detector</div>
        <div><strong>Text:</strong> "${selectedText.substring(0, 30)}${selectedText.length > 30 ? '...' : ''}"</div>
        <div><strong>Font:</strong> ${fontInfo.fontFamily.split(',')[0].replace(/"/g, '')}</div>
        <div><strong>Size:</strong> ${fontInfo.fontSize}</div>
        <div><strong>Weight:</strong> ${fontInfo.fontWeight}</div>
        <div><strong>Style:</strong> ${fontInfo.fontStyle}</div>
        <button onclick="this.parentElement.remove()" style="
            position: absolute;
            top: 5px;
            right: 8px;
            background: none;
            border: none;
            font-size: 16px;
            cursor: pointer;
            color: #666;
        ">×</button>
    `;
    
    document.body.appendChild(popup);
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        if (popup.parentElement) {
            popup.remove();
        }
    }, 5000);
}

chrome.runtime.onMessage.addListener(function(request, _, sendResponse) {
    if (request.action === "startListening") {
        console.log("Starting to listen for text selection");
        document.addEventListener("mouseup", mouseupHandler);
    }
    else if (request.action === "stopListening") {
        console.log("Stopping listening for text selection");
        document.removeEventListener("mouseup", mouseupHandler);
    }
    sendResponse({ status: "Listening state updated" });
});

