import re

from parsers.common.date import convert_date


def get_match(line, tournament, year, date, stage):
    # Boca Juniors (Bs. Aires)  Arg  Newell's Old Boys         Arg   0-0  0-0  0-0  9-10p
    match_pattern = re.compile(
        r"([0-9A-Za-zÀ-ÿ\s/\-\(\)\.\']+)\s+(?:Arg|Chi|Ven|Bra|Uru|Par|Bol|Ecu|Col|Per|Mex|USA|CRi)\s+([0-9A-Za-zÀ-ÿ\s/\-\(\)\.\']+)\s+(?:Arg|Chi|Ven|Bra|Uru|Par|Bol|Ecu|Col|Per|Mex|USA|CRi)\s+(\d{1,2})\-(\d{1,2})\s+(\d{1,2})\-(\d{1,2})",
        re.UNICODE,
    )

    match = match_pattern.search(line)

    if not match:
        # El Nacional (Quito)       Ecu  Nacional (Asunción)       Par   0-5  3-3  3-8
        match_pattern = re.compile(
            r"([0-9A-Za-zÀ-ÿ\s/\-\(\)\.\']+)(?:\s+|\))[A-Z]{1}[a-z]{2}\s+([0-9A-Za-zÀ-ÿ\s/\-\(\)\.\']+)(?:\s+|\))[A-Z]{1}[a-z]{2}\s+(\d{1,2})\-(\d{1,2})\s+(\d{1,2})\-(\d{1,2})",
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
                stage,
                tournament,
                year,
            ],
            [
                date[1],
                match_away_team,
                match2_home_score,
                match2_away_score,
                match_home_team,
                False,
                stage,
                tournament,
                year,
            ],
        ]

    # River Plate               Arg  Boca Juniors              Arg   1-0  abd  4-0x
    match_pattern = re.compile(
        r"([0-9A-Za-zÀ-ÿ\s/\-\(\)\.\']+)\s+[A-Z]{1}[a-z]{2}\s+([0-9A-Za-zÀ-ÿ\s/\-\(\)\.\']+)\s+[A-Z]{1}[a-z]{2}\s+(\d{1,2})\-(\d{1,2})\s+abd",
        re.UNICODE,
    )

    match = match_pattern.search(line)

    if match:
        match_home_team = match.group(1).strip()
        match_away_team = match.group(2).strip()
        match1_home_score = match.group(3)
        match1_away_score = match.group(4)
        return [
            [
                date[0],
                match_home_team,
                match1_home_score,
                match1_away_score,
                match_away_team,
                False,
                stage,
                tournament,
                year,
            ],
        ]
    
    # Tacuary FC                Par  Club General Caballero    Par   2-2
    match_pattern = re.compile(
        r"([0-9A-Za-zÀ-ÿ\s/\-\(\)\.\']+)\s+(?:Arg|Chi|Ven|Bra|Uru|Par|Bol|Ecu|Col|Per|Mex|USA|CRi)\s+([0-9A-Za-zÀ-ÿ\s/\-\(\)\.\']+)\s+(?:Arg|Chi|Ven|Bra|Uru|Par|Bol|Ecu|Col|Per|Mex|USA|CRi)\s+(\d{1,2})\-(\d{1,2})",
        re.UNICODE,
    )

    match = match_pattern.search(line)

    if match:
        match_home_team = match.group(1).strip()
        match_away_team = match.group(2).strip()
        match1_home_score = match.group(3)
        match1_away_score = match.group(4)
        return [
            [
                date[0],
                match_home_team,
                match1_home_score,
                match1_away_score,
                match_away_team,
                False,
                stage,
                tournament,
                year,
            ],
        ]

    # Feb 17: LDU (Quito) - Palmeiras               3-2
    match_pattern = re.compile(
        r"(\w{3}\s+\d{1,2})\:\s*([0-9A-Za-zÀ-ÿ\s/\-\(\)\.\']+)\s*[\-\–]{1}\s*([0-9A-Za-zÀ-ÿ\s/\-\(\)\.\']+)\s+(\d{1,2})\-(\d{1,2})",
        re.UNICODE,
    )

    match = match_pattern.search(line)

    if match:
        match_date = match.group(1)
        match_home_team = match.group(2).strip()
        match_away_team = match.group(3).strip()
        match1_home_score = match.group(4)
        match1_away_score = match.group(5)

        return [
            [
                convert_date(match_date, year),
                match_home_team,
                match1_home_score,
                match1_away_score,
                match_away_team,
                False,
                stage,
                tournament,
                year,
            ],
        ]

    # 24 Apr: Alianza - Millonarios                   0-0
    match_pattern = re.compile(
        r"(\d{1,2}\s+\w{3})\:\s*([0-9A-Za-zÀ-ÿ\s/\-\(\)\.\']+)\s*[\-\–]{1}\s*([0-9A-Za-zÀ-ÿ\s/\-\(\)\.\']+)\s+(\d{1,2})\-(\d{1,2})",
        re.UNICODE,
    )

    match = match_pattern.search(line)

    if match:
        match_date = match.group(1)
        match_home_team = match.group(2).strip()
        match_away_team = match.group(3).strip()
        match1_home_score = match.group(4)
        match1_away_score = match.group(5)

        return [
            [
                convert_date(match_date, year),
                match_home_team,
                match1_home_score,
                match1_away_score,
                match_away_team,
                False,
                stage,
                tournament,
                year,
            ],
        ]
    
    # 2005-12-11 19:20    Al-Ittihad      1-0 Al-Ahly           (Tokyo)
    match_pattern = re.compile(
        r"(\d{4}-\d{2}-\d{2})\s+\d{2}:\d{2}\s+([0-9A-Za-zÀ-ÿ\s/\-\(\)\.\']+)\s+(\d{1,2})\-(\d{1,2})\s+([0-9A-Za-zÀ-ÿ\s/\-\(\)\.\']+)\s+\(.*?\)",
        re.UNICODE,
    )

    match = match_pattern.search(line)

    if match:
        match_date = match.group(1)
        match_home_team = match.group(2).strip()
        match_away_team = match.group(5).strip()
        match1_home_score = match.group(3)
        match1_away_score = match.group(4)

        return [
            [
                convert_date(match_date, year),
                match_home_team,
                match1_home_score,
                match1_away_score,
                match_away_team,
                False,
                stage,
                tournament,
                year,
            ],
        ]
    
    # 17-12-08 19:30    Pachuca       0-2 LDU de Quito            Tokyo
    match_pattern = re.compile(
        r"(\d{2}-\d{2}-\d{2})\s+\d{2}:\d{2}\s+([0-9A-Za-zÀ-ÿ\s/\-\(\)\.\']+)\s+(\d{1,2})\-(\d{1,2})\s+([0-9A-Za-zÀ-ÿ\s/\-\(\)\.\']+)\s+[A-Za-z\s]+",
        re.UNICODE,
    )

    match = match_pattern.search(line)

    if match:
        match_date = match.group(1)
        match_home_team = match.group(2).strip()
        match_away_team = match.group(5).strip()
        match1_home_score = match.group(3)
        match1_away_score = match.group(4)

        return [
            [
                convert_date(match_date, year),
                match_home_team,
                match1_home_score,
                match1_away_score,
                match_away_team,
                False,
                stage,
                tournament,
                year,
            ],
        ]
    
    # 10-12-06    Auckland City    0-2 Al-Ahly          (19:20 Toyota)
    match_pattern = re.compile(
        r"(\d{2}-\d{2}-\d{2})\s+([0-9A-Za-zÀ-ÿ\s/\-\(\)\.\']+)\s+(\d{1,2})\-(\d{1,2})\s+([0-9A-Za-zÀ-ÿ\s/\-\(\)\.\']+)\s+[\(\[].*?\)",
        re.UNICODE,
    )

    match = match_pattern.search(line)

    if match:
        match_date = match.group(1)
        match_home_team = match.group(2).strip()
        match_away_team = match.group(5).strip()
        match1_home_score = match.group(3)
        match1_away_score = match.group(4)

        return [
            [
                convert_date(match_date, year),
                match_home_team,
                match1_home_score,
                match1_away_score,
                match_away_team,
                False,
                stage,
                tournament,
                year,
            ],
        ]
    
    # 1-2-23    Al-Ahly               3-0 Auckland City                        Tanger
    match_pattern = re.compile(
        r"(\d{1,2}-\d{1,2}-\d{1,2})\s+([0-9A-Za-zÀ-ÿ\s/\-\(\)\.\']+)\s+(\d{1,2})\-(\d{1,2})\s+([0-9A-Za-zÀ-ÿ\s/\-\(\)\.\']+)\s\s+",
        re.UNICODE,
    )

    match = match_pattern.search(line)

    if match:
        match_date = match.group(1)
        match_home_team = match.group(2).strip()
        match_away_team = match.group(5).strip()
        match1_home_score = match.group(3)
        match1_away_score = match.group(4)

        return [
            [
                convert_date(match_date, year),
                match_home_team,
                match1_home_score,
                match1_away_score,
                match_away_team,
                False,
                stage,
                tournament,
                year,
            ],
        ]
    
    # 09-12-09       Al-Ahli Dubai    0-2 Auckland City
    match_pattern = re.compile(
        r"(\d{1,2}-\d{1,2}-\d{1,2})\s+([0-9A-Za-zÀ-ÿ\s/\-\(\)\.\']+)\s+(\d{1,2})\-(\d{1,2})\s+([0-9A-Za-zÀ-ÿ\s/\-\(\)\.\']+)",
        re.UNICODE,
    )

    match = match_pattern.search(line)

    if match:
        match_date = match.group(1)
        match_home_team = match.group(2).strip()
        match_away_team = match.group(5).strip()
        match1_home_score = match.group(3)
        match1_away_score = match.group(4)

        return [
            [
                convert_date(match_date, year),
                match_home_team,
                match1_home_score,
                match1_away_score,
                match_away_team,
                False,
                stage,
                tournament,
                year,
            ],
        ]

    #         Olimpia – Emelec                      2-3
    match_pattern = re.compile(
        r"([0-9A-Za-zÀ-ÿ\s/\-\(\)\.\']+)\s*[\-\–]{1}\s*([0-9A-Za-zÀ-ÿ\s/\-\(\)\.\']+)\s+(\d{1,2})\-(\d{1,2})",
        re.UNICODE,
    )

    match = match_pattern.search(line)

    if match:
        match_home_team = match.group(1).strip()
        match_away_team = match.group(2).strip()
        match1_home_score = match.group(3)
        match1_away_score = match.group(4)

        return [
            [
                date[0],
                match_home_team,
                match1_home_score,
                match1_away_score,
                match_away_team,
                False,
                stage,
                tournament,
                year,
            ],
        ]

    # River Plate (Bs. Aires)   Arg  Flamengo (Rio de Janeiro) Bra   1-2
    match_pattern = re.compile(
        r"([0-9A-Za-zÀ-ÿ\s/\-\(\)\.\']+)(?:\s+|\))[A-Z]{1}[a-z]{2}\s+([0-9A-Za-zÀ-ÿ\s/\-\(\)\.\']+)(?:\s+|\))[A-Z]{1}[a-z]{2}\s+(\d{1,2})\-(\d{1,2})",
        re.UNICODE,
    )

    match = match_pattern.search(line)

    if match:
        match_home_team = match.group(1).strip()
        match_away_team = match.group(2).strip()
        match1_home_score = match.group(3)
        match1_away_score = match.group(4)

        return [
            [
                date[0],
                match_home_team,
                match1_home_score,
                match1_away_score,
                match_away_team,
                False,
                stage,
                tournament,
                year,
            ],
        ]

    # check if should be parsed
    match_pattern = re.compile(
        r"[^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)]\s\d{1,2}\-\d{1,2}",
        re.UNICODE,
    )

    match = match_pattern.search(line)

    if match:
        raise Exception("Not parsed", line)

    return None
