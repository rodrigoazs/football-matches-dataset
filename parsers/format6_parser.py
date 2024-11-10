import re
from datetime import datetime


def _convert_date(date_string, year):
    try:
        date_format = "%d/%m/%Y"
        date_object = datetime.strptime(date_string, date_format).replace(year=year)
        return date_object.strftime("%Y-%m-%d")
    except:
        raise Exception(date_string)


def format6_parser(text, year):
    # Initialize a list to hold the results
    results = []
    lines = text.split("\n")
    stage = "first"
    neutral = False
    knockout = False
    current_date = None

    # Regular expression for capturing teams and scores, including accents
    match_pattern = re.compile(
        r"([A-Za-zÀ-ÿ\s/\-\(\)\.]+)\s+(\d{1,2})x(\d{1,2})\s+([A-Za-zÀ-ÿ\s/\-\(\)\.]+)\s\s",
        re.UNICODE,
    )

    match_date = re.compile(
        r"(\d{2}\/\d{2}\/\d{4})",
        re.UNICODE,
    )

    # Process each line
    for line in lines:
        match = match_date.search(line)

        if match:
            current_date = match.group(1)

        match = match_pattern.search(line)

        if match:
            match_home_team = match.group(1).strip()
            match_away_team = match.group(4).strip()
            match_home_score = match.group(2)
            match_away_score = match.group(3)

            results.append(
                [
                    _convert_date(current_date, year),
                    match_home_team,
                    match_home_score,
                    match_away_score,
                    match_away_team,
                    neutral,
                    knockout,
                    stage,
                ]
            )

        if line.startswith("First Phase") or line.startswith("First Round"):
            stage = "first"

        if line.startswith("Second Phase") or line.startswith("Second Round"):
            stage = "round16"

        if line.startswith("Third Phase") or line.startswith("Third Round"):
            stage = "round16"

        if line.startswith("1/8 Finals") or line.lower().startswith("segunda fase"):
            stage = "round16"

        if line.startswith("Quarterfinals") or line.startswith("Quarterfinal") or line.lower().startswith("terceira fase"):
            stage = "quarter"

        if line.startswith("Semifinals") or line.startswith("Semifinal") or line.lower().startswith("semi final"):
            stage = "semi"

        if line.lower().startswith("final"):
            stage = "final"

        if line.startswith("Playoff"):
            stage = "relegation"

    return results
