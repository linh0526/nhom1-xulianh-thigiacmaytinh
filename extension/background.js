chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "analyzeFakeNews",
    title: "Analyze Fake News (Image + Text)",
    contexts: ["image"]
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "analyzeFakeNews") {
    // We have the image URL. Now we need the text. We will send a message to content script to get selected text.
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      files: ['content.js']
    }, () => {
      chrome.tabs.sendMessage(tab.id, { action: "getSelection" }, (response) => {
        const text = response ? response.text : "";
        const imageUrl = info.srcUrl;
        
        analyzeData(imageUrl, text);
      });
    });
  }
});

function analyzeData(imageUrl, text) {
  // Clear old state
  chrome.storage.local.set({ 
    isAnalyzing: true, 
    analysisResult: null, 
    analysisError: null 
  });
  
  // Open popup (Note: Chrome doesn't allow opening popup programmatically easily without user click, 
  // so the user will click it, but we store the state).
  
  fetch("http://localhost:8000/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      image_url: imageUrl,
      text: text || " "
    })
  })
  .then(res => {
    if (!res.ok) throw new Error("API Error");
    return res.json();
  })
  .then(data => {
    chrome.storage.local.set({ 
      isAnalyzing: false, 
      analysisResult: data 
    });
  })
  .catch(err => {
    chrome.storage.local.set({ 
      isAnalyzing: false, 
      analysisError: err.message 
    });
  });
}
