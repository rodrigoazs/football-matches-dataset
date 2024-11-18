from pathlib import Path

import pandas as pd

from parsers import *

FOLDER = "data/country/bra/brasileirao-serie-a/"

# from, to, number of matches
generate_matches = {
    "international/clubs/copa-libertadores-de-america": [
        (1960, 1960, 13),
        (1961, 1961, 16),
        (1962, 1962, 26),
        (1963, 1963, 19),
        (1964, 1964, 25),
        (1965, 1965, 25),
        (1966, 1966, 95),
        (1967, 1967, 114),
        (1968, 1968, 93),
        (1969, 1969, 74),
        (1970, 1970, 88),
        (1971, 1971, 74),
        (1972, 1972, 68),
        (1973, 1973, 66),
        (1974, 1975, 76),
        (1976, 1976, 77),
        (1977, 1980, 75),
        (1981, 1981, 77),
        (1982, 1983, 74),
        (1984, 1984, 75),
        (1985, 1985, 74),
        (1986, 1986, 65),
        (1987, 1987, 76),
        (1988, 1988, 83),
        (1989, 1989, 91),
        (1990, 1990, 81),
        (1991, 1991, 91),
        (1992, 1992, 99),
        (1993, 1993, 92),
        (1994, 1994, 90),
        (1995, 1995, 91),
        (1996, 1997, 90),
        (1998, 1998, 99),
        (1999, 1999, 102),
        (2000, 2003, 138),
        (2004, 2004, 141),
        (2005, 2008, 138),
        (2009, 2009, 134),
        (2010, 2014, 138),
        (2015, 2015, 137),
        (2016, 2016, 138),
        (2017, 2017, 156),
        (2018, 2018, 156),
        (2019, 2021, 155),
        (2022, 2022, 155),
    ]
}

tournament_name = "Copa Libertadores de América"

parsers = [parse for name, parse in globals().items() if name.endswith("_parser")]


def main():
    teams = set()
    for tournament, schemas in generate_matches.items():
        for schema in schemas:
            from_year, to_year, assert_matches = schema
            for year in range(from_year, to_year + 1):
                with open(Path(f"data/{tournament}/{year}.txt"), "r") as file:
                    text = file.read()
                print(f"Parsing {year} for {tournament}")
                for parse in parsers:
                    print(f"Parsing with {parse.__name__}")
                    # try:
                    results = parse(text, tournament_name, year)
                    print("Matches extracted:", len(results))
                    print("Matches expected:", assert_matches)
                    if len(results) == assert_matches:
                        break
                    # except Exception as err:
                    #     print(f"Error {str(err)}")
                    #     continue

                if len(results) != assert_matches:
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
                    dataframe.to_csv("error.csv", index=False)

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
                teams.update(list(dataframe["home_team"].unique()))
                teams.update(list(dataframe["away_team"].unique()))
    for team in sorted(list(teams)):
        print(team)


if __name__ == "__main__":
    main()
