import re
from datetime import datetime


def convert_date(date_string, year):
    for date_format in ["%b %d %Y", "%d %b %Y"]:
        try:
            date_object = datetime.strptime(f"{date_string} {year}", date_format)
            return date_object.strftime("%Y-%m-%d")
        except:
            continue
    for date_format in ["%Y-%m-%d", "%d-%m-%y"]:
        try:
            date_object = datetime.strptime(f"{date_string}", date_format)
            return date_object.strftime("%Y-%m-%d")
        except:
            continue
    raise Exception(f"Date error: {date_string}.")


def get_date(line, year):
    # (May 14-21)
    match_date = re.compile(
        r"[\[\(]{1}(\w{3})\s+(\d{1,2})\s*(?:[\s\,\;\-\&]+|and)\s*(\d{1,2})[\]\)]{1}",
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

    # (Jan 5 and 12, 2021)
    match_date = re.compile(
        r"[\[\(]{1}(\w{3})\s+(\d{1,2})\s*(?:[\s\,\;\-\&]+|and)\s*(\s\d{1,2})[\,\;]\s*(\d{4})",
        re.UNICODE,
    )

    match = match_date.search(line)

    if match:
        match_month = match.group(1)
        match_day_1 = match.group(2)
        match_day_2 = match.group(3)
        match_year = match.group(4)
        return [
            convert_date(f"{match_month} {match_day_1}", match_year),
            convert_date(f"{match_month} {match_day_2}", match_year),
        ]

    # Final (Jan 30, 2021, Rio de Janeiro)
    match_date = re.compile(
        r"[\[\(]{1}(\w{3} +\d{1,2})[\,\;]\s*(\d{4})",
        re.UNICODE,
    )

    match = match_date.search(line)

    if match:
        match_date_1 = match.group(1)
        match_year = match.group(2)
        return [
            convert_date(match_date_1, match_year),
            None,
        ]

    return None
