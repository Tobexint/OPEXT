chrome.tabs.onCreated.addListener(function(tab) {
  console.log("New tab created: ", tab);
  // Logic to manage tabs
});

chrome.tabs.onRemoved.addListener(function(tabId, removeInfo) {
  console.log("Tab closed: ", tabId);
});

chrome.tabs.query({}, function(tabs) {
  console.log("All open tabs: ", tabs);
});

function getTabInfo() {
  return new Promise((resolve, reject) => {
    chrome.tabs.query({}, function(tabs) {
      const tabData = tabs.map(tab => ({
        id: tab.id,
        url: tab.url,
        title: tab.title,
        lastAccessed: tab.lastAccessed, // Assuming this is available
        memory_usage: Math.random() * 200 * 1024 * 1024  // Simulated memory usage
      }));
      resolve(tabData);
    });
  });
}

function sendTabsToFlask() {
  getTabInfo().then(tabs => {
    fetch('http://localhost:5000/process-tabs', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ tabs: tabs })
    })
    .then(response => response.json())
    .then(data => {
      console.log('Tab Suggestions:', data.suggestions);
      console.log('Tabs to close:', data.tabs_to_close); // Log the tabs to close

      // Get the list of tab IDs to close
      const tabsToClose = data.tabs_to_close;

      // Close inactive tabs
      if (tabsToClose && tabsToClose.length > 0) {
        tabsToClose.forEach(tabId => {
          chrome.tabs.remove(tabId, function() {
            console.log(`Tab with ID ${tabId} closed.`);
          });
        });
      }
    })
    .catch(error => console.error('Error:', error));
  });
}

// Trigger when user clicks on the extension
chrome.action.onClicked.addListener(() => {
  console.log("Extension icon clicked");
  sendTabsToFlask();
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "searchTabs") {
    console.log("Search button clicked");
    sendTabsToFlask();  // Call the function to send tab data to Flask
  }
});

