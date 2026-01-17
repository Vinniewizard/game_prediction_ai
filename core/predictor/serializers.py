from rest_framework import serializers
from .models import Prediction
from rest_framework import serializers
from .models import Prediction, PredictionAccuracy, MatchOdds

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = '__all__'

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = '__all__'

class AccuracySerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictionAccuracy
        fields = '__all__'

class MatchOddsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchOdds
        fields = '__all__'
