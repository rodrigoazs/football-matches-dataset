import re
from datetime import datetime


def _convert_date(date_string, year):
    try:
        date_format = "%b %d"
        date_object = datetime.strptime(date_string, date_format).replace(year=year)
        return date_object.strftime("%Y-%m-%d")
    except:
        raise Exception(date_string)


def format1_parser(text, year):
    # Initialize a list to hold the results
    results = []
    lines = text.split("\n")
    stage = "first"

    # Regular expression for capturing teams and scores, including accents
    match_pattern = re.compile(
        # r"([A-Za-zÀ-ÿ\s/-]+)\s+(\d+)-(\d+)\s+([A-Za-zÀ-ÿ\s/-]+)", re.UNICODE
        r"([A-Za-zÀ-ÿ\s/-]+)\s+(\d+\s*)-(s*\d+)\s+([A-Za-zÀ-ÿ\s/-]+)\s*(\[(\w{3} \d{1,2})\])*",
        re.UNICODE,
    )

    match_pattern_2 = re.compile(
        r"([A-Za-zÀ-ÿ\s/-]+)\s+(\d+s*)-(s*\d+)\s+(\d+s*)-(s*\d+)\s+([A-Za-zÀ-ÿ\s/-]+)\s*(\[(\w{3} \d{1,2})\])*",
        re.UNICODE,
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
                results.append(
                    [
                        _convert_date(date, year),
                        home_team,
                        home_score,
                        away_score,
                        away_team,
                        False,
                        False,
                        stage,
                    ]
                )
                results.append(
                    [
                        _convert_date(date, year),
                        away_team,
                        away_score2,
                        home_score2,
                        home_team,
                        False,
                        False,
                        stage,
                    ]
                )
                continue

            # Store the extracted data in results
            results.append(
                [
                    _convert_date(current_date, year),
                    home_team,
                    home_score,
                    away_score,
                    away_team,
                    False,
                    False,
                    stage,
                ]
            )
            results.append(
                [
                    _convert_date(current_date, year),
                    away_team,
                    away_score2,
                    home_score2,
                    home_team,
                    False,
                    False,
                    stage,
                ]
            )

        elif match:
            home_team = match.group(1).strip()
            home_score = match.group(2)
            away_score = match.group(3)
            away_team = match.group(4).strip()

            date = match.group(6)
            if date:
                results.append(
                    [
                        _convert_date(date, year),
                        home_team,
                        home_score,
                        away_score,
                        away_team,
                        False,
                        False,
                        stage,
                    ]
                )
                continue

            # Store the extracted data in results
            results.append(
                [
                    _convert_date(current_date, year),
                    home_team,
                    home_score,
                    away_score,
                    away_team,
                    False,
                    False,
                    stage,
                ]
            )

        # Check if the line contains a date
        date_match = re.search(r"\[(\w{3} \d{1,2})\]", line)
        if date_match:
            current_date = date_match.group(1)

        if line.startswith("First Phase"):
            stage = "first"

        if line.startswith("Second Phase"):
            stage = "second"

        if line.startswith("Third Phase"):
            stage = "third"

        if line.startswith("Quarterfinals") or line.startswith("Quarterfinal"):
            stage = "quarter"

        if line.startswith("Semifinals") or line.startswith("Semifinal"):
            stage = "semi"

        if line.startswith("Final"):
            stage = "final"

        if line.startswith("Playoff"):
            stage = "relegation"

    return results
