import pandas as pd

def load_data():
    df = pd.read_csv("data/epl_matches.csv")
    return df
