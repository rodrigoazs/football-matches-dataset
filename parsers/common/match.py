import re

from parsers.common.date import convert_date


def get_match(line, year, date, stage):
    # El Nacional (Quito)       Ecu  Nacional (Asunción)       Par   0-5  3-3  3-8
    match_pattern = re.compile(
        r"([A-Za-zÀ-ÿ\s/\-\(\)\.]+)\s+\w{3}\s+([A-Za-zÀ-ÿ\s/\-\(\)\.]+)\s+\w{3}\s+(\d{1,2})\-(\d{1,2})\s+(\d{1,2})\-(\d{1,2})",
        re.UNICODE,
    )

    match = match_pattern.search(line)

    if match:
        match_home_team = match.group(1).strip()
        match_away_team = match.group(2).strip()
        match1_home_score = match.group(3)
        match1_away_score = match.group(4)
        match2_away_score = match.group(5)
        match2_home_score = match.group(6)
        return [
            [
                date[0],
                match_home_team,
                match1_home_score,
                match1_away_score,
                match_away_team,
                False,
                False,
                stage,
            ],
            [
                date[1],
                match_away_team,
                match2_home_score,
                match2_away_score,
                match_home_team,
                False,
                False,
                stage,
            ],
        ]

    # Feb 17: LDU (Quito) - Palmeiras               3-2
    match_pattern = re.compile(
        r"(\w{3}\s+\d{1,2})\:\s*([A-Za-zÀ-ÿ\s/\-\(\)\.]+)\s*[\-\–]{1}\s*([A-Za-zÀ-ÿ\s/\-\(\)\.]+)\s+(\d{1,2})\-(\d{1,2})",
        re.UNICODE,
    )

    match = match_pattern.search(line)

    if match:
        match_date = match.group(1)
        match_home_team = match.group(2).strip()
        match_away_team = match.group(3).strip()
        match1_home_score = match.group(4)
        match1_away_score = match.group(5)

        knockout = (
            True
            if stage in ["Round of 16", "Quarterfinal", "Semifinal", "Final"]
            else False
        )
        return [
            [
                convert_date(match_date, year),
                match_home_team,
                match1_home_score,
                match1_away_score,
                match_away_team,
                True,
                knockout,
                stage,
            ],
        ]

    #         Olimpia – Emelec                      2-3
    match_pattern = re.compile(
        r"([A-Za-zÀ-ÿ\s/\-\(\)\.]+)\s*[\-\–]{1}\s*([A-Za-zÀ-ÿ\s/\-\(\)\.]+)\s+(\d{1,2})\-(\d{1,2})",
        re.UNICODE,
    )

    match = match_pattern.search(line)

    if match:
        match_home_team = match.group(1).strip()
        match_away_team = match.group(2).strip()
        match1_home_score = match.group(3)
        match1_away_score = match.group(4)

        knockout = (
            True
            if stage in ["Round of 16", "Quarterfinal", "Semifinal", "Final"]
            else False
        )
        return [
            [
                date[0],
                match_home_team,
                match1_home_score,
                match1_away_score,
                match_away_team,
                True,
                knockout,
                stage,
            ],
        ]

    return None
