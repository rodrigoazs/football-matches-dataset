from pathlib import Path

import pandas as pd

from parsers import *

FOLDER = "data/country/bra/brasileirao-serie-a/"

# from, to, number of matches
generate_matches = {
    "international/clubs/copa-libertadores-de-america": [
        (2009, 2009, 134),
        (2010, 2014, 138),
        (2015, 2015, 137),
        (2016, 2016, 138),
        (2017, 2018, 156),
        (2019, 2022, 155),
    ]
}

tournament_name = "Copa Libertadores de América"

parsers = [parse for name, parse in globals().items() if name.endswith("_parser")]


def main():
    for tournament, schemas in generate_matches.items():
        for schema in schemas:
            from_year, to_year, assert_matches = schema
            for year in range(from_year, to_year + 1):
                with open(Path(f"data/{tournament}/{year}.txt"), "r") as file:
                    text = file.read()
                print(f"Parsing {year} for {tournament}")
                for parse in parsers:
                    print(f"Parsing with {parse.__name__}")
                    try:
                        results = parse(text, tournament_name, year)
                        print("Matches extracted:", len(results))
                        print("Matches expected:", assert_matches)
                        if len(results) == assert_matches:
                            break
                    except Exception as err:
                        print(f"Error {str(err)}")
                        continue

                assert len(results) == assert_matches

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
                        "knockout",
                        "stage",
                        "tournament_name",
                        "tournament_year",
                    ],
                )
                dataframe.to_csv(path, index=False)


if __name__ == "__main__":
    main()
