from pathlib import Path

import os
import pandas as pd

from parsers import *

tournament = "international/clubs/fifa-intercontinental-cup"
tournament_name = "FIFA Intercontinental Cup"

parsers = [parse for name, parse in globals().items() if name.endswith("_parser")]


def main():
    files = [f for f in os.listdir(os.path.join("data", tournament)) if os.path.isfile(os.path.join("data", tournament, f)) and f.endswith(".txt")]
    for file in files:
        year = file.split("/")[-1].split(".")[0]
        with open(Path(f"data/{tournament}/{year}.txt"), "r") as file:
            text = file.read()
        print(f"Parsing {year} for {tournament}")
        results = []
        for parse in parsers:
            print(f"Parsing with {parse.__name__}")
            # try:
            results = parse(text, tournament_name, year)
            # except Exception as err:
            #     print(f"Error {str(err)}")
            #     continue

        if results:
            path = Path(f"data/{tournament}/{year}.csv")
            print(f"Saving to {path}")

            dataframe = pd.DataFrame(
                results,
                columns=[
                    "date",
                    "home_team",
                    "home_score",
                    "away_score",
                    "away_team",
                    "neutral",
                    "stage",
                    "tournament_name",
                    "tournament_year",
                ],
            )
            dataframe.to_csv(path, index=False)

if __name__ == "__main__":
    main()
