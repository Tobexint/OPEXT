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
    inactive_threshold = timedelta(minutes=30)  # Tabs inactive for 30+ minutes
    high_memory_threshold = 100 * 1024 * 1024  # 100 MB threshold (simulated)

    suggestions = {
        "close_duplicates": [],
        "group_similar": [],
        "suspend_high_memory": [],
        "close_inactive": [],
        "prioritize_frequently_used": []
    }

    tabs_to_close = []  # List of tab IDs to close

    # Track for duplicates
    url_set = set()
    domain_groups = defaultdict(list)

    for tab in tabs:
        tab_id = tab['id']
        tab_url = tab['url']
        tab_title = tab['title']
        tab_memory_usage = tab.get('memory_usage', 0)  # Simulated memory usage

        # Simulate closing inactive tabs in Flask
        suggestions['tabs_to_close'] = [tab['id'] for tab in tabs[:2]]  # Close the first two tabs for testing

        return jsonify(suggestions)


        # Simulate last accessed time tracking
        if tab_id not in tab_access_times:
            tab_access_times[tab_id] = now
        else:
            last_access_time = tab_access_times[tab_id]
            if now - last_access_time > inactive_threshold:
                suggestions['close_inactive'].append(tab_title)
                tabs_to_close.append(tab_id)  # Add tab ID to the list

        # Detect duplicate URLs
        if tab_url in url_set:
            suggestions['close_duplicates'].append(tab_title)
        else:
            url_set.add(tab_url)

        # Group by domain
        domain = tab_url.split('/')[2] if '//' in tab_url else tab_url
        domain_groups[domain].append(tab_title)

        # Check for high memory usage
        if tab_memory_usage > high_memory_threshold:
            suggestions['suspend_high_memory'].append(tab_title)

    # Group similar tabs
    for domain, grouped_tabs in domain_groups.items():
        if len(grouped_tabs) > 1:
            suggestions['group_similar'].append({
                "domain": domain,
                "tabs": grouped_tabs
            })

    # Simulate frequently used tabs prioritization
    frequently_used_tabs = sorted(tabs, key=lambda t: tab_access_times.get(t['id'], now), reverse=True)
    for tab in frequently_used_tabs[:5]:  # Example: prioritize the top 5
        suggestions['prioritize_frequently_used'].append(tab['title'])

    print("Suggestions generated: ", suggestions)

    # Return the suggestions and the tab IDs to close
    return jsonify(suggestions=suggestions, tabs_to_close=tabs_to_close)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
