chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "getSelection") {
    let selection = window.getSelection().toString();
    sendResponse({ text: selection });
  }
  return true;
});
