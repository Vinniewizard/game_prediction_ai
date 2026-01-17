from django.core.management.base import BaseCommand
from predictor.engine import save_prediction
from predictor.best_pick import calculate_ev

class Command(BaseCommand):
    help = "Run daily predictions and best picks"

    def handle(self, *args, **kwargs):
        matches = [
            ("Arsenal", "Chelsea"),
            ("Man City", "Liverpool"),
            ("Tottenham", "Arsenal")
        ]
        for home, away in matches:
            pred = save_prediction(home, away)
            best_picks = calculate_ev(home, away)
            self.stdout.write(f"Predictions saved for {home} vs {away}")
            self.stdout.write(str(best_picks))

