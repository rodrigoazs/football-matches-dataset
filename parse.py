import re

import requests

import pandas as pd
from datetime import datetime

FOLDER = "data/br/serie_a/"


def convert_date(date_string, year):
    try:
      date_format = "%b %d"
      date_object = datetime.strptime(date_string, date_format).replace(year=year)
      return date_object.strftime("%Y-%m-%d")
    except:
      raise Exception(date_string)


year = 2000

print(f"Parsing {year}")


lines = """
[Jul 29]
Vitória            4-1  Palmeiras
Vasco da Gama      0-2  Sport
Fluminense         2-0  Bahia
[Jul 30]
Goiás              3-0  Corinthians
Juventude          1-1  Flamengo
Guarani            0-0  Santa Cruz
Botafogo-RJ        0-0  Atlético-MG
América-MG         0-1  Gama
Cruzeiro           0-2  Atlético-PR

[Aug 2]
Flamengo           3-0  Grêmio
Gama               2-1  Fluminense
Santos             2-0  Vitória
Ponte Preta        3-1  América-MG
Internacional      0-1  Goiás
Bahia              2-1  Atlético-PR
Coritiba           0-0  Sport
[Aug 3]
Palmeiras          0-0  Botafogo-RJ

[Aug 5]
Fluminense         2-1  Santos
Atlético-PR        1-1  Flamengo
Corinthians        4-2  Gama
[Aug 6]
Grêmio             0-1  Palmeiras
Coritiba           0-2  Botafogo-RJ
São Paulo          2-1  Santa Cruz
Portuguesa         0-2  Goiás
Atlético-MG        0-0  Bahia
Juventude          1-1  Ponte Preta
Vasco da Gama      3-3  Cruzeiro

[Aug 8]
Gama               0-1  Atlético-PR
[Aug 9]
Internacional      1-1  Fluminense
Santos             1-1  São Paulo
Flamengo           1-1  Guarani
Botafogo-RJ        4-1  Portuguesa
Santa Cruz         2-1  Vitória
Bahia              1-1  Grêmio
Goiás              1-0  Coritiba

[Aug 11]
Palmeiras          1-1  Goiás
Vasco da Gama      1-0  Corinthians
Atlético-PR        2-1  Atlético-MG

[Aug 12]
Grêmio             0-2  Santos
Coritiba           0-1  Gama
São Paulo          3-2  Flamengo
[Aug 13]
Atlético-PR        0-0  Palmeiras
Guarani            0-1  Vasco da Gama
Corinthians        2-0  Santa Cruz
Portuguesa         2-0  Juventude
Botafogo-RJ        0-1  Internacional
Sport              1-1  Cruzeiro
Goiás              4-5  Vitória

[Aug 16]
Cruzeiro           2-2  São Paulo
Santa Cruz         1-1  Vasco da Gama
Santos             3-0  América-MG
Fluminense         0-0  Guarani
Internacional      1-1  Atlético-MG
Vitória            2-0  Portuguesa
Goiás              3-2  Botafogo-RJ
Gama               0-1  Bahia
Palmeiras          0-1  Corinthians
[Aug 17]
Flamengo           2-1  Coritiba

[Aug 19]
Atlético-MG        1-0  Santos
América-MG         1-1  Fluminense
Gama               1-1  Goiás
Palmeiras          1-4  Internacional
Guarani            0-1  Cruzeiro
[Aug 20]
Botafogo-RJ        1-1  Corinthians
Santa Cruz         2-2  Flamengo
Vasco da Gama      2-1  Ponte Preta
Juventude          1-1  Sport
Atlético-PR        1-3  Coritiba
São Paulo          1-1  Bahia

[Aug 23]
Vitória            2-4  Fluminense
Ponte Preta        3-0  Gama
Internacional      0-0  Guarani
América-MG         0-0  Atlético-PR
Bahia              1-3  Cruzeiro
Goiás              1-1  Santa Cruz
Juventude          1-1  Santos

[Aug 26]
Fluminense         2-0  Juventude
Cruzeiro           3-1  Vitória
Atlético-PR        2-1  São Paulo
Guarani            1-2  Botafogo-RJ
[Aug 27]
Ponte Preta        3-2  Atlético-MG
Corinthians        1-2  Grêmio
Internacional      1-1  Coritiba
Sport              2-0  Goiás
Santos             2-3  Palmeiras
Portuguesa         2-2  Vasco da Gama
Bahia              3-2  Santa Cruz

[Aug 30]
Corinthians        0-3  Santos
Guarani            1-2  Juventude
Portuguesa         3-1  Gama
Vitória            3-0  Internacional
Botafogo-RJ        0-2  Atlético-PR

[Sep 2]
Atlético-MG        1-2  Flamengo
Coritiba           1-1  Bahia
Gama               0-1  Internacional
Santos             1-1  Cruzeiro
Vitória            4-3  Sport
América-MG         1-0  Guarani
Fluminense         1-0  Botafogo-RJ
Grêmio             2-2  Ponte Preta
Palmeiras          0-3  São Paulo
Santa Cruz         0-0  Portuguesa

[Sep 5]
Vasco da Gama      2-2  Atlético-PR
Cruzeiro           1-1  Internacional
[Sep 6]
América-MG         5-2  Botafogo-RJ
Juventude          2-1  Coritiba
Fluminense         2-1  Portuguesa
Gama               1-1  Santa Cruz
[Sep 7]
Atlético-MG        3-1  Corinthians
Ponte Preta        2-1  Vitória
Grêmio             1-0  Sport

[Sep 9]
São Paulo          2-0  Fluminense
Santa Cruz         0-1  Santos
Goiás              2-0  América-MG
Sport              1-1  Guarani
[Sep 10]
Flamengo           0-0  Palmeiras
Corinthians        1-1  Vitória
Cruzeiro           2-1  Gama
Coritiba           2-0  Ponte Preta
Bahia              3-1  Vasco da Gama
Portuguesa         2-1  Atlético-MG
Juventude          4-3  Grêmio

[Sep 13]
Ponte Preta        3-3  São Paulo
Sport              4-1  Atlético-PR
Gama               2-0  Palmeiras
Vasco da Gama      4-3  Fluminense
Cruzeiro           4-0  Botafogo-RJ
Portuguesa         3-1  Bahia
Vitória            3-1  Coritiba
[Sep 14]
Grêmio             2-1  América-MG
Flamengo           3-1  Goiás

[Sep 16]
Internacional      1-1  Santos
Atlético-MG        2-2  Fluminense
Vitória            1-1  Gama
Atlético-PR        0-1  Juventude
Botafogo-RJ        3-1  Ponte Preta
[Sep 17]
Guarani            0-0  Goiás
Bahia              4-1  Flamengo
Palmeiras          1-1  Sport
Coritiba           1-1  Corinthians
América-MG         1-0  Santa Cruz
São Paulo          2-0  Portuguesa
Grêmio             0-0  Cruzeiro

[Sep 20]
Santos             2-1  Atlético-PR
Juventude          0-2  Gama
Vasco da Gama      4-0  América-MG
Ponte Preta        3-1  Portuguesa
Sport              3-0  Bahia

[Sep 23]
Flamengo           3-0  Santos
Guarani            2-0  Coritiba
Grêmio             1-0  Vitória
América-MG         1-1  Internacional
[Sep 24]
Fluminense         0-1  Palmeiras
Gama               1-3  São Paulo
Goiás              2-0  Cruzeiro
Corinthians        1-0  Ponte Preta
Santa Cruz         1-2  Atlético-MG
Portuguesa         1-0  Sport
Juventude          1-2  Vasco da Gama

[Sep 27]
São Paulo          3-0  América-MG
Portuguesa         2-3  Guarani
Ponte Preta        3-0  Sport
Botafogo-RJ        0-0  Vitória
Santa Cruz         2-1  Juventude
[Sep 28]
Corinthians        2-3  Atlético-PR

[Sep 30]
Gama               2-4  Flamengo
Goiás              2-2  São Paulo
América-MG         3-0  Juventude
Coritiba           1-2  Grêmio
Sport              3-2  Fluminense
Atlético-MG        2-4  Cruzeiro

[Oct 4]
Palmeiras          2-1  Coritiba
Vasco da Gama      4-0  Atlético-MG
São Paulo          1-1  Grêmio
Botafogo-RJ        2-1  Juventude
América-MG         1-1  Portuguesa
Santa Cruz         0-3  Sport
Atlético-PR        0-1  Guarani
Gama               2-1  Santos
Bahia              1-0  Vitória
Ponte Preta        2-0  Flamengo

[Oct 7]
Vitória            5-1  São Paulo
Sport              3-0  Gama
Juventude          0-1  Palmeiras
Santos             3-3  Ponte Preta
Guarani            2-2  Bahia
Atlético-PR        4-0  Santa Cruz
Internacional      1-2  Grêmio
América-MG         1-1  Cruzeiro
Botafogo-RJ        3-1  Flamengo
Corinthians        2-3  Portuguesa
Atlético-MG        2-1  Goiás

[Oct 10]
Cruzeiro           3-0  Santa Cruz
[Oct 11]
São Paulo          3-2  Coritiba
Ponte Preta        0-1  Atlético-PR
Fluminense         1-0  Grêmio
Atlético-MG        3-0  Guarani
Palmeiras          0-0  América-MG
Portuguesa         3-2  Internacional
Bahia              2-1  Corinthians
Vasco da Gama      2-2  Vitória

[Oct 12]
Cruzeiro           2-1  Juventude

[Oct 14]
Santos             1-1  Vasco da Gama
Palmeiras          3-2  Atlético-MG
Flamengo           1-2  Sport
Internacional      3-2  Bahia
[Oct 15]
Grêmio             2-2  Portuguesa
Juventude          1-2  Goiás
Santa Cruz         1-1  Coritiba
Botafogo-RJ        1-0  São Paulo
Guarani            3-2  Corinthians
Fluminense         2-1  Cruzeiro

[Oct 17]
São Paulo          1-1  Internacional
[Oct 18]
Guarani            3-2  Grêmio
Flamengo           1-2  América-MG
Palmeiras          0-1  Cruzeiro
Atlético-PR        1-0  Fluminense
Botafogo-RJ        2-0  Gama
[Oct 19]
Atlético-MG        2-1  Coritiba

[Oct 21]
Goiás              3-1  Santos
Portuguesa         2-1  Flamengo
Vasco da Gama      1-0  Gama
Internacional      4-0  Santa Cruz
[Oct 22]
Ponte Preta        5-1  Palmeiras
   [Washington (3), ?, ? ; ?]
Corinthians        1-3  Fluminense
Vitória            0-1  Juventude
São Paulo          2-2  Guarani
Coritiba           3-2  América-MG
Atlético-MG        2-2  Grêmio
Sport              2-2  Botafogo-RJ

[Oct 24]
Vasco da Gama      2-1  Goiás
[Oct 25]
Gama               0-0  Atlético-MG
Bahia              1-2  Ponte Preta
Fluminense         6-1  Santa Cruz
   [Magno Alves (5), ? ; ?]
Sport              3-1  Corinthians
Grêmio             2-1  Botafogo-RJ

[Oct 27]
Flamengo           4-0  Vasco da Gama
[Oct 28]
América-MG         2-3  Vitória
Grêmio             4-1  Gama
São Paulo          2-1  Atlético-MG
   [?, ? ; Guilherme]
Santa Cruz         1-5  Palmeiras
Santos             0-1  Bahia
Cruzeiro           5-1  Portuguesa
Sport              0-1  Internacional

[Nov 1]
Internacional      1-0  Corinthians
[Nov 2]
Guarani            2-1  Ponte Preta
[Nov 3]
Coritiba           0-1  Vasco da Gama

[Nov 4]
Bahia              2-0  Botafogo-RJ
Cruzeiro           3-1  Corinthians
Atlético-PR        3-1  Vitória
Goiás              2-2  Grêmio
Atlético-MG        0-1  América-MG
[Nov 5]
Internacional      2-0  Vasco da Gama
Juventude          3-1  São Paulo
Santa Cruz         0-3  Ponte Preta
Fluminense         1-1  Flamengo
Coritiba           2-1  Santos
Portuguesa         1-1  Palmeiras
  [Lúcio ; ?]

[Nov 8]
Ponte Preta        3-1  Internacional
Bahia              2-1  América-MG
Atlético-PR        1-1  Goiás
Santos             2-0  Portuguesa
Sport              4-3  São Paulo
[Nov 9]
Vitória            1-2  Guarani
Corinthians        1-2  Juventude
[Nov 10]
Palmeiras          3-0  Vasco da Gama

[Nov 11]
Goiás              3-3  Fluminense
Santos             3-1  Sport
Coritiba           3-1  Portuguesa
Atlético-MG        3-2  Juventude
Grêmio             3-0  Atlético-PR
[Nov 12]
Internacional      3-0  Flamengo
Bahia              1-2  Palmeiras
São Paulo          0-0  Corinthians
Vasco da Gama      1-2  Botafogo-RJ
Cruzeiro           2-2  Ponte Preta
Gama               1-2  Guarani

[Nov 14]
Flamengo           1-2  Cruzeiro

[Nov 15]
Juventude          0-0  Bahia
[Nov 16]
Corinthians        1-4  Flamengo
Guarani            3-2  Santos
Grêmio             0-1  Vasco da Gama
Botafogo-RJ        1-2  Santa Cruz
Fluminense         2-0  Coritiba
Sport              1-0  América-MG
Atlético-PR        2-1  Internacional
Goiás              3-0  Ponte Preta
Vitória            2-0  Atlético-MG

[Nov 19]
Santos             4-1  Botafogo-RJ
Palmeiras          2-0  Guarani
Portuguesa         2-1  Atlético-PR
Flamengo           3-2  Vitória
Internacional      2-1  Juventude
Atlético-MG        0-6  Sport
   [Leonardo (5), ?]
Santa Cruz         0-3  Grêmio
Bahia              0-1  Goiás
Coritiba           1-1  Cruzeiro
Vasco da Gama      0-4  São Paulo
Ponte Preta        3-4  Fluminense
América-MG         2-1  Corinthians


[1] teams that would have played 1st level in case of normal season
[2] teams that would have played 2nd level in case of normal season
[2*] successfully protested relegation to 2nd level in civil court


Yellow Module

First Phase


[Aug 8]
Botafogo-SP        1-1  União São João
São Caetano        3-1  Figueirense
Bangu              0-1  América-RJ
[Aug 9]
XV de Novembro     1-1  Bragantino
Paraná             1-0  Marcílio Dias
Joinville          0-0  Villa Nova-MG
Criciúma           2-0  Londrina
Caxias             1-1  Americano
Brasil             0-2  Avaí

[Aug 11]
América-RJ         1-0  Botafogo-SP
[Aug 13]
Londrina           0-3  XV de Novembro
Figueirense        3-0  Joinville
Avaí               2-0  Criciúma
Marcílio Dias      1-0  Brasil
Villa Nova-MG      1-2  Caxias
Americano          1-1  São Caetano
União São João     0-0  Paraná
[Aug 14]
Bragantino         1-2  Bangu

[Aug 16]
Paraná             1-0  Americano
Joinville          1-1  Londrina
Botafogo-SP        0-0  Figueirense
Brasil             1-1  União São João
XV de Novembro     1-0  Villa Nova-MG
São Caetano        2-1  Marcílio Dias
América-RJ         2-1  Avaí
[Aug 17]
Bangu              3-0  Criciúma
Caxias             1-1  Bragantino

[Aug 20]
Villa Nova-MG      1-0  Paraná
Criciúma           1-3  São Caetano
Figueirense        1-0  XV de Novembro
Bragantino         2-2  Brasil
Botafogo-SP        0-0  Avaí
Americano          2-1  Bangu
Londrina           0-0  América-RJ
Marcílio Dias      1-1  Joinville
[Aug 21]
União São João     0-0  Caxias

[Aug 23]
São Caetano        5-3  Villa Nova-MG
América-RJ         1-1  Bragantino
XV de Novembro     3-1  Criciúma
Paraná             3-0  Londrina
Joinville          3-0  Americano
Avaí               2-2  Bangu
[Aug 24]
Caxias             1-1  Botafogo-SP
Marcílio Dias      0-2  União São João

[Aug 26]
Criciúma           1-0  Paraná
[Aug 27]
São Caetano        4-3  Avaí
Botafogo-SP        3-1  Brasil
União São João     2-2  XV de Novembro
Bragantino         2-1  Londrina
Figueirense        3-2  Caxias
Marcílio Dias      1-2  Americano
Bangu              1-0  Joinville
Villa Nova-MG      2-1  América-RJ

[Aug 30]
XV de Novembro     0-1  Avaí
Paraná             2-1  Botafogo-SP
América-RJ         0-0  Criciúma
Americano          2-0  Villa Nova-MG
Caxias             2-4  São Caetano
Figueirense        3-1  Marcílio Dias
Joinville          0-0  Bragantino
Londrina           1-1  União São João
Brasil             4-1  Bangu

[Sep 2]
XV de Novembro     2-3  Caxias
Bangu              1-1  São Caetano
Bragantino         0-0  Marcílio Dias
Villa Nova-MG      0-0  Figueirense
Criciúma           2-1  Joinville
Paraná             2-0  Brasil
Avaí               1-1  Americano
União São João     1-1  América-RJ
[Sep 3]
Botafogo-SP        5-0  Londrina

[Sep 6]
São Caetano        1-0  Botafogo-SP
Joinville          3-0  Paraná
Figueirense        3-0  União São João
Americano          1-1  América-RJ
Londrina           1-0  Bangu
Bragantino         1-1  Villa Nova-MG
Brasil             0-0  XV de Novembro
Marcílio Dias      2-2  Avaí

[Sep 10]
Americano          2-1  Londrina
Bangu              0-0  Paraná
Criciúma           1-1  Bragantino
Botafogo-SP        5-2  Marcílio Dias
XV de Novembro     1-0  Joinville
União São João     4-3  Villa Nova-MG
São Caetano        3-0  Brasil
Avaí               1-1  Figueirense
[Sep 11]
América-RJ         2-3  Caxias

[Sep 13]
Paraná             0-0  São Caetano
Botafogo-SP        3-0  Bangu
Marcílio Dias      2-1  XV de Novembro
Bragantino         0-0  Americano
Londrina           0-1  Figueirense
Avaí               1-1  União São João
Villa Nova-MG      1-1  Criciúma
[Sep 14]
Joinville          2-2  Caxias
Brasil             2-1  América-RJ

[Sep 17]
Brasil             3-1  Villa Nova-MG
Caxias             3-1  Londrina
XV de Novembro     1-2  Paraná
São Caetano        1-1  União São João
Americano          1-1  Figueirense
Marcílio Dias      0-0  Bangu
América-RJ         3-1  Joinville
Criciúma           2-1  Botafogo-SP
Avaí               1-1  Bragantino

[Sep 20]
União São João     4-2  Bragantino
Joinville          2-0  Botafogo-SP
São Caetano        5-0  XV de Novembro
Villa Nova-MG      0-0  Marcílio Dias
Figueirense        2-0  América-RJ
Bangu              3-2  Caxias
Londrina           2-1  Brasil
Criciúma           3-0  Americano
Paraná             4-1  Avaí

[Sep 24]
Bangu              5-1  XV de Novembro
América-RJ         3-2  São Caetano
Botafogo-SP        2-1  Villa Nova-MG
Paraná             0-1  Bragantino
Figueirense        1-1  Criciúma
Londrina           0-1  Marcílio Dias
Brasil             0-1  Joinville
Americano          0-0  União São João
Avaí               1-1  Caxias

[Sep 27]
XV de Novembro     0-1  Botafogo-SP
Bragantino         1-1  Figueirense
União São João     0-2  Criciúma
Joinville          1-0  São Caetano
Americano          1-3  Brasil
Villa Nova-MG      3-3  Bangu
Marcílio Dias      1-0  América-RJ
Caxias             1-1  Paraná
Avaí               4-0  Londrina

[Sep 30]
Brasil             0-2  Figueirense
Caxias             1-0  Criciúma

[Oct 2]
Botafogo-SP        2-1  Americano

[Oct 4]
XV de Novembro     3-1  América-RJ
São Caetano        3-1  Bragantino
Bangu              2-1  União São João
Paraná             2-1  Figueirense
Villa Nova-MG      1-0  Londrina
Criciúma           1-0  Brasil
Caxias             3-3  Marcílio Dias
Joinville          2-2  Avaí

[Oct 7]
Americano          2-2  XV de Novembro
Bragantino         0-2  Botafogo-SP
União São João     1-1  Joinville
Figueirense        1-1  Bangu
Londrina           0-2  São Caetano
Brasil             0-1  Caxias
Marcílio Dias      1-1  Criciúma
Avaí               2-0  Villa Nova-MG
América-RJ         0-0  Paraná

[2] teams that would have played 2nd level in case of normal season

Group B

Participants
ABC FC (Natal-RN)                         Nacional FC (Manaus-AM)
América FC (Natal-RN)                     C Náutico Capibaribe (Recife-PE)
AA Anapolina (Anápolis-GO)                Paysandu SC (Belém-PA)
AD Bandeirante (Brasília-DF)              Clube do Remo (Belém-PA)
Ceará SC (Fortaleza-CE)                   River AC (Teresina-PI)
Clube de Regatas Brasil - CRB (Maceió-AL) Sampaio Corrêa FC (São Luís-MA)
Centro Sport. Alagoano - CSA (Maceió-AL)  São Raimundo EC (Manaus-AM)
A Desportiva F (Cariacica-ES)             GE Serra (EC)
Fortaleza EC (CE)                         Vila Nova EC (Goiânia-GO)

[Aug 6]
River              2-2  Nacional-AM
Fortaleza          1-0  Náutico
Anapolina          0-0  Serra
São Raimundo       2-0  Sampaio Corrêa
Remo               1-1  América-RN

[Aug 9]
CSA                1-2  River
São Raimundo       1-0  Paysandu
Remo               2-0  Nacional-AM
Anapolina          1-1  Bandeirante
América-RN         1-1  Ceará
Fortaleza          2-1  ABC
Desportiva         1-0  Vila Nova-GO
Sampaio Corrêa     1-2  Náutico
[Aug 10]
Serra              0-1  CRB

[Aug 12]
Vila Nova-GO       5-1  Sampaio Corrêa
[Aug 13]
Ceará              0-1  São Raimundo
CRB                1-1  Fortaleza
ABC                1-3  CSA
Náutico            2-1  América-RN
Paysandu           0-1  Serra
Bandeirante        0-0  Remo
Nacional-AM        1-1  Anapolina
River              2-0  Desportiva

[Aug 16]
CRB                2-1  ABC
Nacional-AM        1-2  Desportiva
Paysandu           0-0  Sampaio Corrêa
América-RN         1-0  Bandeirante
Ceará              3-0  Serra
River              3-2  Vila Nova-GO
Náutico            3-0  CSA
[Aug 17]
São Raimundo       1-2  Anapolina
Fortaleza          2-1  Remo

[Aug 19]
Serra              2-4  Náutico
Vila Nova-GO       2-3  América-RN
[Aug 20]
CSA                0-3  Paysandu
Remo               1-1  CRB
ABC                2-0  Bandeirante
Sampaio Corrêa     3-2  Nacional-AM
Desportiva         0-2  Ceará
Anapolina          0-0  Fortaleza
São Raimundo       2-1  River

[Aug 22]
Vila Nova-GO       0-1  Náutico
[Aug 23]
CSA                4-3  Nacional-AM
Paysandu           1-0  CRB
América-RN         1-1  ABC
Sampaio Corrêa     1-0  River
Bandeirante        0-2  Ceará
Desportiva         3-2  Fortaleza
Anapolina          3-1  Remo
[Aug 24]
Serra              0-0  São Raimundo

[Aug 26]
Ceará              1-0  CSA
Náutico            0-2  Anapolina
Nacional-AM        4-1  ABC
[Aug 27]
CRB                1-1  Vila Nova-GO
América-RN         3-0  Serra
Fortaleza          3-2  Paysandu
River              1-2  Remo
São Raimundo       4-1  Desportiva
Bandeirante        3-3  Sampaio Corrêa

[Aug 29]
Ceará              2-2  Anapolina
[Aug 30]
Fortaleza          1-2  Bandeirante
River              1-0  Serra
Nacional-AM        3-2  Náutico
Remo               1-2  ABC
América-RN         1-2  Paysandu
CSA                3-2  Vila Nova-GO
Desportiva         3-4  CRB

[Sep 2]
CRB                0-0  Ceará
Paysandu           3-1  River
ABC                3-0  São Raimundo
Vila Nova-GO       3-3  Fortaleza
Anapolina          4-0  Desportiva
Náutico            2-0  Bandeirante
Serra              1-1  Nacional-AM
[Sep 4]
Sampaio Corrêa     1-0  CSA

[Sep 6]
São Raimundo       4-5  Nacional-AM
Paysandu           1-0  Anapolina
ABC                2-0  Desportiva
River              2-1  Ceará
Bandeirante        2-2  Vila Nova-GO
Náutico            0-2  Remo
Serra              2-5  Fortaleza
[Sep 7]
CSA                0-2  CRB
Sampaio Corrêa     1-0  América-RN

[Sep 9]
Nacional-AM        1-0  Paysandu
Ceará              0-0  Náutico
[Sep 10]
CRB                6-2  Bandeirante
São Raimundo       2-0  CSA
Remo               1-0  Vila Nova-GO
Desportiva         0-6  Serra
América-RN         1-1  Anapolina
Fortaleza          2-0  Sampaio Corrêa
River              1-1  ABC

[Sep 13]
CSA                5-2  América-RN
Sampaio Corrêa     1-0  CRB
ABC                2-2  Ceará
Fortaleza          4-3  São Raimundo
Vila Nova-GO       2-0  Nacional-AM
Anapolina          3-2  River
Paysandu           0-0  Remo
Náutico            1-0  Desportiva
[Sep 14]
Bandeirante        1-2  Serra

[Sep 16]
ABC                2-2  Anapolina
[Sep 17]
CSA                1-1  Fortaleza
América-RN         1-0  River
Ceará              2-0  Nacional-AM
Sampaio Corrêa     3-2  Desportiva
Vila Nova-GO       1-1  Paysandu
Bandeirante        2-2  São Raimundo
Náutico            1-1  CRB
Serra              5-2  Remo

[Sep 20]
CRB                0-2  Anapolina
São Raimundo       2-1  América-RN
Náutico            2-0  ABC
Desportiva         1-1  CSA
Remo               1-1  Sampaio Corrêa
[Sep 21]
River              3-0  Bandeirante
Serra              2-0  Vila Nova-GO
Paysandu           4-2  Ceará
Nacional-AM        3-4  Fortaleza

[Sep 23]
CRB                0-0  América-RN
Remo               4-0  Desportiva
Vila Nova-GO       0-1  São Raimundo
[Sep 24]
Bandeirante        1-1  Nacional-AM
CSA                1-0  Anapolina
Fortaleza          3-1  River
Sampaio Corrêa     2-0  Ceará
Paysandu           0-0  Náutico
ABC                0-0  Serra

[Sep 27]
CSA                0-2  Serra
Nacional-AM        3-4  CRB
América-RN         4-0  Desportiva
Ceará              1-3  Fortaleza
Sampaio Corrêa     3-2  ABC
Bandeirante        0-1  Paysandu
Anapolina          1-0  Vila Nova-GO
Náutico            0-0  River
[Sep 28]
São Raimundo       4-1  Remo

[Sep 30]
América-RN         1-1  Fortaleza

[Oct 3]
Desportiva         3-0  Bandeirante
[Oct 4]
Serra              3-1  Sampaio Corrêa
Náutico            3-2  São Raimundo
River              1-1  CRB
Ceará              0-0  Vila Nova-GO
ABC                4-1  Paysandu
Remo               1-0  CSA

[Oct 7]
Anapolina          0-1  Sampaio Corrêa
Vila Nova-GO       0-1  ABC
Ceará              1-2  Remo
Paysandu           3-2  Desportiva
CRB                1-1  São Raimundo
Bandeirante        2-3  CSA
Nacional-AM        4-2  América-RN


[2] teams that would have played 2nd level in case of normal season

Second Phase

[Oct 14 and 18]
Caxias             2-0   1-1  Sampaio Corrêa
[Oct 14 an 19]
Remo               4-1   1-2  Figueirense
[Oct 15 and 18]
Avaí               0-2   2-1  Fortaleza
Criciúma           1-2   0-0  Náutico
Bangu              2-1   2-2  São Raimundo
[Oct 15 and 19]
Anapolina          0-1   0-2  Paraná
Paysandu           3-0   1-2  Botafogo-SP
[Oct 16 and 19]
CRB                1-1   1-4  São Caetano

Third Phase

[Oct 22 and 25]
Fortaleza          0-1   0-1  Paysandu
[Oct 23 and 26]
Náutico            1-0   2-6  São Caetano
Caxias             2-1   0-3  Remo
Bangu              0-3   1-2  Paraná

Semifinals

[Nov 1 and 5]
Paraná             0-0   2-1  Remo
[Nov 1 and 6]
Paysandu           1-1   4-5  São Caetano

Third Place Dispute

[Nov 12 and 19]
Remo               3-2   1-1  Paysandu

Final

[Nov 13 and 18]
Paraná             1-1   3-1  São Caetano


Green Module

First Phase

Group A

Participants
Botafogo FC (João Pessoa-PB)              AC Porto (Caruaru-PE)
Central SC (Caruaru-PE)                   Treze FC (Campina Grande-PB)
Moto Clube (São Luís-MA)                  Tuna Luso Brasileira (Belém-PA)
ADC Potiguar (Mossoró-RN)

Round 1 [Aug 6]
Porto              0-1  Central
Tuna Luso          3-1  Botafogo-PB
Treze              2-0  Moto Clube

Round 2 [Aug 9]
Porto              1-2  Tuna Luso
Botafogo-PB        3-1  Central
Moto Clube         3-1  Potiguar

Round 3 [Aug 13]
Potiguar           1-0  Porto
Tuna Luso          1-1  Moto Clube
Central            1-0  Treze

Round 4 [Aug 16]
Central            2-0  Potiguar
Treze              0-1  Tuna Luso
Moto Clube         2-0  Botafogo-PB

Round 5
[Aug 20]
Tuna Luso          2-0  Central
Porto              3-0  Treze
[Aug 21]
Botafogo-PB        5-0  Potiguar

Round 6 [Aug 24]
Potiguar           1-2  Tuna Luso
Treze              2-2  Botafogo-PB
Moto Clube         0-1  Porto

Round 7 [Aug 27]
Central            2-0  Moto Clube
Botafogo-PB        3-1  Porto
Potiguar           1-2  Treze

Round 8 [Sep 2]
Moto Clube         5-1  Central
Porto              0-2  Botafogo-PB
Treze              5-0  Potiguar

Round 9 [Sep 6]
Tuna Luso          3-0  Potiguar
Porto              1-0  Moto Clube
Botafogo-PB        1-0  Treze

Round 10 [Sep 10]
Central            3-2  Tuna Luso
Potiguar           1-0  Botafogo-PB
Treze              1-0  Porto

Round 11 [Sep 13]
Botafogo-PB        2-2  Moto Clube
Tuna Luso          3-2  Treze
Potiguar           0-2  Central

Round 12 
[Sep 16]
Moto Clube         3-3  Tuna Luso
[Sep 17]
Porto              6-2  Potiguar
Treze              1-0  Central

Round 13 [Sep 20]
Tuna Luso          1-2  Porto
Central            3-2  Botafogo-PB
Potiguar           2-3  Moto Clube

Round 14 
[Sep 23]
Moto Clube         5-1  Treze
[Sep 24]
Botafogo-PB        1-2  Tuna Luso
Central            0-0  Porto

Table
 1.Tuna Luso         12  8  2  2  25-15  26  Qualified
 2.Central           12  7  1  4  16-15  22  Qualified
 3.Moto Clube        12  5  3  4  24-17  18  Qualified
-------------------------------------------
 4.Botafogo-PB       12  5  2  5  22-17  17
 5.Porto             12  5  1  6  15-13  16
 6.Treze             12  5  1  6  16-17  16
 7.Potiguar          12  2  0 10   9-33   6
 
Group B

Participants
Assoc.Sport. Arapiraquense (Arapiraca-AL) SC Corinthians Alagoano (Maceió-AL)
Camaçari FC (BA)                          Juazeiro FC (BA)
Campinense Clube (Campina Grande-PB)      Sergipe SC (Aracaju-SE)
AD Confiança (Aracaju-SE)

Round 1
[Aug 6]
Sergipe            1-0  Camaçari
Confiança          1-0  Campinense
[Aug 29]
ASA                0-0  Juazeiro

Round 2 
[Aug 9]
Sergipe            0-1  Confiança
Campinense         0-3  Camaçari
[Aug 10]
Juazeiro           2-2  Corinthians-AL

Round 3 [Aug 13]
Confiança          2-1  Juazeiro
Camaçari           5-0  ASA
Corinthians-AL     2-1  Sergipe

Round 4 [Aug 16]
Camaçari           1-1  Corinthians-AL
ASA                0-1  Confiança
Juazeiro           2-1  Campinense

Round 5
[Aug 20]
Campinense         0-2  Corinthians-AL
[Aug 29]
Confiança          2-1  Camaçari
[Sep 4]
Sergipe            4-2  ASA

Round 6
[Aug 23]
Juazeiro           3-2  Sergipe
ASA                3-0  Campinense
Corinthians-AL     1-0  Confiança

Round 7
[Aug 26]
Camaçari           0-2  Juazeiro
Corinthians-AL     0-0  ASA
[Aug 27]
Campinense         3-2  Sergipe

Round 8
[Sep 1]
Sergipe            2-1  Campinense
ASA                3-1  Corinthians-AL
[Sep 2]
Juazeiro           1-0  Camaçari

Round 9 
[Sep 6]
Confiança          0-1  Corinthians-AL
[Sep 7]
Sergipe            1-0  Juazeiro
Campinense         0-1  ASA

Round 10 [Sep 10]
Corinthians-AL     3-1  Campinense
ASA                0-1  Sergipe
Camaçari           2-0  Confiança

Round 11 [Sep 13]
Campinense         2-2  Juazeiro          
Confiança          0-0  ASA
Corinthians-AL     1-0  Camaçari

Round 12 [Sep 17]
Juazeiro           2-0  Confiança
ASA                2-0  Camaçari
Sergipe            0-1  Corinthians-AL

Round 13 [Sep 20]
Confiança          1-1  Sergipe
Corinthians-AL     1-0  Juazeiro
Camaçari           1-1  Campinense

Round 14 [Sep 24]
Campinense         2-2  Confiança
Juazeiro           1-0  ASA
Camaçari           0-0  Sergipe

Table
 1.Corinthians-AL    12  8  3  1  16- 8  27  Qualified
 2.Juazeiro-BA       12  7  2  3  15- 9  23  Qualified
 3.Confiança         12  5  3  4  10-11  18  Qualified
-------------------------------------------
 4.Sergipe           12  5  2  5  15-14  17
 5.ASA               12  4  3  5  11-13  15
 6.Camaçari          12  3  3  6  13-11  12
 7.Campinense        12  1  2  9   9-23   5
 
Group C

Participants
Baré EC (Boa Vista-RR)                    Atl. Rio Negro Clube (Manaus-AM)
EC Flamengo (Teresina-PI)                 Tocantinópolis EC (TO)
SC Genus Rondoniense (Porto Velho-RO)     Ypiranga Clube (Macapá-AP)
Rio Branco FC (AC)

Round 1 [Aug 6]
Rio Branco-AC      4-2  Flamengo-PI
Genus              2-1  Rio Negro
Ypiranga           3-0  Baré

Round 2 
[Aug 9]
Rio Branco-AC      2-0  Genus
Rio Negro          0-2  Flamengo-PI
[Aug 30]
Baré               2-1  Tocantinópolis

Round 3
[Aug 12]
Flamengo-PI        4-0  Ypiranga
[Aug 13]
Genus              1-3  Baré
[Aug 15]
Tocantinópolis     1-1  Rio Branco-AC

Round 4
[Aug 16]
Ypiranga           5-3  Genus
Baré               0-0  Rio Negro
[Aug 17]
Flamengo-PI        2-0  Tocantinópolis

Round 5 [Aug 20]
Rio Negro          0-2  Tocantinópolis
Rio Branco-AC      2-2  Ypiranga
Genus              0-1  Flamengo-PI

Round 6 [Aug 23]
Tocantinópolis     4-0  Genus
Baré               2-1  Rio Branco-AC
Ypiranga           1-0  Rio Negro

Round 7
[Aug 26]
Flamengo-PI        1-0  Baré
[Aug 27]
Rio Negro          2-1  Rio Branco-AC
Tocantinópolis     1-0  Ypiranga

Round 8 [Sep 2]
Rio Branco-AC      3-0  Rio Negro
Ypiranga           3-0  Tocantinópolis
Baré               1-0  Flamengo-PI

Round 9 [Sep 6]
Genus              2-3  Tocantinópolis
Rio Branco-AC      1-0  Baré
Rio Negro          2-0  Ypiranga

Round 10
[Sep 9]
Flamengo-PI        1-0  Genus
[Sep 10]
Tocantinópolis     3-1  Rio Negro         
Ypiranga           1-0  Rio Branco-AC

Round 11 [Sep 13]
Tocantinópolis     1-0  Flamengo-PI
Genus              3-2  Ypiranga
Rio Negro          1-0  Baré

Round 12 [Sep 17]
Ypiranga           3-1  Flamengo-PI
Rio Branco-AC      2-1  Tocantinópolis
Baré               9-1  Genus

Round 13 [Sep 20]
Flamengo-PI        1-1  Rio Negro
Tocantinópolis     2-1  Baré
Genus              2-2  Rio Branco-AC

Round 14 [Sep 24]
Rio Negro          4-2  Genus
Flamengo-PI        3-1  Rio Branco-AC
Baré               3-3  Ypiranga

Table
 1.Flamengo-PI       12  7  1  4  18-11  22  Qualified
 2.Ypiranga-AP       12  6  2  4  23-19  20  Qualified
 3.Tocantinópolis    12  6  1  5  16-14  19  Qualified
-------------------------------------------
 4.Rio Branco-AC     12  5  3  4  20-16  18
 5.Baré              12  5  2  5  21-15  17
 6.Rio Negro         12  5  2  5  12-14  17
 7.Genus             12  2  1  9  16-37   7

Group D

Participants
Atlético C Goianiense (Goiânia-GO)        Goiânia EC (GO)
Brasília EC (DF)                          Interporto FC (Porto Nacional-TO)
EC Comercial (Campo Grande-MS)            Operário FC (Campo Grande-MS)
EC Dom Pedro II (Brasília-DF)

Round 1
[Aug 4]
Comercial-MS       1-0  Operário
[Aug 23]
Brasília           0-1  Atlético-GO

Round 2 [Aug 6]
Operário           1-2  Atlético-GO
Brasília           2-1  Dom Pedro II

Round 3 [Aug 9]
Atlético-GO        0-3  Goiânia
Dom Pedro II       0-0  Comercial-MS

Round 4 [Aug 13]
Operário           2-1  Dom Pedro II
Goiânia            1-2  Brasília

Round 5 [Aug 16]
Brasília           2-2  Operário
Dom Pedro II       1-1  Atlético-GO
Goiânia            1-0  Comercial-MS

Round 6 [Aug 20]
Goiânia            3-2  Operário
Atlético-GO        2-1  Comercial-MS

Round 7 [Aug 27]
Goiânia            1-2  Dom Pedro II
Brasília           1-2  Comercial-MS

Round 8
[Aug 30]
Operário           1-1  Goiânia
[Sep 10]
Comercial-MS       0-0  Atlético-GO

Round 9
[Sep 2]
Dom Pedro II       1-1  Goiânia
[Sep 16]
Comercial-MS       1-2  Brasília

Round 10
[Sep 6]
Atlético-GO        2-0  Brasília
[Sep 7]
Operário           0-2  Comercial-MS 

Round 11 
[Sep 13]
Operário           1-0  Brasília
Atlético-GO        0-1  Dom Pedro II
[Sep 14]
Comercial-MS       4-2  Goiânia

Round 12
[Sep 17]
Dom Pedro II       1-2  Operário
[Sep 19]
Brasília           1-1  Goiânia

Round 13
[Sep 20]
Comercial-MS       0-1  Dom Pedro II
[Sep 22]
Goiânia            1-1  Atlético-GO

Round 14 [Sep 24]
Atlético-GO        0-1  Operário
Dom Pedro II       2-0  Brasília

Table
 1.Operário-MS       10  5  2  3  13-11  17  Qualified
 2.Dom Pedro II      10  4  3  3  11- 9  15  Qualified
 3.Atlético-GO       10  4  3  3   9- 9  15  Qualified
-------------------------------------------
 4.Goiânia           10  3  4  3  15-14  13
 5.Comercial-MS      10  3  2  5   9-10  11
 6.Brasília          10  3  2  5  10-14  11
Interporto forfeited the tournament
 
Second Phase

Group 1

Round 1 [Sep 30]
Tuna Luso          2-0  Juazeiro
Ypiranga           2-1  Atlético-GO

Round 2 [Oct 4]
Juazeiro           2-1  Ypiranga
Atlético-GO        0-1  Tuna Luso

Round 3 [Oct 7]
Tuna Luso          1-0  Ypiranga
Atlético-GO        1-2  Juazeiro

Round 4 [Oct 11]
Juazeiro           2-0  Atlético-GO
Ypiranga           2-1  Tuna Luso

Round 5 [Oct 15]
Tuna Luso          3-2  Atlético-GO
Ypiranga           3-2  Juazeiro

Round 6 [Oct 19]
Juazeiro           5-0  Tuna Luso
Atlético-GO        3-2  Ypiranga

 
Group 2

Round 1 [Sep 30]
Corinthians-AL     1-3  Central
Dom Pedro II       2-1  Tocantinópolis

Round 2 [Oct 4]
Central            0-0  Dom Pedro II
Tocantinópolis     1-2  Corinthians-AL

Round 3 [Oct 7]
Tocantinópolis     2-1  Central
Corinthians-AL     2-2  Dom Pedro II

Round 4
[Oct 11]
Dom Pedro II       0-0  Corinthians-AL
[Oct 13]
Central            0-1  Tocantinópolis

Round 5 [Oct 15]
Corinthians-AL     5-1  Tocantinópolis
Dom Pedro II       2-3  Central

Round 6 [Oct 19]
Tocantinópolis     2-0  Dom Pedro II
Central            2-1  Corinthians-AL

 
Group 3

Round 1 [Sep 30]
Flamengo-PI        7-2  Operário
Moto Clube         2-1  Confiança

Round 2 [Oct 4]
Confiança          1-2  Flamengo-PI
Operário           3-3  Moto Clube

Round 3 [Oct 7]
Flamengo-PI        1-1  Moto Clube
Confiança          0-1  Operário

Round 4 [Oct 11]
Moto Clube         1-0  Flamengo-PI
Operário           1-1  Confiança

Round 5 [Oct 15]
Moto Clube         1-0  Operário
Flamengo-PI        3-5  Confiança

Round 6 [Oct 19]
Operário           1-0  Flamengo
Confiança          3-0  Moto Clube



White Module

Group E


Round 1 [Aug 6]
São José           1-2  Uberlândia
Juventus           2-0  Volta Redonda
Nacional-SP        2-1  Rio Branco-SP

Round 2 [Aug 9]
Nacional-SP        1-4  Juventus
Volta Redonda      1-1  Rio Branco-SP

Round 3 [Aug 13]
Juventus           4-0  Uberlândia
Rio Branco-SP      4-1  São José

Round 4 [Aug 16]
São José           0-1  Juventus
Uberlândia         1-0  Volta Redonda

Round 5 [Aug 20]
Nacional-SP        2-1  São José
Juventus           1-3  Rio Branco-SP

Round 6 [Aug 23]
Uberlândia         3-0  Nacional-SP
São José           2-2  Volta Redonda

Round 7 [Aug 27]
Volta Redonda      3-1  Nacional-SP
Rio Branco-SP      2-0  Uberlândia

Round 8 [Sep 2]
Uberlândia         1-1  Rio Branco-SP
Nacional-SP        1-0  Volta Redonda

Round 9 [Sep 6]
Nacional-SP        3-3  Uberlândia
Volta Redonda      2-1  São José

Round 10 
[Sep 9]
São José           0-2  Nacional-SP
[Sep 10]
Rio Branco-SP      2-2  Juventus

Round 11 [Sep 13]
Juventus           1-0  São José
Volta Redonda      0-1  Uberlândia

Round 12 [Sep 17]
Uberlândia         2-2  Juventus
São José           1-2  Rio Branco-SP

Round 13 [Sep 20]
Juventus           2-1  Nacional-SP
Rio Branco-SP      3-1  Volta Redonda

Round 14 [Sep 24]
Rio Branco-SP      4-0  Nacional-SP
Volta Redonda      1-1  Juventus
Uberlândia         2-1  São José


Group F


Round 1 [Aug 6]
Etti Jundiaí       4-0  Malutrom
Internacional-SP   1-1  União Bandeirante
Comercial-SP       1-1  Madureira

Round 2 
[Aug 9]
Etti Jundiaí       2-0  Internacional-SP
União Bandeirante  2-1  Malutrom
[Aug 30]
Madureira          2-0  União

Round 3 [Aug 13]
Internacional-SP   2-0  Madureira
Malutrom           3-0  Comercial-SP
União              0-2  Etti Jundiaí

Round 4
[Aug 16]
Madureira          6-0  União Bandeirante
Malutrom           3-2  União
[Aug 17]
Comercial-SP       2-1  Internacional-SP

Round 5 [Aug 20]
União Bandeirante  3-0  União
Internacional-SP   2-2  Malutrom
Etti Jundiaí       3-0  Comercial-SP

Round 6 [Aug 23]
Madureira          0-2  Etti Jundiaí
Comercial-SP       1-0  União Bandeirante
União              2-1  Internacional-SP

Round 7 
[Aug 27]
União              2-0  Comercial-SP
União Bandeirante  1-1  Etti Jundiaí
[Aug 28]
Malutrom           2-1  Madureira

Round 8
[Sep 2]
Madureira          0-0  Malutrom
Etti Jundiaí       8-0  União Bandeirante
[Sep 19]
Comercial-SP       2-1  União

Round 9 [Sep 6]
Internacional-SP   6-0  União
Etti Jundiaí       4-0  Madureira
União Bandeirante  3-0  Comercial-SP

Round 10
[Sep 9]
Malutrom           0-0  Internacional-SP
Comercial-SP       1-4  Etti Jundiaí
[Sep 10]
União              2-1  União Bandeirante

Round 11 [Sep 13]
Internacional-SP   2-0  Comercial-SP
União              0-2  Malutrom
União Bandeirante  1-1  Madureira

Round 12
[Sep 16]
Comercial-SP       1-4  Malutrom
Etti Jundiaí       5-2  União
[Sep 17]
Madureira          1-1  Internacional-SP

Round 13
[Sep 20]
Internacional-SP   2-4  Etti Jundiaí
Malutrom           2-2  União Bandeirante
[Sep 21]
União              1-1  Madureira

Round 14 [Sep 24]
Madureira          7-1  Comercial-SP
União Bandeirante  3-0  Internacional-SP
Malutrom           2-1  Etti Jundiaí


Group G

Round 1 [Aug 6]
União Agrícola     2-0  Mogi Mirim
Olimpia            1-1  Ipatinga
Matonense          1-0  Friburguense

Round 2 [Aug 9]
União Agrícola     0-0  Olimpia
Ipatinga           0-0  Mogi Mirim
Friburguense       1-1  São Cristóvão

Round 3 [Aug 13]
Olimpia            0-1  Friburguense
São Cristóvão      2-0  União Agrícola
Mogi Mirim         1-1  Matonense

Round 4 [Aug 16]
Mogi Mirim         4-0  São Cristóvão
Matonense          1-1  Olimpia
Friburguense       1-0  Ipatinga

Round 5 [Aug 20]
Olimpia            2-5  Mogi Mirim
Ipatinga           3-2  São Cristóvão
União Agrícola     1-2  Matonense

Round 6
[Aug 23]
Friburguense       0-0  União Agrícola
Matonense          2-0  Ipatinga
São Cristóvão      0-2  Olimpia

Round 7 [Aug 27]
Mogi Mirim         1-1  Friburguense
Ipatinga           4-2  União Agrícola
São Cristóvão      0-0  Matonense

Round 8 
[Sep 2]
Friburguense       2-2  Mogi Mirim
União Agrícola     0-0  Ipatinga
[Sep 3]
Matonense          1-1  São Cristóvão

Round 9 [Sep 6]
Olimpia            1-0  São Cristóvão
União Agrícola     3-1  Friburguense
Ipatinga           3-2  Matonense

Round 10 [Sep 10]
Mogi Mirim         2-2  Olimpia
São Cristóvão      2-1  Ipatinga
Matonense          2-1  União Agrícola

Round 11 [Sep 13]
Olimpia            1-0  Matonense
Ipatinga           0-1  Friburguense
São Cristóvão      1-0  Mogi Mirim

Round 12 [Sep 17]
União Agrícola     2-3  São Cristóvão
Friburguense       0-0  Olimpia
Matonense          2-2  Mogi Mirim

Round 13 [Sep 20]
Mogi Mirim         4-4  Ipatinga
Olimpia            3-1  União Agrícola
São Cristóvão      1-1  Friburguense

Round 14 [Sep 24]
Ipatinga           0-3  Olimpia
Friburguense       2-1  Matonense
Mogi Mirim         2-0  União Agrícola


Group H


Round 1 [Aug 9]
Internacional/SM   1-0  Olaria
Rio Branco-PR      2-1  Ituano
Santo André        2-2  Portuguesa/San

Round 2 [Aug 13]
Portuguesa/San     5-0  Internacional/SM
Ituano             1-3  Santo André
Olaria             0-1  Rio Branco-PR

Round 3
[Aug 16]
Rio Branco-PR      3-1  Portuguesa/San
Santo André        0-0  Olaria
[Aug 30]
Internacional/SM   0-2  Ituano

Round 4 [Aug 20]
Olaria             1-1  Portuguesa/San
Rio Branco-PR      1-1  Santo André

Round 5 [Aug 23]
Internacional/SM   1-4  Rio Branco-PR
Portuguesa/San     0-0  Ituano

Round 6 [Aug 27]
Santo André        2-0  Internacional/SM
Ituano             1-0  Olaria

Round 7
[Sep 1]
Olaria             3-1  Internacional/SM
[Sep 2]
Ituano             0-0  Rio Branco-PR
[Sep 3]
Portuguesa/San     3-0  Santo André

Round 8 [Sep 6]
Internacional/SM   3-0  Santo André
Olaria             2-1  Ituano

Round 9 [Sep 10]
Rio Branco-PR      0-0  Internacional/SM
Ituano             0-1  Portuguesa/San

Round 10 [Sep 13]
Santo André        1-2  Rio Branco-PR
Portuguesa/San     2-1  Olaria

Round 11 [Sep 17]
Santo André        2-0  Ituano
Rio Branco-PR      2-0  Olaria
Internacional/SM   1-1  Portuguesa/San

Round 12 [Sep 20]
Portuguesa/San     3-1  Rio Branco-PR
Olaria             2-0  Santo André
Ituano             4-0  Internacional/SM

 
Second Phase

Group 4 

Round 1 [Sep 30]
Rio Branco-SP      0-2  Malutrom
Friburguense       1-1  Santo André        [awarded 0-1, originally 1-1]

Round 2
[Oct 4]
Santo André        0-2  Rio Branco-SP
[Oct 5]
Malutrom           2-0  Friburguense

Round 3 [Oct 7]
Santo André        1-1  Malutrom
Rio Branco-SP      1-3  Friburguense

Round 4 [Oct 11]
Malutrom           4-2  Santo André
Friburguense       0-1  Rio Branco-SP

Round 5 [Oct 15]
Rio Branco-SP      4-0  Santo André
Friburguense       0-0  Malutrom

Round 6 [Oct 18]
Santo André        1-1  Friburguense
Malutrom           1-0  Rio Branco-SP

 
Group 5 

Round 1 [Sep 30]
Etti Jundiaí       1-2  Juventus           [awarded 1-0, orginally 1-2]
Portuguesa/San     2-1  Matonense

Round 2 [Oct 4]
Juventus           2-2  Portuguesa/San
Matonense          1-1  Etti Jundiaí

Round 3 [Oct 7]
Etti Jundiaí       2-0  Portuguesa/San
Matonense          2-1  Juventus

Round 4 [Oct 11]
Juventus           3-0  Matonense
Portuguesa/San     1-2  Etti Jundiaí

Round 5 [Oct 15]
Etti Jundiaí       7-0  Matonense
Portuguesa/San     2-0  Juventus

Round 6 [Oct 18]
Juventus           5-0  Etti Jundiaí
Matonense          0-0  Portuguesa/San

 
Group 3

Round 1 [Sep 30]
Olimpia            2-0  Rio Branco-PR
Uberlândia         1-0  União Bandeirante

Round 2 [Oct 4]
Rio Branco-PR      3-2  Uberlândia
União Bandeirante  0-1  Olimpia

Round 3 [Oct 7]
Olimpia            1-1  Uberlândia
União Bandeirante  0-1  Rio Branco-PR

Round 4 [Oct 11]
Uberlândia         3-0  Olimpia
Rio Branco-PR      2-1  União Bandeirante

Round 5 [Oct 15]
Olimpia            3-1  União Bandeirante
Uberlândia         0-0  Rio Branco-PR

Round 6 [Oct 18]
União Bandeirante  3-4  Uberlândia
Rio Branco-PR      0-0  Olimpia



Green and White Module Playoffs

Third Phase

Group 1

Round 1
[Oct 22]
Juazeiro           1-1  Uberlândia
[Oct 23]
Central            0-0  Olimpia

Round 2 
[Oct 25]
Uberlândia         5-0  Central
[Oct 26]
Olimpia            1-0  Juazeiro

Round 3 [Oct 29]
Juazeiro           1-1  Central
Olimpia            1-1  Uberlândia

Round 4 [Nov 1]
Uberlândia         2-1  Olimpia
Central            1-2  Juazeiro

Round 5 [Nov 5]
Juazeiro           1-0  Olimpia
Central            0-1  Uberlândia

Round 6 [Nov 8]
Uberlândia         0-1  Juazeiro
Olimpia            5-1  Central


Group 2

Round 1
[Oct 22]
Moto Clube         2-2  Malutrom
[Nov 4]
Etti Jundiaí       4-0  Tuna Luso

Round 2
[Oct 25]
Tuna Luso          1-0  Moto Clube
[Nov 13]
Etti Jundiaí       1-2  Malutrom

Round 3
[Oct 28]
Tuna Luso          3-1  Malutrom
[Oct 29]
Moto Clube         1-1  Etti Jundiaí

Round 4 [Nov 1]
Etti Jundiaí       7-0  Moto Clube
Malutrom           2-1  Tuna Luso

Round 5 [Nov 7]
Malutrom           1-1  Etti Jundiaí
Moto Clube         3-2  Tuna Luso

Round 6 [Nov 11]
Malutrom           4-3  Moto Clube
Tuna Luso          2-1  Etti Jundiaí

 
Final

[Nov 16 and 19]
Uberlândia         1-1   2-3  Malutrom
  [? ; ?]
  [? ; Flávio(pen), ?, ?]


Championship Eighthfinals
Away goal rule applied

[Nov 22 and 25]
Paraná             1-1   3-0  Goiás
  [Hélcio 51; Araújo 54]
  [Gil Baiano 71, Flávio 73, Indio (own goal) 89]
Internacional-RS   0-0   2-1  Atlético-PR 
  [Elivélton 68pen, Diogo 89; Kléber 44pen]
[Nov 22 and 26]
Remo               1-2   0-1  Sport
  [Robinho 50; Sidnei 59, Marquinhos 84]
  [Leomar 74]
[Nov 23 and 26]
Malutrom           0-3   1-1  Cruzeiro
  [Jackson 15, 67, Juan Pablo Sorín 60]
  [Calmon 85; Oséas 13]
São Caetano        3-3   1-0  Fluminense
  [Adhemar 26, Ailton 32, Serginho 37; Magno Alves 5, Roger 11, Agnaldo 90]
  [Adhemar 72]
Grêmio             1-0   1-2  Ponte Preta
  [Ronaldinho Gaúcho 71]
  [Zinho 58; Macedo 50, Hernani 61]
[Nov 25 and 28]
Bahia              3-3   2-3  Vasco da Gama
  [Jorge Wagner 1, Mauricio 5, Odvan (own goal) 79; Clebson 12, Romário 23, 
   Juninho Pernambucano 46]
  [Vágner 41, Fabrício Carvalho 58; Euller 27, 50, Juninho Paulista 75]
[Nov 25 and 30]
Palmeiras          1-1   2-1  São Paulo
  [Adriano 89; Marcelo Ramos 45]
  [Tuta 35pen, Galeano 57; Marcelo Ramos 55pen]

Quarterfinals
Away goal rule applied

[Nov 29 and Dec 2]
Internacional      1-1   2-3  Cruzeiro
  [Oséas (own goal) 28; Oséas 31]
  [Elivélton 1, Fábio Rochemback 46; Juan Pablo Sorín 38, Geovanni 43, 
   Fábio Júnior 71]
[Nov 30 and Dec 3]
Grêmio             2-1   1-1  Sport
  [Ronaldinho Gaúcho 41, 45; Taílson 61]
  [Ronaldinho Gaúcho 53; Adriano 60]
[Dec 3 and 9]
Vasco da Gama      3-1   0-1  Paraná
  [Juninho Paulista 23, Romário 50, 83; Flávio 58]
  [Reinaldo 50]
Palmeiras          3-4   2-2  São Caetano
  [Francisco Arce 27, 53, Taddei 45; Vágner 1, César 8, Adhemar 44, 66]
  [Galeano 5, Magrão 27; Serginho 42, César 50pen]

Semifinals
Away goal rule applied

[Dec 14 and 17]
São Caetano        3-2   3-1  Grêmio
  [Adhemar 45pen, 69, Daniel 77; Ronaldinho Gaúcho 70, 84]
  [César 51, 68, Adhemar 62; Zinho 7]
[Dec 16 and 23]
Vasco da Gama      2-2   3-1  Cruzeiro
  [Euller 39, 47; Fábio Júnior 79, Alex Mineiro 88]
  [Juninho Pernambucano 32, Euller 66, Romário 92; Juan Pablo Sorín 41]

Finals
Away goal rule applied

[Dec 27 and 30]
São Caetano        1-1   0-0  Vasco da Gama
  [César 14; Romário 27]

2nd leg replay
[Jan 18]
Vasco da Gama      3-1  São Caetano
    """.split("\n")   

