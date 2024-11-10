import pandas as pd

from parsers import *

FOLDER = "data/country/bra/copa-do-brasil/"
YEAR = 1989
MATCHES = 61

parsers = [parse for name, parse in globals().items() if name.endswith("_parser")]
with open("text.txt", "r") as file:
    text = file.read()


def main():
    print(f"Parsing {YEAR}")
    for parse in parsers:
        print(f"Parsing with {parse.__name__}")
        results = parse(text, YEAR)
        print("Matches extracted:", len(results))
        if len(results) == MATCHES:
            break

    assert len(results) == MATCHES

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
        ],
    )
    dataframe.to_csv(FOLDER + str(YEAR) + ".csv", index=False)


if __name__ == "__main__":
    main()
