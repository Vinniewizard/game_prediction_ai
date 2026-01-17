def calculate_stats(df):
    avg_home_goals = df['home_goals'].mean()
    avg_away_goals = df['away_goals'].mean()
    return avg_home_goals, avg_away_goals
