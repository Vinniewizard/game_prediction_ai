import pandas as pd
from predictor.data_loader import load_data

df = load_data()

def calculate_team_strengths():
    teams = pd.concat([df['home_team'], df['away_team']]).unique()

    team_stats = {}

    league_avg_home = df['home_goals'].mean()
    league_avg_away = df['away_goals'].mean()

    for team in teams:
        home_matches = df[df['home_team'] == team]
        away_matches = df[df['away_team'] == team]

        home_attack = home_matches['home_goals'].mean() if len(home_matches) else league_avg_home
        home_defense = home_matches['away_goals'].mean() if len(home_matches) else league_avg_away

        away_attack = away_matches['away_goals'].mean() if len(away_matches) else league_avg_away
        away_defense = away_matches['home_goals'].mean() if len(away_matches) else league_avg_home

        team_stats[team] = {
            "home_attack": home_attack / league_avg_home,
            "home_defense": home_defense / league_avg_away,
            "away_attack": away_attack / league_avg_away,
            "away_defense": away_defense / league_avg_home,
        }

    return team_stats
