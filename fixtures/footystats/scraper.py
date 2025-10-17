import pandas as pd
import soccerdata as sd
from datetime import date

LEAGUES = {
    "ENG-Premier-League": "ENG-Premier-League",
    "ESP-LaLiga"        : "ESP-LaLiga",
    "ITA-Serie-A"       : "ITA-Serie-A",
}

def pull_matches(league: str, season: str) -> pd.DataFrame:
    """Return tidy dataframe of fixtures & odds (no Selenium)."""
    espn = sd.ESPN(league=LEAGUES[league], season=season)
    df   = espn.read_schedule()
    # keep only columns we need
    cols = ["date", "home_team", "away_team", "home_score", "away_score"]
    return df[cols].rename(columns={
        "home_score": "goals_home",
        "away_score": "goals_away",
    })

if __name__ == "__main__":
    print(pull_matches("ENG-Premier-League", "2023-2024").head())
