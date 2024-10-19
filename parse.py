import re

import requests

import pandas as pd
from datetime import datetime

FOLDER = "data/br/serie_a/"


def convert_date(date_string, year):
    try:
      date_format = "%b %d"
      date_object = datetime.strptime(date_string, date_format).replace(year=year)
      return date_object.strftime("%Y-%m-%d")
    except:
      raise Exception(date_string)


year = 1983

print(f"Parsing {year}")


lines = """

    """.split("\n")   

# Initialize a list to hold the results
results = []

# Regular expression for capturing teams and scores, including accents
match_pattern = re.compile(
    # r"([A-Za-zÀ-ÿ\s/-]+)\s+(\d+)-(\d+)\s+([A-Za-zÀ-ÿ\s/-]+)", re.UNICODE
    r"([A-Za-zÀ-ÿ\s/-]+)\s+(\d+\s*)-(s*\d+)\s+([A-Za-zÀ-ÿ\s/-]+)\s*(\[(\w{3} \d{1,2})\])*", re.UNICODE
)

match_pattern_2 = re.compile(
    r"([A-Za-zÀ-ÿ\s/-]+)\s+(\d+s*)-(s*\d+)\s+(\d+s*)-(s*\d+)\s+([A-Za-zÀ-ÿ\s/-]+)\s*(\[(\w{3} \d{1,2})\])*", re.UNICODE
)

# Process each line
for line in lines:
    # line = line.strip()

    match_2 = match_pattern_2.match(line)
    match = match_pattern.match(line)

    if match_2:
        home_team = match_2.group(1).strip()
        home_score = match_2.group(2)
        away_score = match_2.group(3)
        home_score2 = match_2.group(4)
        away_score2 = match_2.group(5)
        away_team = match_2.group(6).strip()
        
        date = match_2.group(7)
        if date:
          results.append([convert_date(date, year), home_team, home_score, away_score, away_team, False, False, "first"])
          results.append([convert_date(date, year), away_team, away_score2, home_score2, home_team, False, False, "first"])
          continue

        # Store the extracted data in results
        results.append([convert_date(current_date, year), home_team, home_score, away_score, away_team, False, False, "first"])
        results.append([convert_date(current_date, year), away_team, away_score2, home_score2, home_team, False, False, "first"])

    elif match:
        home_team = match.group(1).strip()
        home_score = match.group(2)
        away_score = match.group(3)
        away_team = match.group(4).strip()
        
        date = match.group(6)
        if date:
          results.append([convert_date(date, year), home_team, home_score, away_score, away_team, False, False, "first"])
          continue

        # Store the extracted data in results
        results.append([convert_date(current_date, year), home_team, home_score, away_score, away_team, False, False, "first"])
        
    # Check if the line contains a date
    date_match = re.search(r"\[(\w{3} \d{1,2})\]", line)
    if date_match:
        current_date = date_match.group(1)

print("Matches:", len(results))
assert len(results) == 306

dataframe = pd.DataFrame(results, columns=["date", "home_team", "home_score", "away_score", "away_team", "neutral", "knockout", "stage"])
dataframe.to_csv(FOLDER + str(year) + ".csv")
