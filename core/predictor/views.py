from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Prediction
from .serializers import PredictionSerializer
from .engine import save_prediction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Prediction, PredictionAccuracy, MatchOdds
from .serializers import PredictionSerializer, AccuracySerializer, MatchOddsSerializer
from .best_pick import calculate_ev
from .accuracy_report import report_accuracy
from django.shortcuts import render

def dashboard(request):
    return render(request, 'dashboard.html')

@api_view(['GET'])
def get_prediction(request, home_team, away_team):
    # Generate & save prediction
    prediction = save_prediction(home_team, away_team)
    
    serializer = PredictionSerializer(prediction)
    return Response(serializer.data)

@api_view(['GET'])
def today_predictions(request):
    predictions = Prediction.objects.all()
    serializer = PredictionSerializer(predictions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def best_picks(request):
    matches = Prediction.objects.all()
    all_picks = {}
    for match in matches:
        all_picks[f"{match.home_team} vs {match.away_team}"] = calculate_ev(match.home_team, match.away_team)
    return Response(all_picks)

@api_view(['GET'])
def accuracy_report_api(request):
    return Response(report_accuracy())
