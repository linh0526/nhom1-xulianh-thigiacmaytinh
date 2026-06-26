chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "analyzeFakeNews",
    title: "Analyze Fake News (Image + Text)",
    contexts: ["image"]
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "analyzeFakeNews") {
    const imageUrl = info.srcUrl;
    
    // Attempt to get text, but if it fails, just send the image
    try {
      chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: () => window.getSelection().toString()
      }, (injectionResults) => {
        let text = "";
        if (injectionResults && injectionResults[0] && injectionResults[0].result) {
          text = injectionResults[0].result;
        }
        analyzeData(imageUrl, text);
      });
    } catch (e) {
      console.error("Script injection failed", e);
      analyzeData(imageUrl, "");
    }
  }
});

function analyzeData(imageUrl, text) {
  // Clear old state
  chrome.storage.local.set({ 
    isAnalyzing: true, 
    analysisResult: null, 
    analysisError: null,
    analysisRequestData: { image_url: imageUrl, text: text || " " }
  });
  
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
  .then(async res => {
    if (!res.ok) {
      const text = await res.text();
      throw new Error("API Error: " + text);
    }
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
