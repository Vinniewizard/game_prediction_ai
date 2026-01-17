from django.urls import path
from . import views

urlpatterns = [
    path('predict/<str:home_team>/<str:away_team>/', views.get_prediction),
    path('api/today-predictions/', views.today_predictions, name='today_predictions'),
    path('api/best-picks/', views.best_picks, name='best_picks'),
    path('api/accuracy/', views.accuracy_report_api, name='accuracy_report'),
    path('dashboard/', views.dashboard, name='dashboard'), 
]
