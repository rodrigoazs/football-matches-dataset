import re
from datetime import datetime


def _convert_date(date_string, year):
    try:
        date_format = "%d/%m"
        date_object = datetime.strptime(date_string, date_format).replace(year=year)
        return date_object.strftime("%Y-%m-%d")
    except:
        raise Exception(date_string)


def format3_parser(text, year):
    # Initialize a list to hold the results
    results = []
    lines = text.split("\n")
    stage = "first"
    neutral = False
    knockout = False

    # Regular expression for capturing teams and scores, including accents
    match_pattern = re.compile(
        r"\s([A-Za-zÀ-ÿ\s/\-\(\)\.]+)\s\-\s([A-Za-zÀ-ÿ\s/\-\(\)\.]+)\s+((\d{1,2})\-(\d{1,2})|n\/p)\s+\((\d{1,2}\/\d{1,2})\)\s+((\d{1,2})\-(\d{1,2})|n\/p)\s+\((\d{1,2}\/\d{1,2})\)",
        re.UNICODE,
    )

    # Process each line
    for line in lines:
        match = match_pattern.search(line)

        if match:
            match1_home_team = match.group(1).strip()
            match1_away_team = match.group(2).strip()
            match1_score = match.group(3)
            match1_home_score = match.group(4)
            match1_away_score = match.group(5)
            match1_date = match.group(6)
            match2_score = match.group(7)
            match2_away_score = match.group(8)
            match2_home_score = match.group(9)
            match2_date = match.group(10)

            if match1_score != "n/p":
                results.append(
                    [
                        _convert_date(match1_date, year),
                        match1_home_team,
                        match1_home_score,
                        match1_away_score,
                        match1_away_team,
                        neutral,
                        knockout,
                        stage,
                    ]
                )

            if match2_score != "n/p":
                results.append(
                    [
                        _convert_date(match2_date, year),
                        match1_away_team,
                        match2_home_score,
                        match2_away_score,
                        match1_home_team,
                        neutral,
                        knockout,
                        stage,
                    ]
                )

        if line.startswith("First Phase") or line.startswith("First Round"):
            stage = "first"

        if line.startswith("Second Phase") or line.startswith("Second Round"):
            stage = "second"

        if line.startswith("Third Phase") or line.startswith("Third Round"):
            stage = "round16"

        if line.startswith("1/8 Finals"):
            stage = "round16"

        if line.startswith("Quarterfinals") or line.startswith("Quarterfinal"):
            stage = "quarter"

        if line.startswith("Semifinals") or line.startswith("Semifinal"):
            stage = "semi"

        if line.lower().startswith("final"):
            stage = "final"

        if line.startswith("Playoff"):
            stage = "relegation"

    return results
