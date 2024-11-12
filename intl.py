import os
from pathlib import Path

import pandas as pd

directory = "data"

def main():
    df = pd.read_csv("results-int.csv")
    df["neutral"] = df["neutral"].apply(lambda x: True if x == "TRUE" else False)
    df["tournament_year"] = df["date"].apply(lambda x: x[:4])
    df["tournament_name"] = df["tournament"]
    df["stage"] = None
    df["knockout"] = False
    tournaments = list(df["tournament"].unique())
    for tour in tournaments:
        tour_slug = tour.lower().replace(" ", "-")
        # Path(f"data/international/{tour_slug}").mkdir(parents=True, exist_ok=True)
        filtered = df[df["tournament"] == tour]
        filtered = filtered[["date","home_team","home_score","away_score","away_team","neutral","knockout","stage","tournament_name","tournament_year"]]
        filtered.to_csv(f"data/international/{tour_slug}.csv", index=False)



if __name__ == "__main__":
    main()
