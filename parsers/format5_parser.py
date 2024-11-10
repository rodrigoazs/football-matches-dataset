import re
from datetime import datetime


def _convert_date(date_string, year):
    try:
        date_format = "%b %d"
        date_object = datetime.strptime(date_string, date_format).replace(year=year)
        return date_object.strftime("%Y-%m-%d")
    except:
        raise Exception(date_string)


def format5_parser(text, year):
    # Initialize a list to hold the results
    results = []
    lines = text.split("\n")
    stage = "first"
    neutral = False
    knockout = False
    current_date = None

    # Regular expression for capturing teams and scores, including accents
    match_1_match_pattern = re.compile(
        r"([A-Za-zÀ-ÿ\s/\-\(\)\.]+)\s+(\d{1,2})\-(\d{1,2})\s+([A-Za-zÀ-ÿ\s/\-\(\)\.]+)",
        re.UNICODE,
    )

    match_2_matches_pattern = re.compile(
        r"([A-Za-zÀ-ÿ\s/\-\(\)\.]+)\s+(\d{1,2})\-(\d{1,2})\s+(\d{1,2})\-(\d{1,2})\s+([A-Za-zÀ-ÿ\s/\-\(\)\.]+)",
        re.UNICODE,
    )

    match_1_match_date = re.compile(
        r"\[(\w{3} \d{1,2})\]",
        re.UNICODE,
    )

    match_2_matches_date_1 = re.compile(
        r"\[(\w{3} \d{1,2})(?:\sand|;|,)\s(\w{3} \d{1,2})\]",
        re.UNICODE,
    )

    match_2_matches_date_2 = re.compile(
        r"\[(\w{3})\s(\d{1,2})(?:\sand\s|; |, )(\d{1,2})\]",
        re.UNICODE,
    )

    # Process each line
    for line in lines:
        match = match_1_match_date.search(line)

        if match:
            match_date = match.group(1)
            current_date = match_date

        match = match_2_matches_date_1.search(line)

        if match:
            match1_date = match.group(1)
            match2_date = match.group(2)
            current_date = [match1_date, match2_date]

        match = match_2_matches_date_2.search(line)

        if match:
            match_date_month = match.group(1)
            match1_date = match.group(2)
            match2_date = match.group(3)
            current_date = [
                f"{match_date_month} {match1_date}",
                f"{match_date_month} {match2_date}",
            ]

        match = match_2_matches_pattern.search(line)

        if match:
            match1_home_team = match.group(1).strip()
            match1_away_team = match.group(6).strip()
            match1_home_score = match.group(2)
            match1_away_score = match.group(3)
            match2_away_score = match.group(4)
            match2_home_score = match.group(5)

            results.append(
                [
                    _convert_date(current_date[0], year),
                    match1_home_team,
                    match1_home_score,
                    match1_away_score,
                    match1_away_team,
                    neutral,
                    knockout,
                    stage,
                ]
            )
            results.append(
                [
                    _convert_date(current_date[1], year),
                    match1_away_team,
                    match2_home_score,
                    match2_away_score,
                    match1_home_team,
                    neutral,
                    knockout,
                    stage,
                ]
            )

        else:
            match = match_1_match_pattern.search(line)

            if match:
                print(match.groups())
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
