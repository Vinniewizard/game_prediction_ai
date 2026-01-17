import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from predictor.engine import save_prediction
from predictor.best_pick import calculate_ev

# Example matches to predict
matches = [
    ("Arsenal", "Chelsea"),
    ("Man City", "Liverpool"),
    ("Tottenham", "Arsenal")
]

for home, away in matches:
    # Save prediction in database
    pred = save_prediction(home, away)
    print(f"Saved prediction for {home} vs {away}")

    # Calculate best pick
    best_picks = calculate_ev(home, away)
    print(f"Best picks for {home} vs {away}:")
    for pick in best_picks:
        print(f" - {pick['market']} | Odds: {pick['odds']} | EV: {pick['expected_value']} | Source: {pick['source']}")
    print("\n" + "="*50 + "\n")
