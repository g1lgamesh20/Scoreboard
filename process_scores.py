import sys
import json
import urllib.request

urls = {
    "nfl": "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard",
    "nba": "https://espn.com",
    "mlb": "https://espn.com",
    "nhl": "https://espn.com",
    "ncaa": "https://espn.com"
}

for name, url in urls.items():
    print(f"Starting connection to ESPN for: {name.upper()}")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
        out = []
        events = data.get('events', [])
        print(f"Found {len(events)} total events in raw feed for {name.upper()}")
        
        for e in events:
            competitions = e.get('competitions', [])
            if not competitions:
                continue
                
            # FIXED: explicitly grabbing item 0 from the array layout block
            comp = competitions[0]
            competitors = comp.get('competitors', [])
            if len(competitors) < 2:
                continue
                
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
        print(f"--- SUCCESS: Wrote data-{name}.json with {len(out)} live/placeholder cards ---")
            
    except Exception as err:
        print(f"!!! Error processing data structure for {name.upper()}: {err} !!!")
        with open(f"data-{name}.json", "w") as outfile:
            json.dump([], outfile)
