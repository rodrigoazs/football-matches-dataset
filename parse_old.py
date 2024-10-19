import re

import requests

import pandas as pd
from datetime import datetime

FOLDER = "data/br/serie_a/"

championships = [
    # {"year": 2023, "link": "https://rsssfbrasil.com/tablesae/br2023.htm"},
    # {"year": 2022, "link": "https://rsssfbrasil.com/tablesae/br2022.htm"},
    # {"year": 2021, "link": "https://rsssfbrasil.com/tablesae/br2021.htm"},
    # {"year": 2020, "link": "https://rsssfbrasil.com/tablesae/br2020.htm"},
    # {"year": 2019, "link": "https://rsssfbrasil.com/tablesae/br2019.htm"},
    # {"year": 2018, "link": "https://rsssfbrasil.com/tablesae/br2018.htm"},
    # {"year": 2017, "link": "https://rsssfbrasil.com/tablesae/br2017.htm"},
    # {"year": 2016, "link": "https://rsssfbrasil.com/tablesae/br2016.htm"},
    # {"year": 2015, "link": "https://rsssfbrasil.com/tablesae/br2015.htm"},
    # {"year": 2014, "link": "https://rsssfbrasil.com/tablesae/br2014.htm"},
    # {"year": 2013, "link": "https://rsssfbrasil.com/tablesae/br2013.htm"},
    # {"year": 2012, "link": "https://rsssfbrasil.com/tablesae/br2012.htm"},
    # {"year": 2011, "link": "https://rsssfbrasil.com/tablesae/br2011.htm"},
    # {"year": 2010, "link": "https://rsssfbrasil.com/tablesae/br2010.htm"},
    # {"year": 2009, "link": "https://rsssfbrasil.com/tablesae/br2009.htm"},
    # {"year": 2008, "link": "https://rsssfbrasil.com/tablesae/br2008.htm"},
    # {"year": 2007, "link": "https://rsssfbrasil.com/tablesae/br2007.htm"},
    # {"year": 2006, "link": "https://rsssfbrasil.com/tablesae/br2006.htm"},
    # {"year": 2005, "link": "https://rsssfbrasil.com/tablesae/br2005.htm"},
    {"year": 2003, "link": "https://rsssfbrasil.com/tablesae/br2003.htm"},
]


def convert_date(date_string, year):
    date_format = "%b %d"
    date_object = datetime.strptime(date_string, date_format).replace(year=year)
    return date_object.strftime("%Y-%m-%d")


for championship in championships:
    year = championship["year"]
    link = championship["link"]

    print(f"Parsing {year} in link {link}")
    
    response = requests.get(link)

    if response.status_code == 200:
        
        # try:
        #     lines = response.content.decode("utf-8").split("\n")
        # except:
        #     pass

        # try:
        #     lines = response.content.decode("latin1").split("\n")
        # except:
        #     pass

        lines = """


        """.split("\n")   

        # Initialize a list to hold the results
        results = []

        # Regular expression for capturing teams and scores, including accents
        match_pattern = re.compile(
            r"([A-Za-zÀ-ÿ\s/-]+)\s+(\d+)-(\d+)\s+([A-Za-zÀ-ÿ\s/-]+)", re.UNICODE
        )

        # Process each line
        for line in lines:
            # line = line.strip()

            # Check if the line contains a date
            date_match = re.search(r"\[(\w{3} \d{1,2})\]", line)
            if date_match:
                current_date = date_match.group(1)

            # Check if the line contains a match (team and score)
            else:
                match = match_pattern.match(line)
                if match:
                    home_team = match.group(1).strip()
                    home_score = match.group(2)
                    away_score = match.group(3)
                    away_team = match.group(4).strip()

                    # Store the extracted data in results
                    results.append([convert_date(current_date, year), home_team, home_score, away_score, away_team, False])

        print("Matches:", len(results))
        assert len(results) == 552

        dataframe = pd.DataFrame(results, columns=["date", "home_team", "home_score", "away_score", "away_team", "neutral"])
        dataframe.to_csv(FOLDER + str(year) + ".csv")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
