import os

import pandas as pd

directory = "data"


def get_all_files(directory):
    all_files = []
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            all_files.append(os.path.join(dirpath, filename))
    return all_files


def main():
    teams = set()
    files = get_all_files(directory)
    for file in files:
        print(file)
        df = pd.read_csv(file)
        teams.update(list(df["home_team"].unique()))
        teams.update(list(df["away_team"].unique()))
    teams = sorted(list(teams))
    for team in teams:
        print(team)


if __name__ == "__main__":
    main()
