document.getElementById('search-tabs').addEventListener('input', function() {
  const searchQuery = this.value;
  chrome.tabs.query({}, function(tabs) {
    const filteredTabs = tabs.filter(tab => tab.title.includes(searchQuery));
    const tabList = document.getElementById('tab-list');
    tabList.innerHTML = '';
    filteredTabs.forEach(tab => {
      const li = document.createElement('li');
      li.textContent = tab.title;
      tabList.appendChild(li);
    });
  });
});

document.getElementById('searchBtn').addEventListener('click', function() {
    chrome.runtime.sendMessage({ action: "searchTabs" });
});
