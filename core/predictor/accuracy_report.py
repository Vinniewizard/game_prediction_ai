from predictor.models import PredictionAccuracy

def report_accuracy():
    records = PredictionAccuracy.objects.all()
    total = records.count()

    gg_correct = sum(1 for r in records if r.gg_predicted == r.gg_actual)
    over25_correct = sum(1 for r in records if r.over25_predicted == r.over25_actual)
    cs_correct = sum(1 for r in records if r.correct_score_predicted == r.correct_score_actual)

    return {
        "total_matches": total,
        "gg_accuracy": round(gg_correct / total * 100, 2) if total else 0,
        "over25_accuracy": round(over25_correct / total * 100, 2) if total else 0,
        "correct_score_accuracy": round(cs_correct / total * 100, 2) if total else 0
    }
