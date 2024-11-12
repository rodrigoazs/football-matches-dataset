import os

import pandas as pd

tournaments = {
    "brasileirao-serie-a": "Brasileirão Série A 2024",
    "copa-do-brasil": "Copa do Brasil",
}

directory = "data/country/bra/copa-do-brasil"


def get_all_files(directory):
    all_files = []
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            all_files.append(os.path.join(dirpath, filename))
    return all_files


def main():
    files = get_all_files(directory)
    for file in files:
        info = file.split("/")
        tournament = info[-2]
        year = int(info[-1].replace(".csv", ""))
        df = pd.read_csv(file)
        df["tournament_name"] = tournaments[tournament]
        df["tournament_year"] = year
        df.to_csv(f"{directory}/{year}.csv", index=False)


if __name__ == "__main__":
    main()
