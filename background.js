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
        // You can add memory usage simulation here or in Flask.
        memory_usage: Math.random() * 200 * 1024 * 1024  // Simulated memory usage
      }));
      resolve(tabData);
    });
  });
}

function sendTabsToFlask() {
  getTabInfo().then(tabs => {
    console.log("Sending tabs to Flask:", tabs);  // Log the tabs you're sending
    fetch('http://localhost:5000/process-tabs', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ tabs: tabs })
    })
    .then(response => response.json())
    .then(data => {
      console.log('Tab Suggestions from Flask:', data);  // Log the Flask response
    })
    .catch(error => console.error('Error:', error));  // Log any error
  });
}


// Trigger when user clicks on the extension
chrome.action.onClicked.addListener(() => {
  sendTabsToFlask();
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "searchTabs") {
    console.log("Search button clicked");
    sendTabsToFlask();  // Call the function to send tab data to Flask
  }
});

const MAX_TABS = 10;  // Set your maximum allowed open tabs

function manageTabs() {
    chrome.tabs.query({}, function(tabs) {
        console.log(`Currently open tabs: ${tabs.length}`);

        if (tabs.length > MAX_TABS) {
            // Sort tabs by lastAccessed to close the least recently used ones
            tabs.sort((a, b) => a.lastAccessed - b.lastAccessed);

            // Calculate how many tabs to close
            const tabsToClose = tabs.length - MAX_TABS;

            console.log(`Closing ${tabsToClose} excess tabs...`);
            for (let i = 0; i < tabsToClose; i++) {
                const tabToClose = tabs[i];
                chrome.tabs.remove(tabToClose.id, () => {
                    console.log(`Closed tab: ${tabToClose.title}`);
                });
            }
        }
    });
}

// Trigger when user clicks on the extension
chrome.action.onClicked.addListener(() => {
    manageTabs();  // Check and manage tabs when the extension is clicked
});
