from parsers.common.date import get_date
from parsers.common.match import get_match


def fix_name(name):
    teams = [
        "Boca Juniors",
        "Bolívar",
        "Botafogo",
        "Boyacá Chicó",
        "Caracas",
        "Cienciano",
        "Cobreloa",
        "Colo Colo",
        "Corinthians",
        "Coritiba",
        "Cruz Azul",
        "Cruzeiro",
        "Danubio",
        "Delfín",
        "Flamengo",
        "Fluminense",
        "Goiás",
        "Grêmio",
        "Internacional",
        "Palmeiras",
        "Peñarol",
        "River Plate",
        "Sport",
        "São Paulo",
        "Vasco da Gama",
        "Vélez Sarsfield",
        "Unión Española",
        "Progreso",
        "Palestino",
        "Pachuca",
        "Once Caldas",
        "Olmedo",
        "Olimpia",
    ]
    for team in teams:
        if name.startswith(team):
            return team
        
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
    }
    for key, value in mapping.items():
        if name == key:
            return value
    
    # Barcelona SC (Quito)
    # Cerro
    # Cerro (Montevideo)
    # Cerro Largo (Melo)
    # Cerro Porteño
    # Cerro Porteño (Asunción)
    # Chaco Petrolero

    # Defensor
    # Defensor Arica
    # Defensor Sp. (Montevideo)
    # Defensor Sporting

    # Dep. Concepción
    # Dep. Indep. Medellín
    # Dep. La Guaira
    # Dep. Petare (Caracas)
    # Dep. Quito
    # Deportes Concepción
    # Deportes Iquique

    # Deportes Tolima
    # Deportes Tolima (Ibagué)
    # Deportivo Anzoátegui
    # Deportivo Binacional
    # Deportivo Cali
    # Deportivo Canarias
    # Deportivo Capiatá
    # Deportivo Cuenca
    # Deportivo Galicia
    # Deportivo ItalChacao
    # Deportivo Italia
    # Deportivo La Guaira
    # Deportivo Lara
    # Deportivo Municipal
    # Deportivo Municipal (Lima
    # Deportivo Pasto
    # Deportivo Portugués
    # Deportivo Quito
    # Deportivo Táchira
    # EC Bahia
    # El Nacional
    # El Nacional (Quito)
    # Emelec
    # Emelec (Guayaquil)
    # Espoli
    # Estudiantes
    # Estudiantes (La Plata)
    # Estudiantes (Mérida)
    # Estudiantes LP
    # Estudiantes-LP
    # Everest
    # Everton
    # Everton (Viña del Mar)
    # Ferro Carril Oeste
    # Filanbanco

    # Fortaleza
    # Fénix
    # Gimnasia y Esgrima
    # Godoy Cruz
    # Godoy Cruz (Mendoza)

    # Guabirá
    # Guadalajara
    # Guarani
    # Guaraní
    # Guaraní (Asunción)
    # Huachipato
    # Huracán
    # Huracán (Buenos Aires)
    # Ind. Medellín
    # Indep. José Terán
    # Indep. Medellín
    # Indep. Petrolero
    # Indep. Santa Fe
    # Indep. del Valle
    # Independiente
    # Independiente (Avellaneda
    # Independiente (Avellaneda)
    # Independiente José Terán
    # Independiente Medellín
    # Independiente Petrolero
    # Independiente Santa Fe
    # Independiente Sta. Fe
    # Independiente del Valle

    # Jaguares
    # Jaguares (Tuxtla Gtz.)

    # Juan Aurich
    # Juan Aurich (Chiclayo)
    # Junior
    # Junior (Barranquilla)
    # Juventude
    # LDU (Quito)
    # LDU Quito
    # LP
    # La Paz FC
    # Lanús
    # Lanús (Buenos Aires)
    # Lanús - Estudiantes
    # León
    # León de Huánuco
    # Libertad
    # Libertad (Asunción)
    # Litoral
    # Liverpool (Montevideo)
    # M. Wanderers
    # Macará (Ambato)
    # Magallanes
    # Mariano Melgar
    # Marítimo
    # Medellín
    # Melgar
    # Melgar (Arequipa)
    # Millonarios
    # Millonarios (Bogotá)
    # Mineros
    # Mineros de Guayana
    # Minervén
    # Monagas SC
    # Monterrey
    # Montevideo City Torque
    # Montevideo Wanderers
    # Morelia
    # Nacional
    # Nacional (A)
    # Nacional (A.)
    # Nacional (Asunción)
    # Nacional (M.)
    # Nacional (Montevideo)
    # Nacional Táchira
    # Necaxa
    # Newell's Old Boys
    # Nueve de Octubre
    # Náutico
    # O'Higgins
    # Olimpia
    # Olimpia (Asunción)
    # Olmedo
    # Olmedo (Riobamba)
    # Once Caldas
    # Once Caldas (Manizales)
    # Oriente Petrolero
    # Pachuca
    # Pachuca CF
    # Palestino
    # Palestino (Santiago)

    # Paraná
    # Paraná Clube (Curitiba)
    # Paulista FC
    # Paysandu
    # Paysandu SC (Belém)
    # Pepeganga
    # Peñarol
    # Peñarol (Montevideo)
    # Plaza Colonia
    # Portuguesa
    # Progreso
    # Progreso (Montevideo)
    # Puebla
    # Pumas UNAM
    # Pumas UNAM (Cd.de México)
    # Quilmes
    # Quilmes (Buenos Aires)
    # RB Bragantino
    # Racing
    # Racing (Montevideo)
    # Racing Club
    # Racing Club (Avellaneda)
    # Rangers
    # Real Garcilaso
    # Real Garcilaso (Cuzco)
    # Real Potosí
    # Rentistas

    # Rocha FC
    # Rosario Central
    # Royal Pari (Santa Cruz)
    # S. Wanderers
    # San José
    # San José (Oruro)
    # San Lorenzo
    # San Lorenzo de Almagro
    # San Luis
    # Santiago Wanderers
    # Santo Andre

    # Santos Laguna
    # Santos Laguna (Torreón)
    # Sol de América

    # Sport Boys
    # Sport Boys Warnes
    # Sport Huancayo
    # Sporting Cristal
    # Sporting Cristal (Lima)
    # Sportivo Luqueño
    # São Caetano

    # Tacuary
    # Tacuary (Asunción)
    # Talleres
    # Talleres (Córdoba)
    # The Strongest
    # The Strongest (La Paz)
    # Tigre
    # Tigre (Buenos Aires)
    # Tigres UANL
    # Tigres UANL (Monterrey)
    # Tijuana
    # Tolima
    # Toluca
    # Trujillanos
    # Tuluá
    # Táchira
    # Técnico Universitario
    # U. San Martín
    # U.T. Cajamarca
    # UA Maracaibo
    # Uni. Católica
    # Univ. Católica
    # Univ. Católica (Quito)
    # Univ. Católica (Santiago)
    # Univ. Los Andes
    # Univ. San Martín
    # Univ. de Chile
    # Univ. de Chile (Santiago)
    # Univ. de Concepción
    # Universidad Católica
    # Universidad César Vallejo
    # Universidad San Martín
    # Universidad de Chile
    # Universidad de Concepción
    # Universitario
    # Universitario (Lima)
    # Universitario (Sucre)
    # Universitario de Sucre
    # Unión Atlético Maracaibo
    # Unión Española
    # Unión Española (Santiago)
    # Unión Huaral
    # Unión La Calera
    # Unión Magdalena
    # Unión San Felipe
    # Valdez S.C.
    # Valencia

    # Vélez Sarfield
    # Vélez Sarsfield
    # Vélez Sarsfield (B Aires)
    # Vélez Sarsfield (B. Aires)
    # Vélez Sársfield
    # Wanderers
    # Wanderers (Montevideo)
    # Zamora
    # Zulia
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

        matches = get_match(line, tournment, year, current_date, stage)
        if matches:
            results.extend(matches)
        # else:
        #     print(line)

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
