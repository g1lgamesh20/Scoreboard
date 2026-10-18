import sys
import json
import urllib.request
from datetime import datetime

# Using the free, unblocked public API key '2' from TheSportsDB
LEAGUES_MAP = {
    "nfl": "4391",
    "nba": "4387",
    "mlb": "4424",
    "nhl": "4380"
}

today_str = datetime.today().strftime('%Y-%m-%d')

for name, league_id in LEAGUES_MAP.items():
    print(f"Fetching {name.upper()} data from TheSportsDB...")
    # Pulls scheduled, live, and final matches for the current day
    url = f"https://thesportsdb.com{today_str}&l={league_id}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
        out = []
        events = data.get('events', []) or []
        print(f"Found {len(events)} matches for {name.upper()}")
        
        for e in events:
            # Safely structure placeholder elements
            status = e.get('strStatus', 'Scheduled')
            is_live = status.lower() in ['live', 'in progress', '1h', '2h', 'q1', 'q2', 'q3', 'q4']
            
            # TheSportsDB bundles high-res team badge URLs natively
            out.append({
                'status': f"{status} - {e.get('strProgress', '')}".strip(" - "),
                'isLive': is_live,
                'homeName': e.get('strHomeTeam', 'Home'),
                'homeLogo': e.get('strHomeBadge', 'https://thesportsdb.com'),
                'homeScore': e.get('intHomeScore', '0') or '0',
                'awayName': e.get('strAwayTeam', 'Away'),
                'awayLogo': e.get('strAwayBadge', 'https://thesportsdb.com'),
                'awayScore': e.get('intAwayScore', '0') or '0'
            })
            
        with open(f"data-{name}.json", "w") as outfile:
            json.dump(out, outfile)
            
    except Exception as err:
        print(f"Error handling {name.upper()}: {err}")
        with open(f"data-{name}.json", "w") as outfile:
            json.dump([], outfile)
