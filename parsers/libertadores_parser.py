from parsers.common.date import get_date
from parsers.common.match import get_match


def libertadores_parser(text, tournment, year):
    # Initialize a list to hold the results
    results = []
    lines = text.split("\n")
    stage = ""
    current_date = None

    for line in lines:
        dates = get_date(line, year)
        if dates:
            current_date = dates

        matches = get_match(line, tournment, year, current_date, stage)
        if matches:
            results.extend(matches)
        # else:
        #     print(line)

        if line.startswith("Preliminary Round") or line.startswith("Qualifying Round"):
            stage = "Qualifying Round"

        if line.startswith("Group Phase") or line.startswith("Group Stage"):
            stage = "Group Stage"

        if line.startswith("Second Phase") or line.startswith("Second Round") or line.startswith("1/8 Finals"):
            stage = "Round of 16"

        if (
            line.startswith("Quarterfinals")
            or line.startswith("Quarterfinal")
            or line.lower().startswith("terceira fase")
        ):
            stage = "Quarterfinal"

        if (
            line.startswith("Semifinals")
            or line.startswith("Semi-Finals")
            or line.startswith("Semifinal")
            or line.lower().startswith("semi final")
        ):
            stage = "Semifinal"

        if line.lower().startswith("final"):
            stage = "Final"

        if line.startswith("Playoff"):
            stage = "Relegation"

    return results
