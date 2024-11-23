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
    files = get_all_files(directory)
    result = None
    for file in files:
        if file.endswith(".csv"):
            df = pd.read_csv(file)
            if result is None:
                result = df
            else:
                result = pd.concat([result, df], axis=0)
    result["neutral"] = result["neutral"].astype(bool)
    result["knockout"] = result["knockout"].astype(bool)
    result.to_csv("results.csv", index=False)


if __name__ == "__main__":
    main()
