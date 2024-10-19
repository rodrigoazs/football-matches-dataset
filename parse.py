import re

import requests

import pandas as pd
from datetime import datetime

FOLDER = "data/br/serie_a/"


def convert_date(date_string, year):
    date_format = "%b %d"
    date_object = datetime.strptime(date_string, date_format).replace(year=year)
    return date_object.strftime("%Y-%m-%d")


year = 1987

print(f"Parsing {year}")


lines = """
First Stage
Teams in Group A play against teams in Group B

Round 1
[Sep 11]
Palmeiras         2-0  Cruzeiro
  [Mauro, Tato]
[Sep 12]
Botafogo          1-0  Goiás
  [Berg]
[Sep 13]
Corinthians       0-1  Fluminense
  [Assis]
Flamengo          0-2  São Paulo
  [Müller (2)]
Internacional     4-0  Santa Cruz
  [Amarildo (3), Paulo Matos]
Coritiba          0-1  Grêmio
  [Lima]
Bahia             0-3  Vasco da Gama
  [Romário (3)]
Atlético-MG       5-1  Santos
  [Marquinhos, Batista, Chiquinho, Paulo Roberto Prestes, Marquinho Carioca;
  Mendonça]

Round 2
[Sep 18]
Corinthians       0-1  Goiás
  [Fagundes]
[Sep 19]
Atlético-MG       0-0  Internacional
[Sep 20]
Santos            0-0  Palmeiras
Fluminense        1-1  Botafogo
  [Washington; Vágner]
Bahia             1-1  São Paulo
  [Bobô; Zé Teodoro]
Flamengo          2-1  Vasco da Gama
  [Zico, Bebeto; Roberto Dinamite]
Grêmio            0-0  Cruzeiro
Santa Cruz        0-0  Coritiba

Round 3
[Sep 23]
Fluminense        2-0  Palmeiras
  [Marcelo Henrique, Leomir]
São Paulo         3-0  Santa Cruz
  [Müller (3)]
Grêmio            1-0  Vasco da Gama
  [Lima]
Cruzeiro          2-1  Bahia
  [Édson, Cláudio Adão; Hélio]
Coritiba          2-1  Corinthians
  [Lela, Mílton; Éverton]
[Sep 24]
Botafogo          0-0  Internacional
Santos            0-0  Flamengo
[Sep 30]
Goiás             0-1  Atlético-MG
  [Chiquinho]

Round 4
[Sep 26]
Coritiba          2-1  Bahia
  [Carlos Henrique, Tostão; Bobô]
Fluminense        0-0  Grêmio
Palmeiras         2-1  São Paulo
  [Gérson Caçapa, Edu Manga; Pita]
Goiás             1-0  Santa Cruz
  [Formiga]
[Sep 27]
Cruzeiro          1-1  Botafogo
  [Róbson; Mongoal]
Corinthians       0-0  Santos
Internacional     2-0  Flamengo
  [Hêider, Luís Fernando Flores]
Vasco da Gama     1-2  Atlético-MG
  [Roberto Dinamite; Vânder Luís, Paulo Roberto Costa (own goal)]

Round 5
[Oct 1]
Vasco da Gama     1-0  Botafogo
  [Luís Carlos]
[Oct 2]
Internacional     2-0  Palmeiras
  [Luís Fernando Flores, Aloísio]
[Oct 3]
Atlético-MG       2-0  Coritiba
  [Renato, Paulo Roberto Prestes]
Santos            1-0  Grêmio
  [Edelvan]
[Oct 4]
Bahia             1-0  Goiás
  [Zé Carlos]
Flamengo          0-1  Fluminense
  [Washington]
São Paulo         0-0  Corinthians
Santa Cruz        0-0  Cruzeiro

Round 6
[Oct 7]
Bahia             0-2  Internacional
  [Luís Fernando Flores (2)]
Santa Cruz        1-1  Fluminense
  [Dadinho; Jandir]
Palmeiras         1-0  Vasco da Gama
  [Edu Manga]
Botafogo          0-0  Santos
[Oct 8]
São Paulo         0-1  Atlético-MG
  [Sérgio Araújo]
Cruzeiro          1-1  Corinthians
  [Cláudio Adão; Edmar]
Grêmio            4-0  Goiás
  [Cuca (4)]
Flamengo          3-1  Coritiba
  [Kita (2), Wágner (own goal); Marildo]

Round 7
[Oct 10]
Santa Cruz        3-1  Santos
  [Dadinho, Alexandre, Ataíde; Mendonça]
[Oct 11]
Vasco da Gama     4-1  Corinthians
  [Romário (3), Vivinho; Paulo Roberto Costa (own goal)]
Cruzeiro          0-0  Atlético-MG
Goiás             1-1  Flamengo
  [Goiás: Formiga] Flamengo: Zinho]
Palmeiras         1-0  Coritiba
  [Tato]
[Oct 12]
São Paulo         0-2  Botafogo
  [Maurício, Berg]
Internacional     0-1  Grêmio
  [Jorge Veras]
Fluminense        0-1  Bahia
  [Ronaldo Marques]

Round 8
[Oct 16]
Goiás             2-0  Palmeiras
  [Formiga, Tiãozinho]
[Oct 17]
Vasco da Gama     0-0  Santa Cruz
Santos            0-1  Bahia
  [Sandro]
[Oct 18]
Flamengo          0-0  Cruzeiro
Corinthians       1-0  Internacional
  [Éverton]
Coritiba          1-1  Botafogo
  [Luís Fernando Paulista; Tôni]
Grêmio            1-0  São Paulo
  [Valdo]
Atlético-MG       3-1  Fluminense
  [Chiquinho, Renato, Batista; Assis]

Table

Group A
 1-Atlético-MG 	      8  6  2  0  14- 3  14  Qualified for semifinals
 2-Grêmio             8  5  2  1   8- 1  12
 3-Palmeiras          8  4  1  3   6- 7   9
 4-Botafogo	      8  2  5  1   6- 4   9
 5-Bahia              8  3  1  4   6-10   7
 6-Flamengo           8  2  3  3   6- 8   7
 7-Santa Cruz         8  1  4  3   4-10   6
 8-Corinthians        8  1  3  4   4- 9   5

Group B
 1-Internacional      8  4  2  2  10- 2  10  Qualified for semifinals
 2-Fluminense         8  3  3  2   7- 6   9
 3-Cruzeiro           8  1  6  1   4- 5   8
 4-Vasco da Gama      8  3  1  4  10- 7   7
 5-Goiás              8  3  1  4   5- 8   7
 6-São Paulo          8  2  2  4   7- 7   6
 7-Coritiba           8  2  2  4   6-10   6
 8-Santos             8  1  4  3   3- 9   6

Second Stage

Group A

Round 1
[Oct 23]
Grêmio            0-0  Atlético-MG
[Oct 24]
Flamengo          1-0  Botafogo
  [Jorginho]
[Oct 25]
Corinthians       0-0  Palmeiras
Bahia             0-0  Santa Cruz

Round 2
[Oct 28]
Botafogo          0-0  Atlético-MG
Bahia             1-1  Corinthians
  [Édson Mariano; Marcos Roberto]
Santa Cruz        1-2  Palmeiras
  [Rinaldo; Bizu (2)]
[Oct 29]
Flamengo          1-1  Grêmio
  [Andrade; Jorge Veras]

Round 3
[Oct 31]
Corinthians       2-1  Santa Cruz
  [Marcos Roberto, Edmar; Dadinho]
[Nov 1]
Palmeiras         0-1  Bahia
  [Zanata]
Atlético-MG       1-0  Flamengo
  [Renato]
[Nov 2]
Grêmio            0-2  Botafogo
  [Éder, De Lima]

Round 4
[Nov 7]
Flamengo          2-0  Palmeiras
  [Renato Gaúcho, Aílton]
Grêmio            2-0  Bahia
  [Amaral, Cuca]
Atlético-MG       2-0  Santa Cruz
  [Chiquinho, Renato]
Botafogo          1-0  Corinthians
  [Vágner]

Round 5
[Nov 11]
Palmeiras         2-1  Grêmio
  [Henrique (own goal), Lino; Cuca]
Santa Cruz        1-0  Botafogo
  [Dadinho]
Corinthians       1-2  Atlético-MG
  [Edmar; Renato (2)]
Bahia             0-2  Flamengo
  [Zinho, Bebeto]

Round 6
[Nov 14]
Santa Cruz        2-1  Grêmio
  [Dadinho, Cardim; Cuca]
Palmeiras         1-0  Botafogo
  [Bizu]
[Nov 15]
Corinthians       1-1  Flamengo
  [Marcos Roberto; Aílton]
Bahia             1-1  Atlético-MG
  [Bobô; Renato]

Round 7
[Nov 19]
Grêmio            1-0  Corinthians
  [Valdo]
[Nov 21]
Botafogo          2-2  Bahia
  [Botafogo: De Lima, Berg; Bobô, Leandro]
[Nov 22]
Flamengo          3-1  Santa Cruz
  [Zico (3); Cardim]
Atlético-MG       1-0  Palmeiras
  [Marquinhos]

Table
 1-Atlético-MG        7  4  3  0   7- 2  11  *
 2-Flamengo           7  4  2  1  10- 4  10  Qualified for semifinals
 3-Palmeiras          7  3  1  3   5- 6   7
 4-Botafogo           7  2  2  3   5- 5   6
 5-Grêmio             7  2  2  3   6- 7   6
 6-Bahia              7  1  4  2   5- 8   6
 7-Santa Cruz         7  2  1  4   6-10   5
 8-Corinthians        7  1  3  3   5- 7   5
* - Since Atlético-MG had already won the first stage, the second stage runner-up,
Flamengo, qualified for the semifinal.  
For winning both stages, Atlético earned an extra point to the semifinals.

Group B

Round 1
[Oct 24]
São Paulo         3-1  Santos
  [Müller, Silas, Pita; Davi]
Vasco da Gama     0-2  Fluminense
  [Romerito (2)]
Goiás             1-1  Coritiba
  [Gomes; Mauro Madureira]
Cruzeiro          3-0  Internacional
  [Cláudio Adão (2), Heriberto]

Round 2
[Oct 28]
Cruzeiro          3-0  Vasco da Gama
  [Cláudio Adão, Careca, Morôni (own goal)]
Internacional     0-1  Fluminense
  [Washington]
São Paulo         2-0  Goiás
  [Silas, Raí]
[Oct 29]
Santos            2-1  Coritiba
  [Chicão, Osmarzinho; Mílton]

Round 3
[Oct 31]
Coritiba          3-2  São Paulo
  [Édson Borges, Tostão, Luís Fernando Paulista; Edivaldo, Silas]
Fluminense        1-1  Cruzeiro
  [Romerito; Cláudio Adão]
[Nov 1]
Vasco da Gama     1-0  Internacional
  [Aírton (own goal)]
Goiás             0-0  Santos

Round 4
[Nov 6]
Santos            0-0  Vasco da Gama
[Nov 7]
São Paulo         2-0  Fluminense
  [Dario Pereyra, Lê]
Coritiba          0-3  Cruzeiro
  [Heriberto, Eduardo, Cláudio Adão]
Internacional     0-0  Goiás

Round 5
Fluminense        1-0  Goiás
  [Ricardo Gomes]
Internacional     2-0  Santos
  [Amarildo (2)]
Cruzeiro          0-0  São Paulo
Vasco da Gama     3-2  Coritiba
  [Roberto Dinamite (2), Romário; Donato (own goal), Tostão]

Round 6
[Nov 14]
Fluminense        1-1  Santos
  [Washington; Osmarzinho]
[Nov 15]
Vasco da Gama     1-2  São Paulo
  [Roberto Dinamite; Müller (2)]
Internacional     0-0  Coritiba
Cruzeiro          1-0  Goiás
  [Heriberto]

Round 7
[Nov 21]
São Paulo         3-0  Internacional
  [Müller (2), Silas]
Coritiba          2-1  Fluminense
  [Luís Fernando Paulista, Édson Borges; Leomir]
[Nov 22]
Goiás             2-2  Vasco da Gama
  [Formiga (2); Humberto, Roberto Dinamite]
Santos            0-1  Cruzeiro
  [Careca]

Table
 1-Cruzeiro           7  5  2  0  12- 1  12  Qualified for semifinals
 2-São Paulo          7  5  1  1  14- 5  11
 3-Fluminense         7  3  2  2   7- 6   8
 4-Coritiba           7  2  2  3   9-12   6
 5-Vasco da Gama      7  2  2  3   7-11   6
 6-Santos             7  1  3  3   4- 8   5
 7-Internacional      7  1  2  4   2- 8   4
 8-Goiás              7  0  4  3   3- 7   4

Semifinals

First Leg

[Nov 29 and Dec 2]
Flamengo          1-0   3-2  Atlético-MG
  [Bebeto]
  [Zico, Bebeto, Renato Gaúcho; Chiquinho, Sérgio Araújo]
Internacional     0-0   0-0  Cruzeiro          [aet 1-0]
  [Amarildo]

Final

[Dec 6 and 13]
Internacional     1-1   0-1  Flamengo
  [Amarildo; Bebeto]
  [Bebeto]

13/dezembro/1987 
FLAMENGO 1X0 INTERNACIONAL 
Local: Maracanã (Rio de Janeiro); 
Juiz: José de Assis Aragão (SP); 
Público Presente: 91.034 espectadores; 
Gol: Bebeto 16 do 1º tempo; 
Cartões Amarelos: Aloísio e Edinho. 
FLAMENGO: Zé Carlos, Jorginho, Leandro, Edinho e Leonardo; Andrade, Aílton e Zico (Flávio);
Renato Gaúcho, Bebeto e Zinho.  
Técnico: Carlinhos. 
INTERNACIONAL: Taffarel, Luiz Carlos Winck, Aloísio, Nenê e Paulo Roberto (Bebeto); Norberto,
Luís Fernando e Balalo; Hêider (Manú), Amarildo e Brites.
Técnico: Ênio Andrade.

CR Flamengo are the 1987 Copa União Champions


Final Table
 1-Flamengo          19  9  6  4  22-15  24  [1]
 2-Internacional     19  6  6  7  14-12  18  [1]
 3-Atlético-MG       17 10  5  2  23- 9  25  [1]
 4-Cruzeiro          17  6  9  2  16- 7  21  [1]
 5-Grêmio            15  7  4  4  14- 8  18  [1]
 6-São Paulo         15  7  3  5  21-12  17  [1]
 7-Fluminense        15  6  5  4  14-12  17  [1]
 8-Palmeiras         15  7  2  6  11-13  16  [1]
 9-Botafogo          15  4  7  4  11- 9  15
10-Vasco da Gama     15  5  3  7  17-18  13  [1]
11-Bahia             15  4  5  6  11-18  13  [1]
12-Coritiba          15  4  4  7  15-22  12
13-Goiás             15  3  5  7   8-15  11  [1]
14-Santa Cruz        15  3  5  7  10-20  11  [1]
15-Santos            15  2  7  6   7-17  11  [1]
16-Corinthians       15  2  6  7   9-16  10  [1]

[1] Teams which would play in First Level according to the original rule of
1986 Brazilian Championship.

According to [JB] (09/09/87, 2nd edition), [OG] (09/09/87), [JT] (09/09/87),
[DP] (10/09/87) and [OESP] (13/09/87)
sources, the original rule of 1987 Brazilian Championship stated that:
- The 12 best placed teams would be qualified to 1988 First Level
- The 13th and 14th placed teams would play a qualifying tournament (for two
  berths in 1988 First Level) against the 7th and 8th of Yellow Module
- The 15th and 16th placed teams would play the 1988 Second Level

These rules, however, were not applied, since the composition of 1988 First
and Second Levels were defined under other criteria.


Yellow Module (Taça Roberto Gomes Pedrosa)

Participants

Centro Sportivo Alagoano - CSA (Maceió-AL)
Esporte Clube VITÓRIA (Salvador-BA)
CEARÁ Sporting Club (Fortaleza-CE)
RIO BRANCO Atlético Clube (Cariacica-ES)
ATLÉTICO Club Goianiense (Goiânia-GO)
TREZE Futebol Clube (Campina Grande-PB)
Clube NÁUTICO Capibaribe (Recife-PE)
SPORT Club do Recife (Recife-PE)
Clube ATLÉTICO Paranaense (Curitiba-PR)
BANGU Atlético Clube (Rio de Janeiro-RJ)
CRICIÚMA Esporte Clube (Criciúma-SC)
JOINVILLE Esporte Clube (Joinville-SC)
GUARANI Futebol Clube (Campinas-SP)
Associação Atlética INTERNACIONAL (Limeira-SP)
Associação PORTUGUESA de Desportos (São Paulo-SP)

First Phase

1st Stage

[Sep 13]
Bangu             1-1  Joinville
Criciúma          1-2  Ceará
Treze             0-0  Atlético-PR
CSA               0-1  Guarani

[Sep 16]
Vitória           3-1  Joinville
Internacional     1-0  Ceará
Sport             1-1  Atlético-PR
Treze             1-3  Guarani

[Sep 17]
Criciúma          2-0  Náutico

[Sep 19]
Rio Branco        0-1  CSA
Vitória           1-2  Atlético-PR

[Sep 20]
Internacional     2-1  Treze
Atlético-GO       1-0  Ceará
Sport             2-0  Guarani
Criciúma          1-0  Bangu
Joinville         2-1  Náutico

[Sep 23]
Atlético-PR       1-2  Bangu
Joinville         0-0  Treze
Atlético-GO       3-1  CSA
Sport             3-0  Criciúma

[Sep 24]
Náutico           0-1  Rio Branco

[Sep 27]
Ceará             1-1  Rio Branco
Náutico           2-1  Atlético-GO
Bangu             1-0  Internacional
Guarani           0-1  Vitória
Joinville         0-1  Sport
Treze             2-1  Criciúma
Atlético-PR       1-1  CSA

[Sep 30]
Portuguesa        1-1  Sport
Internacional     0-0  Vitória
Bangu             0-0  Guarani
CSA               1-2  Criciúma
Treze             3-1  Atlético-GO

[Oct 1]
Ceará             1-0  Joinville

[Oct 3]
Internacional     0-1  Náutico

[Oct 4]
CSA               3-2  Joinville
Criciúma          2-1  Vitória
Atlético-GO       0-0  Sport
Bangu             1-0  Rio Branco
Ceará             1-1  Portuguesa
Atlético-PR       0-WO América-RJ       [awarded 1-0]

[Oct 6]
Joinville         0-WO América-RJ       [awarded 1-0]

[Oct 7]
CSA               0-2  Internacional
Rio Branco        0-1  Sport

[Oct 8]
Náutico           2-1  Portuguesa
Guarani           0-WO América-RJ       [awarded 1-0]

[Oct 10]
Atlético-GO       1-0  Bangu

[Oct 11]
Rio Branco        2-1  Treze
Sport             4-0  Internacional
Guarani           4-2  Náutico
Vitória           2-1  Portuguesa
Ceará             0-1  Atlético-PR
América-RJ       WO-0  Criciúma         [awarded 0-1]

[Oct 13]
Portuguesa        1-0  Treze
Internacional     0-WO América-RJ       [awarded 1-0]
[Oct 14]
Atlético-PR       2-0  Náutico
Rio Branco        0-0  Vitória

[Oct 15]
Portuguesa        1-0  Bangu
América-RJ       WO-0  Atlético-GO      [awarded 0-1]

[Oct 18]
Portuguesa        4-0  CSA
Guarani           1-0  Ceará
Vitória           0-0  Atlético-GO
América-RJ       WO-0  Rio Branco       [awarded 0-1]

[Oct 20]
América-RJ       WO-0  Portuguesa       [awarded 0-1]


Tie-Braking match for first place in Group A

[Oct 21]
Guarani           0-2  Atlético-PR
  [Pedrinho Maradona 46' e Carlinhos 48']
                    
Tables

Group A
 1-Atlético-PR        7  3  3  1   8- 5   9  Qualified for the semifinals
 2-Guarani            7  4  1  2   9- 6   9
 3-Criciúma           7  4  0  3   9- 9   8
 4-Portuguesa         7  3  2  2  10- 6   8
 5-Atlético-GO        7  3  2  2   7- 6   8
 6-Internacional-SP   7  3  1  3   5- 7   7
 7-Rio Branco-ES      7  2  2  3   4- 5   6
 8-Joinville          7  1  2  4   6-10   5
                    
Group B
 1-Sport              8  5  3  0  13- 2  13  Qualified for the semifinals
 2-Vitória            8  3  3  2   8- 6   9
 3-Bangu              8  3  2  3   5- 5   8
 4-Náutico            8  3  0  5   8-13   6
 5-Treze              8  2  2  4   8-10   6
 6-Ceará              8  2  2  4   5- 7   6
 7-CSA                8  2  1  5   7-15   5

N.B.: América-RJ was invited by CBF to join Group B.  But the team protested 
for being relegated to the Yellow Module and withdrew from the competition.                    

2nd Stage

Group A

[Oct 21]
Rio Branco        0-0  Atlético-GO

[Oct 24]
Atlético-GO       0-2  Criciúma

[Oct 25]
Rio Branco        0-0  Internacional
Guarani           2-0  Portuguesa
Joinville         1-2  Atlético-PR

[Oct 28]
Atlético-PR       0-1  Portuguesa
Criciúma          3-0  Rio Branco
Internacional     1-0  Atlético-GO
Joinville         0-2  Guarani

[Nov 1]
Joinville         0-0  Rio Branco
Guarani           2-0  Criciúma
Portuguesa        1-0  Atlético-GO
Internacional     1-1  Atlético-PR

[Nov 4]
Criciúma          2-0  Joinville
Atlético-PR       3-0  Atlético-GO

[Nov 8]
Internacional     0-0  Joinville
Atlético-GO       1-0  Guarani
Atlético-PR       1-1  Rio Branco
Portuguesa        0-0  Criciúma

[Nov 11]
Rio Branco        2-3  Guarani
Atlético-GO       0-0  Joinville
Portuguesa        1-0  Internacional

[Nov 15]
Guarani           0-0  Atlético-PR
Criciúma          0-0  Internacional
Joinville         1-0  Portuguesa

[Nov 18]
Guarani           0-0  Internacional
Criciúma          1-1  Atlético-PR
Portuguesa        0-1  Rio Branco

Final Table

Group A
1-Guarani             7  4  2  1   9- 3  10  Qualified for the semifinals
2-Criciúma            7  3  3  1   8- 3   9
3-Atlético-PR         7  2  4  1   8- 5   8
4-Portuguesa          7  3  1  3   3- 4   7
5-Internacional       7  1  5  1   2- 2   7
6-Rio Branco          7  2  2  3   4- 7   6
7-Joinville           7  1  3  3   2- 6   5
8-Atlético-GO         7  1  2  4   1- 7   4

Group B

[Oct 21]
Bangu             2-0  Ceará
Vitória           0-0  CSA

[Oct 25]
CSA               1-1  Náutico
Sport             2-1  Ceará

[Oct 28]
Bangu             2-0  Sport
Ceará             0-2  Treze

[Nov 1]
Treze             1-1  Vitória
CSA               0-0  Bangu
Náutico           0-1  Sport

[Nov 4]
Náutico           2-2  Vitória
Treze             0-0  Bangu

[Nov 8]
Sport             0-0  Vitória
Ceará             1-0  Náutico
Treze             2-1  CSA

[Nov 11]
CSA               0-1  Sport

[Nov 14]
Vitória           1-0  Ceará

[Nov 15]
Sport             2-1  Treze
Bangu             3-0  Náutico

[Nov 18]
Ceará             2-0  CSA
Vitória           3-1  Bangu
Náutico           2-1  Treze

Tie-Braking match for second place in Group B

[Nov 22]
Bangu             1-1  Vitória  [aet 0-0, pen 4-3]
  [Marinho; Júnior]

Group B
 1-Sport              6  4  1  1   6- 4   9  *
 2-Bangu              6  3  2  1   8- 3   8  Qualified for the semifinals
 3-Vitória            6  2  4  0   7- 4   8
 4-Treze              6  2  2  2   7- 6   6
 5-Náutico            6  1  2  3   5- 9   4
 6-Ceará              6  2  0  4   4- 7   4
 7-CSA                6  0  3  3   2- 6   3

* - Since Sport had already won the first stage, the second stage runner-up,
Bangu, qualified for the semifinal.  For winning both stages, Sport earned an
extra point in the semifinals.

Semifinals

[Nov 28 and Dec 2]
Atlético-PR       0-0   0-0  Guarani [aet 0-1]
  [Boiadeiro (aet) 8']

[Nov 29 and Dec 3]
Bangu             3-2   1-3  Sport        
  [Marinho, Paulinho Criciúma e Edevaldo; Betão e Augusto]
  [Marinho; Zico, Betão e Nando]

Finals

[Dec 6 and 13]
Guarani           2-0   0-3  Sport [aet 0-0, pen 11-11]
  [Evair (2) 11' e 27']
  [Nando (2) 19' e 67', Macaé 61']

Both team's managements decided to end the penalties shootouts and
share the Yellow Module title.
In 22/01/1988, Guarani withdrew from this sharement and CBF declared
Sport Recife as champions of Yellow Module. [DP and JC (23/01/88)]

Sport Recife was the 1987 Yellow Module Champions

final table (doesn't include the tie-breaking matches)                    
 1-Sport             18 11  4  3  27-12  26
 2-Guarani           18 10  4  4  22-13  24  [1]
 3-Bangu             16  7  4  5  17-13  18  [1]
 4-Atlético-PR       16  5  8  3  15-10  18  [1]
 5-Criciúma          14  7  3  4  17-12  17  [1]
 6-Vitória           14  5  7  2  15-10  17
 7-Portuguesa        14  6  3  5  13-10  15  [1]
 8-Internacional-SP  14  4  6  4   7- 9  14  [1]
 9-Treze             14  4  4  6  15-16  12  [1]
10-Rio Branco-ES     14  4  4  6   8-12  12  [1]
11-Atlético-GO       14  4  4  6   8-13  12  [1]
12-Ceará             14  4  2  8   9-14  10  [1]
13-Náutico           14  4  2  8  13-22  10  [1]
14-Joinville         14  2  5  7   8-16   9  [1]
15-CSA               14  2  4  8   9-21   8  [1]
16-América-RJ         0  0  0  0   0- 0   0  [1]

[1] Teams which would play in First Level according to the original rule of
1986 Brazilian Championship.

According to [JB] (09/09/87, 2nd edition), [OG] (09/09/87), [DP] (10/09/87)
and [OESP] (13/09/87)
sources, the original rule of 1987 Brazilian Championship stated that:
- The 6 best placed teams would be qualified to 1988 First Level
- The 7th and 8th placed teams would play a qualifying tournament (for two
  berths in 1988 First Level) against the 13th and 14th of Green Module
- The 9th to 16th placed teams would play the 1988 Second Level

These rules, however, were not applied, since the composition of 1988 First
and Second Levels were defined under other criteria.

Sport, Guarani, Bangu, Atlético-PR, Criciúma, Vitória and Portuguesa were
eventually invited to join the 16 clubs from Green Module in the 1988 First
Level. Although América-RJ did not dispute the Yellow Module, they were also 
invited to the 1988 1st level.

Final Phase

NB: Sport Recife and Guarani entered the playoff with the Green Module
(Copa União) top-2  ordered by CBF, but Flamengo and International-RS
did not enter.  Sport Recife and Guarani then played two games.

24/Jan/1988   Guarani           W.O.  Flamengo        [awarded 1-0]
24/Jan/1988   Sport             W.O.  Internacional   [awarded 1-0]

27/Jan/1988   Guarani           W.O.  Internacional   [awarded 1-0]
27/Jan/1988   Sport             W.O.  Flamengo        [awarded 1-0]

30/Jan/1988   Guarani           1-1  Sport

07/Feb/1988   Sport             1-0  Guarani

30/janeiro/1988
GUARANI 1X1 SPORT
Local: Brinco de Ouro(Campinas)
Juiz: Carlos Elias Pimentel (RJ)
Gols: Betão (pênalti) aos 7 min do 2º tempo e Catatau (pen) aos 17 min do 2º tempo.
Público: 4.627 pagantes
GUARANI: Sérgio Neri, Giba, Luciano, Ricardo Rocha e Albéris (Gil Baiano); 
Paulo Isidoro, Nei (Carlinhos) e Boiadeiro; Catatau, Mário Maguila e João Paulo. 
Técnico: José Luís Carbone.
SPORT: Flávio, Betão, Estevam, Marco Antonio e Zé Carlos Macaé; 
Rogério, Zico e Ribamar (Disco); 
Robertinho, Nando (Augusto) e Neco. 
Técnico: Jair Picerni.

07/fevereiro/1988 
SPORT 1X0 GUARANI 
Local: Ilha do Retiro (Recife); 
Juiz: Luís Carlos Félix (RJ); 
Público: 26.282 espectadores; 
Gol: Marco Antônio 19 do 2º tempo; 
Cartões Amarelos: Paulo Isidoro, Catatau e Ricardo Rocha;
Expulsão: Evair 45 do 1º tempo. 
SPORT: Flávio, Betão, Estevam, Marco Antônio e Zé Carlos Macaé; Rogério, Ribamar (Augusto) e 
Zico; Robertinho, Nando e Neco.
Técnico: Jair Picerni. 
GUARANI: Sérgio Néri, Gil Baiano, Luciano, Ricardo Rocha e Albéris; Paulo Isidoro, Nei 
(Carlinhos) e Marco Antônio Boiadeiro; Catatau (Mário), Evair e João Paulo.
Técnico: Carbone.

Sport Recife were declared the 1987 Brazilian champions by CBF
Sport and Guarani qualified to Copa Libertadores 1988
                    

Brazilian Championship 1987 - White Module (Taça Rubens Moreira)

1st Phase
(from 10/10 to 11/11)

Group A

Participants
Mixto EC (Cuiabá-MT)
Operário FC (Campo Grande-MS)
CE Operário Varzeagrandense (Várzea Grande-MT)
Sobradinho EC (Brasília-DF)

Mixto             2-1  Operário-MS
Operário-MT       2-0  Sobradinho

Mixto             1-1  Operário-MT
Operário-MS       4-0  Sobradinho

Mixto             0-0  Sobradinho
Operário-MS       1-0  Operário-MT

Sobradinho        0-1  Mixto
Operário-MT       1-2  Operário-MS

Operário-MT       0-0  Mixto
Sobradinho        0-1  Operário-MS

Operário-MS       0-1  Mixto
Sobradinho        n/p  Operário-MT

Table
 1.Mixto              6  3  3  0   5- 2   9  Qualified
 2.Operário-MS        6  4  0  2   9- 4   8  Qualified
-------------------------------------------
 3.Operário-MT        5  1  2  2   4- 4   4
 4.Sobradinho         5  0  1  4   0- 8   1

Group B

Participants
Auto Esporte Clube (João Pessoa-PB)
AE Catuense (Alagoinhas-BA)
Central SC (Caruaru-PE)
CRB (Maceió-AL)

Auto Esporte      0-3  Catuense
Central           0-1  CRB

Auto Esporte      0-0  CRB
Catuense          2-0  Central

Auto Esporte      1-0  Central
Catuense          2-0  CRB

Central           2-4  Auto Esporte
CRB               1-3  Catuense

Central           0-1  Catuense
CRB               2-1  Auto Esporte

CRB               2-4  Central
Catuense          0-2  Auto Esporte

Table
 1.Catuense           6  5  0  1  11- 3  10  Qualified
 2.Auto Esporte-PB    6  3  1  2   8- 7   7  Qualified
-------------------------------------------
 3.CRB                6  2  1  3   6-10   5
 4.Central            6  1  0  5   6-11   2

Group C

Participants
ABC FC (Natal-RN)
América FC (Natal-RN)
Botafogo FC (João Pessoa-PB)
Fortaleza EC (Fortaleza-CE)

ABC               2-4  América
Botafogo          2-1  Fortaleza

ABC               1-2  Botafogo
América           1-1  Fortaleza

ABC               1-2  Fortaleza
América           3-1  Botafogo

Botafogo          1-0  América
Fortaleza         0-1  ABC

Fortaleza         0-0  América
Botafogo          2-2  ABC

América           0-0  ABC
Fortaleza         2-0  Botafogo

Table
 1.Botafogo-PB        6  3  1  2   8- 9   7  Qualified
 2.América-RN         6  2  3  1   8- 5   7  Qualified
-------------------------------------------
 3.Fortaleza          6  2  2  2   6- 5   6
 4.ABC                6  1  2  3   7-10   4

Group D

Participants
Ferroviário AC (Fortaleza-CE)
EC Flamengo (Teresina-PI) (*)
Maranhão AC (São Luís-MA)
Sampaio Corrêa FC (São Luís)

(*) Flamengo withdrew and was replaced by Serrano SC (Vitória da Conquista-BA)

Ferroviário       1-0  Serrano
Maranhão          0-1  Sampaio Corrêa

Ferroviário       2-0  Maranhão
Sampaio Corrêa    0-1  Serrano

Ferroviário       3-1  Sampaio Corrêa
Maranhão          2-1  Serrano

Serrano           1-0  Maranhão
Sampaio Corrêa    1-0  Ferroviário

Serrano           0-0  Sampaio Corrêa
Maranhão          3-1  Ferroviário

Sampaio Corrêa    1-1  Maranhão
Serrano           0-0  Ferroviário

Table
 1.Ferroviário        6  3  1  2   7- 5   7  Qualified
 2.Serrano-BA         6  2  2  2   3- 3   6  Qualified
-------------------------------------------
 3.Sampaio Corrêa     6  2  2  2   3- 4   6
 4.Maranhão           6  2  1  3   6- 7   5

Group E

Participants
SA Imperatriz (Imperatriz-MA)
Moto Clube (São Luís-MA)
Piauí EC (Teresina-PI)
Ríver AC (Teresina-PI)

Imperatriz        1-1  Piauí
Moto Clube        3-1  Ríver

Imperatriz        0-0  Ríver
Moto Clube        0-0  Piauí

Imperatriz        0-2  Moto Clube
Piauí             2-0  Ríver

Ríver             1-0  Piauí
Moto Clube        2-0  Imperatriz

Piauí             0-0  Moto Clube
Ríver             1-2  Imperatriz

Piauí             1-0  Imperatriz
Ríver             1-3  Moto Clube

Table
 1.Moto Clube         6  4  2  0  10- 2  10  Qualified
 2.Piauí              6  2  3  1   4- 2   7  Qualified
-------------------------------------------
 3.Imperatriz         6  1  2  3   3- 7   6
 4.Ríver              6  1  1  4   4-10   3

Group F

Participants
Nacional FC (Manaus-AM)
Paysandu SC (Belém-PA)
Atlético Rio Negro Clube (Manaus-AM)
Tuna Luso Brasileira (Belém-PA)

Nacional          2-1  Rio Negro
Paysandu          0-1  Tuna Luso

Nacional          1-2  Paysandu
Rio Negro         0-1  Tuna Luso

Nacional          1-1  Tuna Luso
Paysandu          3-1  Rio Negro

Rio Negro         1-1  Paysandu
Tuna Luso         0-2  Nacional

Tuna Luso         1-0  Rio Negro
Paysandu          2-0  Nacional

Tuna Luso         2-3  Paysandu
Rio Negro         3-0  Nacional

Table
 1.Paysandu           6  4  1  1  11- 6   9  Qualified
 2.Tuna Luso          6  3  1  2   6- 6   7  Qualified
-------------------------------------------
 3.Nacional           6  2  1  3   6- 9   5
 4.Rio Negro          6  1  1  4   6- 8   3

2nd Phase

[Nov 18-19 and 21-22]
Auto Esporte-PB   0-1   0-3  Mixto
Operário-MS       2-0   2-2  Catuense
Sampaio Corrêa    1-1   0-0  Botafogo-PB   [aet 0-0, pen 2-3]
América-RN        1-0   2-0  Ferroviário
Tuna Luso         2-0   0-2  Moto Clube    [aet 3-0]
Piauí             1-1   0-2  Paysandu

3rd Phase

[Nov 25-26 and 28-29]
Tuna Luso         2-2   0-1  Paysandu
Operário-MS       2-0   2-2  Mixto
América-RN        1-0   0-2  Botafogo-PB

Final Phase

[Dec 9]
Paysandu          2-0  Botafogo
[Jan 24/88]
Botafogo          0-0  Operário-MS
[Jan 30/88]
Operário-MS       2-1  Paysandu

Table
 1.Operário-MS        2  1  1  0   2- 1   3  champions
-------------------------------------------
 2.Paysandu           2  1  0  1   3- 2   2
 3.Botafogo-PB        2  0  1  1   0- 2   1

According to [JB] (09/09/87, 2nd edition), [JT] (09/09/87), [DP] (10/09/87)
and [OESP] (13/09/87) sources, the original rule of 1987 Brazilian Championship
stated that the 06 best teams of White and the 06 best teams of Blue Modules
would be qualified to 1988 Second Level.

These rules, however, were not applied, since the composition of 1988 First
and Second Levels were defined under other criteria.


Brazilian Championship 1987 - Blue Module (Taça Heleno Nunes)

Minas Gerais State Qualifying Tournament

1st Phase
(from 10/10 to 11/11)

Group A

Participants
Associação Chapecoense de Futebol (Chapecó-SC)
Clube Esportivo BG (Bento Gonçalves-RS)
EC Pinheiros (Curitiba-PR)
FC Santa Cruz (Santa Cruz do Sul-RS)

Esportivo         0-0  Santa Cruz
[Oct 11]
Chapecoense       0-0  Pinheiros

Esportivo         1-1  Chapecoense
[Oct 20]
Santa Cruz        1-0  Pinheiros

Chapecoense       2-2  Santa Cruz
[Oct 25]
Pinheiros         4-1  Esportivo

Santa Cruz        1-0  Esportivo
[Nov 01]
Pinheiros         0-1  Chapecoense

Chapecoense       2-1  Esportivo
[Nov 07]
Pinheiros         1-1  Santa Cruz

Santa Cruz        0-0  Chapecoense
Esportivo         n/p  Pinheiros

Table
 1.Chapecoense        6  2  4  0   6- 4   8  Qualified
 2.Santa Cruz-RS      6  2  4  0   5- 3   8  Qualified
-------------------------------------------
 3.Pinheiros          5  1  2  2   5- 4   4
 4.Esportivo-RS       5  0  2  3   3- 8   2

Group B

Participants
Avaí FC (Florianópolis-SC)
SER Caxias (Caxias do Sul-RS)
EC Juventude (Caxias do Sul-RS)
Londrina EC (Londrina-PR)

Caxias            1-1  Juventude
[Oct 10]
Avaí              2-1  Londrina

Juventude         0-0  Avaí
[Oct 18]
Caxias            2-1  Londrina

Caxias            1-0  Avaí
[Oct 25]
Londrina          1-0  Juventude

Juventude         1-0  Caxias
[Nov 01]
Londrina          0-0  Avaí

Avaí              1-1  Juventude
[Nov 07]
Londrina          0-2  Caxias            

Avaí              1-0  Caxias
[Nov 12]
Juventude         3-1  Londrina

Table
 1.Caxias             6  3  1  2   6- 4   7  Qualified
 2.Juventude          6  2  3  1   6- 4   7  Qualified
-------------------------------------------
 3.Avaí               6  2  3  1   4- 3   7
 4.Londrina           6  1  1  4   4- 9   3

Group C

Participants
Americano FC (Campos-RJ)
Associação Desportiva FVRD (Vitória-ES)
Estrela do Norte FC (Cachoeiro do Itapemirim-ES)
CA Juventus (São Paulo-SP)

Americano         0-0  Juventus
Desportiva        3-0  Estrela do Norte

Estrela do Norte  1-0  Americano
Desportiva        1-1  Juventus

Americano         1-1  Desportiva
Estrela do Norte  0-1  Juventus

Juventus          0-0  Americano
Estrela do Norte  1-0  Desportiva

Americano         1-0  Estrela do Norte
Juventus          0-0  Desportiva

Desportiva        0-1  Americano
Juventus          4-0  Estrela do Norte

Table          
 1.Juventus           6  2  4  0   6- 1   8  Qualified
 2.Americano          6  2  3  1   3- 2   7  Qualified
-------------------------------------------
 3.Desportiva         6  1  3  2   5- 4   5
 4.Estrela do Norte   6  2  0  4   2- 9   4

Group D

Participants
América FC (Belo Horizonte-MG)
Botafogo FC (Ribeirão Preto-SP)
Goytacaz FC (Campos-RJ)
Tupi FC (Juiz de Fora-MG)

América           1-0  Goytacaz
Tupi              4-0  Botafogo

América           2-1  Tupi
Goytacaz          2-1  Botafogo

Botafogo          2-0  América
Goytacaz          0-1  Tupi

Goytacaz          2-1  América
Botafogo          1-0  Tupi

Botafogo          2-1  Goytacaz
Tupi              1-0  América

América           0-0  Botafogo
Tupi              2-0  Goytacaz

Table
 1.Tupi               6  4  0  2   9- 3   8  Qualified
 2.Botafogo-SP        6  3  1  2   6- 7   7  Qualified
-------------------------------------------
 3.América-MG         6  2  1  3   4- 6   5
 4.Goytacaz           6  2  0  4   5- 8   4

Group E

Participants
Itumbiara EC (Itumbiara-GO)
EC Santo André (Santo André-SP)
Uberaba SC (Uberaba-MG)
Uberlândia EC (Uberlândia-MG)

Itumbiara         0-1  Santo André
Uberaba           0-1  Uberlândia

Uberlândia        2-0  Itumbiara
Uberaba           1-0  Santo André

Itumbiara         0-1  Uberaba
Santo André       0-2  Uberlândia

Santo André       0-0  Itumbiara
Uberlândia        0-0  Uberaba

Itumbiara         0-0  Uberlândia
Santo André       0-0  Uberaba

Uberaba           0-0  Itumbiara
Uberlândia        0-1  Santo André

Table
 1.Uberlândia         6  3  2  1   5- 1   8  Qualified
 2.Uberaba            6  2  3  1   2- 1   7  Qualified
-------------------------------------------
 3.Santo André        6  2  2  2   2- 3   6
 4.Itumbiara          6  0  3  3   0- 4   3

Group F

Participants
AA Anapolina (Anápolis-GO)
Brasília EC (Brasília-DF)
Corumbaense FC (Corumbá-MS)
AA Ponte Preta (Campinas-SP)

Anapolina         2-0  Corumbaense 
Brasília          1-3  Ponte Preta 

Anapolina         0-0  Ponte Preta
Brasília          3-2  Corumbaense

Brasília          1-1  Anapolina
Corumbaense       2-2  Ponte Preta

Corumbaense       2-0  Anapolina
Ponte Preta       2-0  Brasília

Ponte Preta       2-0  Anapolina
Corumbaense       2-0  Brasília

Anapolina         0-0  Brasília
Ponte Preta       3-0  Corumbaense

Table
 1.Ponte Preta        6  4  2  0  12- 3  10  Qualified
 2.Corumbaense        6  2  1  3   8-10   5  Qualified
-------------------------------------------
 3.Anapolina          6  1  3  2   3- 5   5
 4.Brasília           6  1  2  3   5-10   4

2nd Phase

[Nov 18 and 21]
Juventude         2-1   1-1  Chapecoense
Santa Cruz-RS     1-1   0-1  Caxias
Botafogo-SP       1-0   0-1  Juventus      [aet 0-0, pen 5-4]
Americano         1-0   1-0  Tupi
Corumbaense       1-0   1-2  Uberlândia    [aet 0-3]
Uberaba           2-0   0-3  Ponte Preta

3rd Phase

[Nov 25 and 28-29]
Uberlândia        5-0   0-3  Ponte Preta
Americano         3-1   0-1  Botafogo-SP
Juventude         1-0   1-1  Caxias

Final Phase

[Dec 5]
Juventude         0-0  Americano

[Dec 9]
Americano         2-0  Uberlândia

[Dec 24]
Uberlândia        2-0  Juventude
    """.split("\n")   

