from django.db import models

class Prediction(models.Model):
    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)
    
    gg_probability = models.FloatField()
    over25_probability = models.FloatField()
   
    top_correct_scores = models.JSONField()  # Stores top 3 scores with probability
    first_goal_home_probability = models.FloatField(null=True, blank=True)
    yellow_cards_expected = models.FloatField(null=True, blank=True)


    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"
class MatchOdds(models.Model):
    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)
    
    market = models.CharField(max_length=50)  # e.g., 'GG', 'Over 2.5', 'Correct Score'
    odds = models.FloatField()
    source = models.CharField(max_length=100)  # website name
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.home_team} vs {self.away_team} - {self.market}"

class PredictionAccuracy(models.Model):
    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    
    gg_predicted = models.BooleanField()
    gg_actual = models.BooleanField()
    
    over25_predicted = models.BooleanField()
    over25_actual = models.BooleanField()
    
    correct_score_predicted = models.CharField(max_length=5)  # e.g., '2-1'
    correct_score_actual = models.CharField(max_length=5)
    
    def __str__(self):
        return f"{self.home_team} vs {self.away_team} | {self.date}"
