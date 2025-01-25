from parsers.common.date import get_date
from parsers.common.match import get_match


def fix_name(name):        
    mapping = {
        "Wanderers": "Montevideo Wanderers",
        "EC Bahia": "Bahia",
        "J. Wilstermann": "Jorge Wilstermann",
        "Santos FC": "Santos",
        "Wanderers (Montevideo)": "Montevideo Wanderers",
        "Vélez Sarfield": "Vélez Sarsfield",
        "Vélez Sársfield": "Vélez Sarsfield",
        "Universitario (Sucre)": "Universitario de Sucre",
        "Universitario (Lima)": "Universitario",
        "Racing": "Racing Club",
        "Racing Club (Avellaneda)": "Racing Club",
        "Racing (Montevideo)": "Racing Club de Montevideo",
        "Paysandu SC (Belém)": "Paysandu",
        "Nacional (A)": "Club Nacional",
        "Nacional (A.)": "Club Nacional",
        "Nacional (Asunción)": "Club Nacional",
        "Nacional (M.)": "Nacional de Montevideo",
        "Nacional (Montevideo)": "Nacional de Montevideo",
        "Nacional": "Nacional de Montevideo",
        "Alianza": "Alianza Lima",
        "Alianza (Lima)": "Alianza Lima",
        "América (Cali)": "América de Cali",
        "América (Cd. de México)": "Club América",
        "América (Cdad. De México)": "Club América",
        "América (Cdad. de México)": "Club América",
        "América Mineiro": "América-MG",
        "Argentinos Jrs.": "Argentinos Juniors",
        "Argentino Juniors": "Argentinos Juniors",
        "Arsenal": "Arsenal de Sarandí",
        "Arsenal (Buenos Aires)": "Arsenal de Sarandí",
        "Ath. Paranaense (Curitiba": "Athletico-PR",
        "Athl. Paranaense": "Athletico-PR",
        "Athletico Paranaense": "Athletico-PR",
        "Atl. Paranaense": "Athletico-PR",
        "Atl. Colegiales": "Atlético Colegiales",
        "Atlético Junior": "Junior de Barranquilla",
        "Atl. Junior": "Junior de Barranquilla",
        "Atl. Junior (Barranquilla": "Junior de Barranquilla",
        "Atl.Junior (Barranquilla)": "Junior de Barranquilla",
        "Atl. Mineiro": "Atlético-MG",
        "Atl. Nacional": "Atlético Nacional",
        "Atl. Nacional (Medellín)": "Atlético Nacional",
        "Atl. Tucumán (San Miguel)": "Atlético Tucumán",
        "Atlas (Guadalajara)": "Atlas",
        "Atlético": "Atlético San Cristóbal",
        "Atlético Paranaense": "Athletico-PR",
        "Barcelona": "Barcelona de Guayaquil",
        "Barcelona (Guayaquil)": "Barcelona de Guayaquil",
        "Barcelona SC (Quito)": "Barcelona de Guayaquil",
        "Cerro (Montevideo)": "Cerro",
        "Cerro Largo (Melo)": "Cerro Largo",
        "Cerro Porteño (Asunción)": "Cerro Porteño",
        "Col. San Agustín": "San Agustín",
        "Colón (Santa Fe)": "Colón",
        "Defensor Sp. (Montevideo)": "Defensor Sporting Club",
        "Defensor Sporting": "Defensor Sporting Club",
        "Dep. Concepción": "Deportes Concepción",
    }
    for key, value in mapping.items():
        if name == key:
            return value

    return name


def fix_names(results):
    for result in results:
        result[1] = fix_name(result[1])
        result[4] = fix_name(result[4])
    return results


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

        try:
            matches = get_match(line, tournment, year, current_date, stage)
            if matches:
                results.extend(matches)
            # else:
            #     print(line)
        except:
            print('Error in:', f"'{line}'", tournment, year, current_date, stage)
            raise

        if line.startswith("Preliminary Round") or line.startswith("Qualifying Round"):
            stage = "Qualifying Round"

        if line.startswith("First Round"):
            stage = "Group Stage"

        if line.startswith("Group Phase") or line.startswith("Group Stage"):
            stage = "Group Stage"

        if (
            line.startswith("Second Phase")
            or line.startswith("Second Round")
            or line.startswith("1/8 Finals")
        ):
            stage = "Round of 16"

        if (
            line.startswith("Quarterfinals")
            or line.startswith("Quarterfinal")
            or line.lower().startswith("terceira fase")
            or line.startswith("Quarter-Finals")
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

    return fix_names(results)
