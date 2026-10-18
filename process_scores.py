import sys
import json
import urllib.request

urls = {
    "nfl": "https://espn.com",
    "nba": "https://espn.com",
    "mlb": "https://espn.com",
    "nhl": "https://espn.com",
    "ncaa": "https://espn.com"
}

for name, url in urls.items():
    print(f"Fetching {name} data...")
    try:
        # Fetch raw JSON directly from ESPN API
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
        out = []
        for e in data.get('events', []):
            comp = e['competitions'][0]
            home = next(c for c in comp['competitors'] if c['side'] == 'home')
            away = next(c for c in comp['competitors'] if c['side'] == 'away')
            
            out.append({
                'status': e['status']['type']['detail'],
                'isLive': e['status']['type']['state'] == 'in',
                'homeName': home['team']['displayName'],
                'homeLogo': home['team'].get('logo', 'https://espncdn.com'),
                'homeScore': home.get('score', '0'),
                'awayName': away['team']['displayName'],
                'awayLogo': away['team'].get('logo', 'https://espncdn.com'),
                'awayScore': away.get('score', '0')
            })
            
        # Write clean data payload safely to a local file
        with open(f"data-{name}.json", "w") as outfile:
            json.dump(out, outfile)
            
    except Exception as err:
        print(f"Error handling {name}: {err}")
        # Always output an empty list placeholder to avoid breaking the frontend carousel
        with open(f"data-{name}.json", "w") as outfile:
            json.dump([], outfile)