# Initialize a list to hold the results
results = []

# Regular expression for capturing teams and scores, including accents
match_pattern = re.compile(
    # r"([A-Za-zÀ-ÿ\s/-]+)\s+(\d+)-(\d+)\s+([A-Za-zÀ-ÿ\s/-]+)", re.UNICODE
    r"([A-Za-zÀ-ÿ\s/-]+)\s+(\d+)-(\d+)\s+([A-Za-zÀ-ÿ\s/-]+)\s*(\[(\w{3} \d{1,2})\])*", re.UNICODE
)

match_pattern_2 = re.compile(
    r"([A-Za-zÀ-ÿ\s/-]+)\s+(\d+)-(\d+)\s+(\d+)-(\d+)\s+([A-Za-zÀ-ÿ\s/-]+)\s*(\[(\w{3} \d{1,2})\])*", re.UNICODE
)

# Process each line
for line in lines:
    # line = line.strip()

    match_2 = match_pattern_2.match(line)
    match = match_pattern.match(line)

    if match_2:
        home_team = match_2.group(1).strip()
        home_score = match_2.group(2)
        away_score = match_2.group(3)
        home_score2 = match_2.group(4)
        away_score2 = match_2.group(5)
        away_team = match_2.group(6).strip()
        
        date = match_2.group(7)
        if date:
          results.append([convert_date(date, year), home_team, home_score, away_score, away_team, False, False, "first"])
          results.append([convert_date(date, year), away_team, away_score2, home_score2, home_team, False, False, "first"])
          continue

        # Store the extracted data in results
        results.append([convert_date(current_date, year), home_team, home_score, away_score, away_team, False, False, "first"])
        results.append([convert_date(current_date, year), away_team, away_score2, home_score2, home_team, False, False, "first"])

    elif match:
        home_team = match.group(1).strip()
        home_score = match.group(2)
        away_score = match.group(3)
        away_team = match.group(4).strip()
        
        date = match.group(6)
        if date:
          results.append([convert_date(date, year), home_team, home_score, away_score, away_team, False, False, "first"])
          continue

        # Store the extracted data in results
        results.append([convert_date(current_date, year), home_team, home_score, away_score, away_team, False, False, "first"])
        
    # Check if the line contains a date
    date_match = re.search(r"\[(\w{3} \d{1,2})\]", line)
    if date_match:
        current_date = date_match.group(1)

print("Matches:", len(results))
assert len(results) == 239

dataframe = pd.DataFrame(results, columns=["date", "home_team", "home_score", "away_score", "away_team", "neutral", "knockout", "stage"])
dataframe.to_csv(FOLDER + str(year) + ".csv")
