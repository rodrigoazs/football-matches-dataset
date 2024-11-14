import re
from datetime import datetime


def convert_date(date_string, year):
    for date_format in ["%b %d"]:
        try:
            date_object = datetime.strptime(date_string, date_format).replace(year=year)
            return date_object.strftime("%Y-%m-%d")
        except:
            continue
    raise Exception(date_string)


def get_date(line, year):
    # (Jan 27-Feb 5)
    match_date = re.compile(
        r"[\[\(]{1}(\w{3}\s\d{1,2})\s*[\s\,\;\-\&]+\s*(\w{3}\s\d{1,2})[\]\)]{1}",
        re.UNICODE,
    )

    match = match_date.search(line)

    if match:
        match_date_1 = match.group(1)
        match_date_2 = match.group(2)
        return [convert_date(match_date_1, year), convert_date(match_date_2, year)]

    # (May 14-21)
    match_date = re.compile(
        r"[\[\(]{1}(\w{3})\s(\d{1,2})\s*[\s\,\;\-\&]+\s*(\d{1,2})[\]\)]{1}",
        re.UNICODE,
    )

    match = match_date.search(line)

    if match:
        match_month = match.group(1)
        match_day_1 = match.group(2)
        match_day_2 = match.group(3)
        return [
            convert_date(f"{match_month} {match_day_1}", year),
            convert_date(f"{match_month} {match_day_2}", year),
        ]

    # Feb 17: LDU (Quito) - Palmeiras               3-2
    match_date = re.compile(
        r"(\w{3}\s+\d{1,2})\:\s*[A-Za-zÀ-ÿ\s/\-\(\)\.]+\s*[\-\–]{1}\s*[A-Za-zÀ-ÿ\s/\-\(\)\.]+\s+\d{1,2}\-\d{1,2}",
        re.UNICODE,
    )

    match = match_date.search(line)

    if match:
        match_date_1 = match.group(1)
        return [
            convert_date(match_date_1, year),
            None,
        ]

    return None
