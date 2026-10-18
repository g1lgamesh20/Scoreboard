import sys
import json
import urllib.request

urls = {
    "nfl": "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard",
    "nba": "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard",
    "mlb": "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard",
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
            competitions = e.get('competitions', [])
            if not competitions:
                continue
                
            # Safely grab the first competition configuration object
            comp = competitions[0]
            competitors = comp.get('competitors', [])
            if len(competitors) < 2:
                continue
                
            # FIXED: Changed from .side to ['side'] so python processes the dictionary keys cleanly
            home = next((c for c in competitors if c['side'] == 'home'), competitors[0])
            away = next((c for c in competitors if c['side'] == 'away'), competitors[1])
            
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
        print(f"Successfully wrote data-{name}.json with {len(out)} matches.")
            
    except Exception as err:
        print(f"Critical error mapping {name}: {err}")
        with open(f"data-{name}.json", "w") as outfile:
            json.dump([], outfile)
