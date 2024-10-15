from flask import Flask, request, jsonify
from collections import defaultdict
from datetime import datetime, timedelta

app = Flask(__name__)

# Dictionary to store the last accessed time of each tab (simulate)
tab_access_times = {}
# Dictionary to track the access frequency of each tab
tab_access_frequency = defaultdict(int)


@app.route('/process-tabs', methods=['POST'])
def process_tabs():
    """
    API endpoint to process open tabs and return suggestions.
    The Chrome extension sends tab data (list of tabs) via a POST request.
    """
    tabs = request.json.get('tabs', [])
    print(f"Received {len(tabs)} tabs")
    
    now = datetime.now()
    inactive_threshold = timedelta(minutes=30)  # 30 minutes inactive
    high_memory_threshold = 100 * 1024 * 1024  # 100 MB threshold (simulated)

    suggestions = {
        "close_duplicates": [],
        "group_similar": [],
        "suspend_high_memory": [],
        "close_inactive": [],
        "prioritize_frequently_used": []
    }

    # Track for duplicates
    url_set = set()
    
    domain_groups = defaultdict(list)

    for tab in tabs:
        tab_id = tab['id']
        tab_url = tab['url']
        tab_title = tab['title']
        tab_memory_usage = tab.get('memory_usage', 0)  # Simulated memory usage
        
        # Simulate last accessed time tracking
        if tab_id not in tab_access_times:
            tab_access_times[tab_id] = now
        else:
            last_access_time = tab_access_times[tab_id]
            if now - last_access_time > inactive_threshold:
                suggestions['close_inactive'].append(tab_title)
        
        # Track how often the tab has been accessed
        tab_access_frequency[tab_id] += 1
        if tab_access_frequency[tab_id] > 5:
            suggestions['prioritize_frequently_used'].append(tab_title)

        # Group by domain
        domain = tab_url.split("/")[2]
        domain_groups[domain].append(tab)

        # Detect duplicates
        if tab_url in url_set:
            suggestions['close_duplicates'].append(tab_title)
        else:
            url_set.add(tab_url)
        
        # Detect high memory usage
        if tab_memory_usage > high_memory_threshold:
            suggestions['suspend_high_memory'].append(tab_title)

    # Group similar tabs
    for domain, group in domain_groups.items():
        if len(group) > 1:
            grouped_tabs = [tab['title'] for tab in group]
            suggestions['group_similar'].extend(grouped_tabs)

    return jsonify(suggestions)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
