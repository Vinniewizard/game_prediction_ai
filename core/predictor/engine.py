from predictor.models import Prediction
import numpy as np
from scipy.stats import poisson
from predictor.team_strength import calculate_team_strengths
from predictor.stats import calculate_stats
from predictor.data_loader import load_data
from predictor.models import Prediction, PredictionAccuracy

df = load_data()
AVG_HOME_GOALS, AVG_AWAY_GOALS = calculate_stats(df)
TEAM_STRENGTH = calculate_team_strengths()


def predict_correct_score():
    max_goals = 5
    results = {}

    for home_goals in range(max_goals):
        for away_goals in range(max_goals):
            prob = poisson.pmf(home_goals, AVG_HOME_GOALS) * \
                   poisson.pmf(away_goals, AVG_AWAY_GOALS)
            results[f"{home_goals}-{away_goals}"] = prob

    top_scores = sorted(results.items(), key=lambda x: x[1], reverse=True)[:3]
    return [(score, round(prob * 100, 2)) for score, prob in top_scores]

def predict_gg_over25():
    gg = 0
    over25 = 0

    for i in range(6):
        for j in range(6):
            p = poisson.pmf(i, AVG_HOME_GOALS) * poisson.pmf(j, AVG_AWAY_GOALS)
            if i > 0 and j > 0:
                gg += p
            if i + j > 2:
                over25 += p

    return {
        "GG (%)": round(gg * 100, 2),
        "Over 2.5 (%)": round(over25 * 100, 2)
    }

def confidence_level(value):
    if value >= 75:
        return "VERY STRONG"
    elif value >= 65:
        return "STRONG"
    elif value >= 55:
        return "MEDIUM"
    else:
        return "RISKY"
def predict_match(home_team, away_team):
    hs = TEAM_STRENGTH[home_team]
    as_ = TEAM_STRENGTH[away_team]

    home_lambda = AVG_HOME_GOALS * hs['home_attack'] * as_['away_defense']
    away_lambda = AVG_AWAY_GOALS * as_['away_attack'] * hs['home_defense']

    max_goals = 5
    scores = {}

    for i in range(max_goals):
        for j in range(max_goals):
            prob = poisson.pmf(i, home_lambda) * poisson.pmf(j, away_lambda)
            scores[f"{i}-{j}"] = prob

    top_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]

    gg = sum(prob for score, prob in scores.items()
             if int(score[0]) > 0 and int(score[2]) > 0)

    over25 = sum(prob for score, prob in scores.items()
                 if int(score[0]) + int(score[2]) > 2)

    first_home, first_away = predict_first_goal(home_team, away_team)
    yellow_cards = predict_yellow_cards(home_team, away_team)

    return {
        "match": f"{home_team} vs {away_team}",
        "GG (%)": round(gg * 100, 2),
        "Over 2.5 (%)": round(over25 * 100, 2),
        "Correct Scores": [(s, round(p * 100, 2)) for s, p in top_scores],
        "First Goal Home (%)": first_home,
        "First Goal Away (%)": first_away,
        "Expected Yellow Cards": yellow_cards
    }

def save_prediction(home_team, away_team):
    pred = predict_match(home_team, away_team)
    
    obj, created = Prediction.objects.update_or_create(
        home_team=home_team,
        away_team=away_team,
        defaults={
            'gg_probability': pred['GG (%)'],
            'over25_probability': pred['Over 2.5 (%)'],
            'top_correct_scores': pred['Correct Scores'],
            'first_goal_home_probability': pred['First Goal Home (%)'],
            'yellow_cards_expected': pred['Expected Yellow Cards']
        }
    )
    
    return obj

def predict_first_goal(home_team, away_team):
    # Count number of matches home team scored first
    df_home = df[df['home_team'] == home_team]
    df_away = df[df['away_team'] == away_team]

    home_first_goals = 0
    away_first_goals = 0
    total_matches = len(df_home) + len(df_away)

    for _, row in df_home.iterrows():
        if row['home_goals'] > 0:
            home_first_goals += 1
    for _, row in df_away.iterrows():
        if row['away_goals'] > 0:
            away_first_goals += 1

    if total_matches == 0:
        return 50, 50  # default 50/50
    home_prob = round((home_first_goals / total_matches) * 100, 2)
    away_prob = round((away_first_goals / total_matches) * 100, 2)
    return home_prob, away_prob
def predict_yellow_cards(home_team, away_team):
    # Assume average 3–5 yellow cards per match
    avg_yc = df['home_goals'].mean() + df['away_goals'].mean()  # proxy for match intensity
    expected_yc = round(avg_yc * 1.2, 2)  # add scaling factor
    return expected_yc

def update_accuracy(home_team, away_team, home_goals, away_goals):
    try:
        pred = Prediction.objects.get(home_team=home_team, away_team=away_team)
    except Prediction.DoesNotExist:
        return "Prediction not found"

    # Calculate actual outcomes
    gg_actual = home_goals > 0 and away_goals > 0
    over25_actual = (home_goals + away_goals) > 2
    correct_score_actual = f"{home_goals}-{away_goals}"

    # GG prediction (assume >50% = True)
    gg_predicted = pred.gg_probability > 50
    over25_predicted = pred.over25_probability > 50
    correct_score_predicted = pred.top_correct_scores[0][0]  # top predicted score

    # Save accuracy
    accuracy = PredictionAccuracy.objects.create(
        home_team=home_team,
        away_team=away_team,
        gg_predicted=gg_predicted,
        gg_actual=gg_actual,
        over25_predicted=over25_predicted,
        over25_actual=over25_actual,
        correct_score_predicted=correct_score_predicted,
        correct_score_actual=correct_score_actual
    )

    return accuracy