# Initialize a list to hold the results
results = []

stage = "first"

# Regular expression for capturing teams and scores, including accents
match_pattern = re.compile(
    # r"([A-Za-zÀ-ÿ\s/-]+)\s+(\d+)-(\d+)\s+([A-Za-zÀ-ÿ\s/-]+)", re.UNICODE
    r"([A-Za-zÀ-ÿ\s/-]+)\s+(\d+\s*)-(s*\d+)\s+([A-Za-zÀ-ÿ\s/-]+)\s*(\[(\w{3} \d{1,2})\])*", re.UNICODE
)

match_pattern_2 = re.compile(
    r"([A-Za-zÀ-ÿ\s/-]+)\s+(\d+s*)-(s*\d+)\s+(\d+s*)-(s*\d+)\s+([A-Za-zÀ-ÿ\s/-]+)\s*(\[(\w{3} \d{1,2})\])*", re.UNICODE
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
          results.append([convert_date(date, year), home_team, home_score, away_score, away_team, False, False, stage])
          results.append([convert_date(date, year), away_team, away_score2, home_score2, home_team, False, False, stage])
          continue

        # Store the extracted data in results
        results.append([convert_date(current_date, year), home_team, home_score, away_score, away_team, False, False, stage])
        results.append([convert_date(current_date, year), away_team, away_score2, home_score2, home_team, False, False, stage])

    elif match:
        home_team = match.group(1).strip()
        home_score = match.group(2)
        away_score = match.group(3)
        away_team = match.group(4).strip()
        
        date = match.group(6)
        if date:
          results.append([convert_date(date, year), home_team, home_score, away_score, away_team, False, False, stage])
          continue

        # Store the extracted data in results
        results.append([convert_date(current_date, year), home_team, home_score, away_score, away_team, False, False, stage])
        
    # Check if the line contains a date
    date_match = re.search(r"\[(\w{3} \d{1,2})\]", line)
    if date_match:
        current_date = date_match.group(1)

    if line.startswith("First Phase"):
      stage = "first"

    if line.startswith("Second Phase"):
      stage = "second"

    if line.startswith("Third Phase"):
      stage = "third"

    if line.startswith("Quarterfinals") or line.startswith("Quarterfinal"):
      stage = "quarter"

    if line.startswith("Semifinals") or line.startswith("Semifinal"):
      stage = "semi"

    if line.startswith("Final"):
      stage = "final"

    if line.startswith("Playoff"):
      stage = "relegation"

print("Matches:", len(results))
# assert len(results) == 1065

dataframe = pd.DataFrame(results, columns=["date", "home_team", "home_score", "away_score", "away_team", "neutral", "knockout", "stage"])
dataframe.to_csv(FOLDER + str(year) + ".csv")
