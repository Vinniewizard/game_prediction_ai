from predictor.models import MatchOdds
from predictor.models import Prediction

def calculate_ev(home_team, away_team):
    pred = Prediction.objects.get(home_team=home_team, away_team=away_team)
    
    best_picks = []

    # GG market
    gg_odds_list = MatchOdds.objects.filter(
        home_team=home_team, away_team=away_team, market='GG'
    )
    for odd in gg_odds_list:
        probability = pred.gg_probability / 100
        ev = (probability * odd.odds) - (1 - probability)
        best_picks.append({
            'market': 'GG',
            'odds': odd.odds,
            'source': odd.source,
            'expected_value': round(ev, 2)
        })
    
    # Over 2.5 market
    over_odds_list = MatchOdds.objects.filter(
        home_team=home_team, away_team=away_team, market='Over 2.5'
    )
    for odd in over_odds_list:
        probability = pred.over25_probability / 100
        ev = (probability * odd.odds) - (1 - probability)
        best_picks.append({
            'market': 'Over 2.5',
            'odds': odd.odds,
            'source': odd.source,
            'expected_value': round(ev, 2)
        })
    
    # Sort by EV descending
    best_picks = sorted(best_picks, key=lambda x: x['expected_value'], reverse=True)
    
    return best_picks
