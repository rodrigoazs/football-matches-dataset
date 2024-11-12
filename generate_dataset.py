import os

import pandas as pd

tournaments = {
    "brasileirao-serie-a": "Brasileirao Serie A",
    "copa-do-brasil": "Copa do Brasil",
}

directory = "data"


def get_all_files(directory):
    all_files = []
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            all_files.append(os.path.join(dirpath, filename))
    return all_files


def main():
    files = get_all_files(directory)
    result = None
    for file in files:
        info = file.split("/")
        tournament = info[-2]
        year = int(info[-1].replace(".csv", ""))
        df = pd.read_csv(file)
        df["tournament_name"] = tournaments[tournament]
        df["tournament_year"] = year
        if result is None:
            result = df
        else:
            result = pd.concat([result, df], axis=0)
    result.to_csv("results.csv", index=False)


if __name__ == "__main__":
    main()
