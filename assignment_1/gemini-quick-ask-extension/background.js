const GEMINI_BASE_URL = "https://gemini.google.com/app";

// Create the context menu item when the extension is installed.
chrome.runtime.onInstalled.addListener(() => {
    chrome.contextMenus.create({
        id: "askGemini",
        title: 'Ask Gemini: "%s"', // %s is a placeholder for the selected text
        contexts: ["selection"],
    });
});

// Add a listener for when the user clicks on the context menu item.
chrome.contextMenus.onClicked.addListener(async (info, tab) => {
    // Ensure the click was on our menu item and there's text selected.
    if (info.menuItemId === "askGemini" && info.selectionText) {
        // A service worker can't directly access the clipboard.
        // We must execute a script in the context of the active tab to do it.
        await chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: (textToCopy) => {
                navigator.clipboard.writeText(textToCopy);
            },
            args: [info.selectionText],
        });

        // Create a new tab with the base Gemini URL.
        chrome.tabs.create({ url: GEMINI_BASE_URL });
    }
});
