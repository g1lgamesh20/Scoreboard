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
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
        out = []
        for e in data.get('events', []):
            # FIXED: ESPN packages competitions as a list, so we grab the first element [0]
            competitions = e.get('competitions', [])
            if not competitions:
                continue
                
            comp = competitions[0]
            competitors = comp.get('competitors', [])
            if len(competitors) < 2:
                continue
                
            home = next((c for c in competitors if c.side == 'home'), competitors[0])
            away = next((c for c in competitors if c.side == 'away'), competitors[1])
            
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
            
        with open(f"data-{name}.json", "w") as outfile:
            json.dump(out, outfile)
        print(f"Successfully wrote data-{name}.json with {len(out)} games.")
            
    except Exception as err:
        print(f"Error handling {name}: {err}")
        with open(f"data-{name}.json", "w") as outfile:
            json.dump([], outfile)
