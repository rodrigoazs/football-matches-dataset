import re
from datetime import datetime


def _convert_date(date_string):
    # Map Portuguese abbreviations to English
    portuguese_to_english_months = {
        "jan": "jan",
        "fev": "feb",
        "mar": "mar",
        "abr": "apr",
        "mai": "may",
        "jun": "jun",
        "jul": "jul",
        "ago": "aug",
        "set": "sep",
        "out": "oct",
        "nov": "nov",
        "dez": "dec",
    }

    # Replace Portuguese month abbreviation with English
    for pt, en in portuguese_to_english_months.items():
        date_string = date_string.replace(pt, en)
    try:
        date_format = "%d %b %y"
        date_object = datetime.strptime(date_string, date_format)
        return date_object.strftime("%Y-%m-%d")
    except:
        raise Exception(date_string)


def format2_parser(text, year=None):
    # Initialize a list to hold the results
    results = []
    stage = "first"
    lines = text.split("\n")

    # Regular expression for capturing teams and scores, including accents
    match_pattern = re.compile(
        r"\[(\d{2} \w{3} \d{2})\]\s+\d{2}\:\d{2}\s+([0-9A-Za-zÀ-ÿ\s/-]+)\s+(\d+\s*)-(s*\d+)\s+([0-9A-Za-zÀ-ÿ\s/-]+)",
        re.UNICODE,
    )

    # Process each line
    for line in lines:
        match = match_pattern.match(line)

        if match:
            date = match.group(1)
            home_team = match.group(2).strip()
            home_score = match.group(3)
            away_score = match.group(4)
            away_team = match.group(5).strip()

            # Store the extracted data in results
            results.append(
                [
                    _convert_date(date),
                    home_team,
                    home_score,
                    away_score,
                    away_team,
                    False,
                    False,
                    stage,
                ]
            )

        if line.startswith("First Phase") or line.startswith("1a Fase"):
            stage = "first"

        if line.startswith("Second Phase") or line.startswith("2a Fase"):
            stage = "second"

        if line.startswith("Third Phase") or line.startswith("3a Fase"):
            stage = "third"

        if line.startswith("Fourth Phase") or line.startswith("4a Fase"):
            stage = "fourth"

        if line.startswith("Round16") or line.startswith("Oitavas de Final"):
            stage = "round16"

        if (
            line.startswith("Quarterfinals")
            or line.startswith("Quarterfinal")
            or line.startswith("Quartas de Final")
        ):
            stage = "quarter"

        if (
            line.startswith("Semifinals")
            or line.startswith("Semifinal")
            or line.startswith("Semi Finais")
        ):
            stage = "semi"

        if line.startswith("Final"):
            stage = "final"

        if line.startswith("Playoff"):
            stage = "relegation"

    return results
