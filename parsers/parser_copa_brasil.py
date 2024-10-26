import re

import pandas as pd
from datetime import datetime

FOLDER = "data/br/cup/"


def convert_date(date_string):
    # Map Portuguese abbreviations to English
    portuguese_to_english_months = {
        "jan": "jan", "fev": "feb", "mar": "mar", "abr": "apr", "mai": "may",
        "jun": "jun", "jul": "jul", "ago": "aug", "set": "sep", "out": "oct",
        "nov": "nov", "dez": "dec"
    }

    # Replace Portuguese month abbreviation with English
    for pt, en in portuguese_to_english_months.items():
        date_string = date_string.replace(pt, en)
    try:
      date_format = "%d %b %y"
      date_object = datetime.strptime(date_string, date_format)
      return date_object.strftime("%Y-%m-%d")
    except:
      raise Exception(date_string)


year = 2020

print(f"Parsing {year}")


lines = """
1a Fase 

[05 fev 20]  15:30 Coruripe-AL              0-0 Juventude-RS     .                  Gerson Amaral-Coruripe-AL                   
[05 fev 20]  15:30 Independente-PA          2-3 CRB-AL            .                 Baenão-Belem-PA                             [Leandro Cabecinha 2' (1ºT), Leandro Cabecinha 45+3' (2ºT) |  Rafael Longuine 5' (1ºT), Leo Gamalho 13' (1ºT), Rafael Longuine 1' (2ºT)]
[05 fev 20]  15:30 Barbalha-CE              0-3 Operário-PR        .                Inaldão-Barbalha-CE                         [Rafael Bonfim 20' (1ºT), Jefinho 4' (2ºT), Bustamante 25' (2ºT)]
[05 fev 20]  16:30 Santo André-SP           4-1 Criciúma-SC         .               Bruno José Daniel-Santo Andre-SP            [Douglas Baggio 3' (1ºT), Ronaldo 25' (1ºT), Branquinho 3' (2ºT), Branquinho 14' (2ºT) |  Andrew 42' (2ºT)]
[05 fev 20]  20:30 São Luiz-RS              0-0 América-RN           .              19 de Outubro-Ijui-RS                       
[05 fev 20]  20:30 Xv de Piracicaba-SP      1-0 Londrina-PR           .             Barão de Serra Negra-Piracicaba-SP          [Samuel 11' (2ºT)]
[05 fev 20]  20:30 Bahia de Feira-BA        3-1 Luverdense-MT          .            Arena Cajueiro-Feira de Santana-BA          [Deon 15' (1ºT), Menezes 21' (2ºT), Jarbas 26' (2ºT) |  Kaue 40' (2ºT)]
[05 fev 20]  20:30 Vilhenense-RO            1-1 Boa-MG                  .           Portal da Amazônia-Vilhena-RO               [Ariel 28' (2ºT) |  Anderson 29' (1ºT)]
[05 fev 20]  20:30 Santos-AP                1-1 America-MG               .          Zerão-Macapa-AP                             [Diego 36' (2ºT) |  Rodolfo 17' (1ºT)]
[05 fev 20]  21:30 River-PI                 1-0 Bahia-BA                  .         Albertão-Teresina-PI                        [Jean Natal 42' (2ºT)]
[05 fev 20]  21:30 Caxias-RS                1-1 Botafogo-RJ                .        Centenário-Caxias do Sul-RS                 [Carlos Alberto 18' (1ºT) |  Pedro Raul 13' (1ºT)]
[05 fev 20]  21:30 Palmas Ltda-TO           0-2 Paraná-PR                   .       Nilton Santos-Palmas-TO                     [Thiaguinho 32' (1ºT), Thiaguinho 24' (2ºT)]
[05 fev 20]  21:30 Operário-MT              0-0 Santa Cruz-PE                .      Arena Pantanal-Cuiaba-MT                    
[05 fev 20]  21:30 Aquidauanense-MS         0-1 ABC-RN                        .     Noroeste-Aquidauana-MS                      [Igor Goularte 33' (2ºT)]
[05 fev 20]  22:30 Fast Clube-AM            0-2 Goiás-GO                       .    Arena da Amazônia-Manaus-AM                 [Bessa 8' (2ºT), Marcinho 43' (2ºT)]
[06 fev 20]  16:30 Novorizontino-SP         1-2 Figueirense-SC                  .   Jorge de Biasi-Novo Horizonte-SP            [Thiago Ribeiro 14' (1ºT) |  Alemao 17' (2ºT), Diego 25' (2ºT)]
[06 fev 20]  19:15 Brasiliense-DF           1-1 Paysandu-PA                      .  Serra do Lago-Luziania-GO                   [Marcos Aurelio 7' (2ºT) |  Perema 3' (1ºT)]
[06 fev 20]  20:30 Vitoria FC-ES         2-1 CSA-AL                            . Salvador Costa-Vitoria-ES                   [Cassio 43' (1ºT), Edinho 5' (2ºT) |  Allano 21' (1ºT)]
[06 fev 20]  21:30 União-MT                 0-1 Atlético-GO                        .Luthero Lopes-Rondonopolis-MT               [Matheus Bossa 4' (2ºT)]
[11 fev 20]  21:30 Imperatriz-MA            0-0 Vitória-BA        .                 Frei Epifânio-Imperatriz-MA                 
[12 fev 20]  15:30 Bragantino-PA            1-2 Ceará-CE           .                Diogão-Braganca-PA                          [Adilson Canga 43' (2ºT) |  Luiz 45+1' (1ºT), Bergson 45+5' (2ºT)]
[12 fev 20]  16:00 Frei Paulistano-SE       1-2 Remo-PA             .               Titão-Frei Paulo-SE                         [Luan 21' (1ºT) |  Fredson 35' (1ºT), Gustavo Ermel 25' (2ºT)]
[12 fev 20]  16:00 Caucaia-CE               1-2 São José-RS          .              Raimundão-Caucaia-CE                        [Jacare 10' (2ºT) |  Alexandre 30' (2ºT), Matheuzinho 42' (2ºT)]
[12 fev 20]  16:00 Bangu-RJ                 1-1 Oeste-SP              .             Moça Bonita-Rio de Janeiro-RJ               [Rodrigo 11' (1ºT) |  Alyson Neves 6' (2ºT)]
[12 fev 20]  19:15 Brusque-SC               2-1 Sport-PE               .            Augusto Bauer-Brusque-SC                    [Edu 23' (1ºT), Ianson 37' (2ºT) |  Leandro Barcia 35' (1ºT)]
[12 fev 20]  20:30 Gama-DF                  3-3 Brasil-RS               .           Valmir Bezerra-Gama-DF                      [Nunes 12' (1ºT), Lucas 31' (1ºT), Platini 40' (2ºT) |  Wesley Pacheco 12' (1ºT), Simião 29' (1ºT), Poveda 16' (2ºT)]
[12 fev 20]  20:30 Atlético-BA              0-0 Botafogo-PB              .          Antônio Carneiro-Alagoinhas-BA              
[12 fev 20]  21:30 Toledo-PR                0-2 Náutico-PE                .         14 de Dezembro-Toledo-PR                    [Jean Carlos 14' (2ºT), Matheus Carvalho 24' (2ºT)]
[12 fev 20]  21:30 Campinense-PB            0-0 Atlético-MG                .        Amigão-Campina Grande-PB                    
[12 fev 20]  21:30 Galvez-AC                0-1 Vila Nova-GO                .       Arena Acreana-Rio Branco-AC                 [Adalberto 11' (2ºT)]
[12 fev 20]  21:30 Altos-PI                 1-1 Vasco da Gama-RJ             .      Albertão-Teresina-PI                        [[og] Marrony 20' (1ºT) |  German Cano 45+2' (1ºT)]
[12 fev 20]  21:30 Águia Negra-MS           2-1 Sampaio Corrêa-MA                 . Ninho D´águia-Rio Brilhante-MS              [Bahia 17' (1ºT), [og] Paulo Sergio 38' (2ºT) |  Gustavo 45+4' (2ºT)]
[12 fev 20]  22:30 Manaus-AM                1-0 Coritiba-PR                   .     Arena da Amazônia-Manaus-AM                 [Rossini 45' (1ºT)]
[13 fev 20]  16:30 Ferroviária-SP           2-0 Avaí-SC                        .    Fonte Luminosa-Araraquara-SP                [Henan 20' (2ºT), Hygor 25' (2ºT)]
[13 fev 20]  19:15 Novo Hamburgo-RS         1-2 Ponte Preta-SP                  .   Estádio do Vale-Novo Hamburgo-RS            [Alison 8' (2ºT) |  João Paulo 2' (1ºT), Roger 34' (2ºT)]
[13 fev 20]  20:30 Afogados-PE              3-0 Atlético-AC                      .  Vianão-Afogados da Ingazeira-PE             [Diego Ceará 24' (1ºT), Diego Ceará 40' (1ºT), DOUGLAS BOMBA 29' (2ºT)]
[13 fev 20]  21:30 São Raimundo-RR          2-2 Cruzeiro-MG                        .Canarinho-Boa Vista-RR                      [VERA CRUZ 25' (1ºT), Stanley 20' (2ºT) |  Edu 34' (1ºT), Alexandre Jesus 4' (2ºT)]
[19 fev 20]  15:30 Lagarto-SE               1-0 Volta Redonda-RJ      .             Albano Franco-Simao Dias-SE                 [Sapé 16' (2ºT)]
[19 fev 20]  19:15 Boavista-RJ              0-2 Chapecoense-SC         .            Elcyr Resende-Saquarema-RJ                  [Aylon 41' (1ºT), Vinicius 13' (2ºT)]
[26 fev 20]  21:30 Moto Club-MA             2-4 Fluminense-RJ           .           Castelão-Sao Luis-MA                        [Walace 1' (1ºT), JEORGE 11' (1ºT) |  Nene 16' (1ºT), Nene 3' (2ºT), Nino 27' (2ºT), Marcos Paulo 38' (2ºT)]
2a Fase 

[18 fev 20]  21:30 Vitoria FC-ES         0-1 Figueirense-SC           .          Salvador Costa-Vitoria-ES                   [Diego 45+3' (2ºT)]
[19 fev 20]  19:15 Paysandu-PA              1-1 CRB-AL                 .  PK: 3-5   Curuzu-Belem-PA                             [Caique Oliveira 45+2' (1ºT) |  Leo Gamalho 45' (1ºT)]
[19 fev 20]  21:30 Náutico-PE               1-1 Botafogo-RJ             . PK: 3-4   Aflitos-Recife-PE                           [Jean Carlos 43' (1ºT) |  Bruno Nazario 23' (2ºT)]
[19 fev 20]  21:30 Oeste-SP                 1-1 Ceará-CE                 .PK: 2-4   Arena Barueri-Barueri-SP                    [Lucas 44' (1ºT) |  Leandro 7' (1ºT)]
[20 fev 20]  21:30 Brusque-SC               5-1 Remo-PA                   .         Augusto Bauer-Brusque-SC                    [Thiago Alagoano 39' (1ºT), Airton 13' (2ºT), [og] Neguete 31' (2ºT), Edu 32' (2ºT), Thiago Alagoano 45+2' (2ºT) |  Giovane 25' (2ºT)]
[26 fev 20]  16:30 Xv de Piracicaba-SP      1-1 Juventude-RS          .   PK: 7-8   Barão de Serra Negra-Piracicaba-SP          [Daniel Costa 2' (2ºT) |  Eltinho 25' (2ºT)]
[26 fev 20]  19:15 Paraná-PR                3-2 Bahia de Feira-BA      .            Durival Britto-Curitiba-PR                  [Thales 45+1' (2ºT), Fabricio 45+3' (2ºT), Renan 45+7' (2ºT) |  Leo Porto 14' (2ºT), Cazumba 23' (2ºT)]
[26 fev 20]  20:30 River-PI                 1-1 América-RN              . PK: 3-4   Albertão-Teresina-PI                        [Valdo Bacabal 22' (2ºT) |  Dione 10' (1ºT)]
[26 fev 20]  20:30 Ferroviária-SP           6-2 Águia Negra-MS    .                 Fonte Luminosa-Araraquara-SP                [Henan 8' (1ºT), Tony 33' (1ºT), Claudinho 45+1' (1ºT), Claudinho 45+3' (1ºT), Max 14' (2ºT), Caio Rangel 45+3' (2ºT) |  Salomão 18' (1ºT), Pedro 38' (2ºT)]
[26 fev 20]  21:30 Afogados-PE              2-2 Atlético-MG        .      PK: 7-6   Vianão-Afogados da Ingazeira-PE             [CANDINHO 16' (2ºT), Philip 27' (2ºT) |  Gabriel Costa Franca 20' (2ºT), Ricardo Oliveira 33' (2ºT)]
[27 fev 20]  19:15 São José-RS              0-0 Chapecoense-SC      .     PK: 5-4   Francisco Novelletto-Porto Alegre-RS        
[27 fev 20]  21:30 Ponte Preta-SP           0-0 Vila Nova-GO         .    PK: 5-3   Moisés Lucarelli-Campinas-SP                
[04 mar 20]  19:15 Fluminense-RJ            2-0 Botafogo-PB           .             Maracanã-Rio de Janeiro-RJ                  [Marcos Paulo 6' (2ºT), Nene 27' (2ºT)]
[04 mar 20]  19:15 Santo André-SP           0-2 Goiás-GO               .            Bruno José Daniel-Santo Andre-SP            [Rafael Vaz 15' (2ºT), Bessa 45+2' (2ºT)]
[04 mar 20]  20:30 Brasil-RS                1-0 Manaus-AM               .           Bento Freitas-Pelotas-RS                    [Lazaro 27' (1ºT)]
[04 mar 20]  21:30 Boa-MG                   1-1 Cruzeiro-MG              .PK: 4-5   Dilzon Melo-Varginha-MG                     [Claudeci 13' (2ºT) |  Joao Lucas 36' (1ºT)]
[04 mar 20]  21:30 Atlético-GO              1-1 Santa Cruz-PE            .PK: 4-3   Olímpico Pedro Ludovico-Goiania-GO          [Renato Kayzer 14' (1ºT) |  Patrick 39' (1ºT)]
[05 mar 20]  19:15 Vitória-BA               3-1 Lagarto-SE                .         Manoel Barradas-Salvador-BA                 [Vico 5' (1ºT), Leonardo 41' (1ºT), Vico 31' (2ºT) |  Edilson 45+1' (1ºT)]
[05 mar 20]  20:00 Operário-PR              0-2 America-MG                 .        Germano Kruger-Ponta Grossa-PR              [Rodolfo 22' (2ºT), Felipe Augusto 25' (2ºT)]
[05 mar 20]  21:30 Vasco da Gama-RJ         1-0 ABC-RN                      .       Maracanã-Rio de Janeiro-RJ                  [German Cano 15' (2ºT)]
3a Fase 

[10 mar 20]  19:15 Botafogo-RJ              1-0 Paraná-PR        .                  Nilton Santos-Rio de Janeiro-RJ             [Luiz Fernando 11' (1ºT)]
[11 mar 20]  19:15 Juventude-RS             1-1 América-RN        .                 Alfredo Jaconi-Caxias do Sul-RS             [Iago Dias 38' (2ºT) |  Dione 37' (1ºT)]
[11 mar 20]  19:15 Figueirense-SC           1-0 Fluminense-RJ      .                Orlando Scarpelli-Florianopolis-SC          [Alemao 37' (2ºT)]
[11 mar 20]  19:15 Ferroviária-SP           0-0 America-MG          .               Fonte Luminosa-Araraquara-SP                
[11 mar 20]  21:30 Cruzeiro-MG              0-2 CRB-AL               .              Mineirão-Belo Horizonte-MG                  [Leo Gamalho 17' (1ºT), Leo Gamalho 13' (2ºT)]
[11 mar 20]  21:30 Atlético-GO              2-0 São José-RS           .             Olímpico Pedro Ludovico-Goiania-GO          [Nicolas 31' (1ºT), Renato Kayzer 43' (1ºT)]
[12 mar 20]  19:15 Ceará-CE                 1-0 Vitória-BA             .            Arena Castelão-Fortaleza                    [Rafael Sobis 44' (1ºT)]
[12 mar 20]  19:15 Ponte Preta-SP           3-0 Afogados-PE             .           Moisés Lucarelli-Campinas-SP                [[og] Heverton Luis 37' (1ºT), Roger 7' (2ºT), Bruno 20' (2ºT)]
[12 mar 20]  21:30 Brasil-RS                0-1 Brusque-SC               .          Bento Freitas-Pelotas-RS                    [Thiago Alagoano 44' (1ºT)]
[12 mar 20]  21:30 Vasco da Gama-RJ         0-1 Goiás-GO                  .         São Januário-Rio de Janeiro-RJ              [Fabio Sanches 43' (1ºT)]
[25 ago 20]  16:00 Afogados-PE              0-2 Ponte Preta-SP             .        Vianão-Afogados da Ingazeira-PE             [Zé Roberto 45+6' (1ºT), Guilherme Lazaroni 22' (2ºT)]
[25 ago 20]  19:00 America-MG               1-0 Ferroviária-SP              .       Independência-Belo Horizonte-MG             [Rodolfo 45+3' (2ºT)]
[25 ago 20]  21:30 Fluminense-RJ            3-0 Figueirense-SC               .      Maracanã-Rio de Janeiro-RJ                  [Nene 15' (1ºT), Nene 10' (2ºT), Nene 35' (2ºT)]
[26 ago 20]  16:00 América-RN               1-1 Juventude-RS        .     PK: 3-5   Arena das Dunas-Natal-RN                    [Zé Eduardo 19' (2ºT) |  Odivan 38' (1ºT)]
[26 ago 20]  16:00 CRB-AL                   1-1 Cruzeiro-MG          .              Rei Pelé-Maceio-AL                          [Leo Gamalho 9' (2ºT) |  Giovanni Palmieri 45' (1ºT)]
[26 ago 20]  19:00 Paraná-PR                1-2 Botafogo-RJ           .             Durival Britto-Curitiba-PR                  [Thales 10' (2ºT) |  Marcelo 4' (2ºT), Danilo Barcelos 45+5' (2ºT)]
[26 ago 20]  21:30 Vitória-BA               3-4 Ceará-CE               .            Manoel Barradas-Salvador-BA                 [Leonardo 8' (1ºT), Carleto 15' (1ºT), Jordy Caicedo 20' (2ºT) |  Vina 45+2' (1ºT), [og] Carleto 3' (2ºT), Fernando 16' (2ºT), Lima 44' (2ºT)]
[26 ago 20]  21:30 Goiás-GO                 1-2 Vasco da Gama-RJ        . PK: 2-3   Hailé Pinheiro-Goiania-GO                   [Rafael Vaz 44' (1ºT) |  Henrique 32' (1ºT), Martin Benitez 5' (2ºT)]
[27 ago 20]  19:00 Brusque-SC               1-0 Brasil-RS                .          Augusto Bauer-Brusque-SC                    [Nuno 38' (1ºT)]
[27 ago 20]  21:30 São José-RS              1-0 Atlético-GO               .         Francisco Novelletto-Porto Alegre-RS        [Marcelo 38' (1ºT)]
4a Fase 

[16 set 20]  19:00 Ponte Preta-SP           2-2 America-MG           .              Moisés Lucarelli-Campinas-SP                [Moises 5' (1ºT), Matheus Peixoto 29' (2ºT) |  Marcelo Toscano 43' (1ºT), Felipe Azevedo 45+1' (2ºT)]
[16 set 20]  21:30 Fluminense-RJ            1-0 Atlético-GO           .             Maracanã-Rio de Janeiro-RJ                  [[og] João Victor 31' (2ºT)]
[16 set 20]  21:30 Brusque-SC               0-2 Ceará-CE               .            Augusto Bauer-Brusque-SC                    [Leandro 39' (1ºT), Vina 45+1' (2ºT)]
[17 set 20]  16:00 Juventude-RS             2-0 CRB-AL                  .           Alfredo Jaconi-Caxias do Sul-RS             [Igor Inocencio 33' (1ºT), Wagner 35' (2ºT)]
[17 set 20]  19:00 Botafogo-RJ              1-0 Vasco da Gama-RJ         .          Nilton Santos-Rio de Janeiro-RJ             [Matheus Babi 22' (2ºT)]
[22 set 20]  19:00 CRB-AL                   1-0 Juventude-RS              .         Rei Pelé-Maceio-AL                          [Leo Gamalho 32' (1ºT)]
[22 set 20]  21:30 America-MG               3-1 Ponte Preta-SP             .        Independência-Belo Horizonte-MG             [Felipe Azevedo 32' (1ºT), Ale 36' (1ºT), Rodolfo 17' (2ºT) |  Apodi 45+2' (2ºT)]
[23 set 20]  21:30 Ceará-CE                 5-1 Brusque-SC                  .       Arena Castelão-Fortaleza                    [Rafael Sobis 44' (1ºT), Rafael Sobis 18' (2ºT), Bergson 29' (2ºT), [og] Airton 33' (2ºT), Tiago 44' (2ºT) |  Alex Sandro 19' (1ºT)]
[23 set 20]  21:30 Vasco da Gama-RJ         0-0 Botafogo-RJ                  .      São Januário-Rio de Janeiro-RJ              
[24 set 20]  20:00 Atlético-GO              3-1 Fluminense-RJ                 .     Olímpico Pedro Ludovico-Goiania-GO          [Chico 9' (1ºT), Marlon Freitas 33' (2ºT), Matheus Vargas 45+2' (2ºT) |  Luccas Claro 45+5' (1ºT)]
Oitavas de Final

[14 out 20]  19:15 Fortaleza-CE             3-3 São Paulo-SP            .           Arena Castelão-Fortaleza                    [David 5' (1ºT), Guilherme 20' (1ºT), Gabriel Dias 20' (2ºT) |  Brenner 16' (1ºT), Luciano 44' (1ºT), Brenner 45+4' (2ºT)]
[25 out 20]  20:30 São Paulo-SP             2-2 Fortaleza-CE             .PK: 10-9  Morumbi-Sao Paulo-SP                        [Brenner 10' (1ºT), Brenner 26' (2ºT) |  David 35' (2ºT), Roger 45+2' (2ºT)]
[27 out 20]  21:30 Botafogo-RJ              0-1 Cuiabá-MT                 .         Nilton Santos-Rio de Janeiro-RJ             [Matheus Barbosa 9' (2ºT)]
[28 out 20]  16:00 Santos-SP                0-0 Ceará-CE                   .        Vila Belmiro-Santos                         
[28 out 20]  19:00 Atlético-GO              1-2 Internacional-RS            .       Olímpico Pedro Ludovico-Goiania-GO          [Jean 45+1' (2ºT) |  Leandro 12' (1ºT), Moises 15' (2ºT)]
[28 out 20]  21:30 Athletico-PR             0-1 Flamengo-RJ                  .      Arena da Baixada-Curitiba-PR                [Bruno Henrique 20' (1ºT)]
[28 out 20]  21:30 Corinthians-SP           0-1 America-MG                    .     Neo Química Arena-Sao Paulo-SP              [Marcelo Toscano 43' (2ºT)]
[29 out 20]  19:00 Red Bull Bragantino-SP   1-3 Palmeiras-SP                   .    Nabi Abi Chedid-Braganca Paulista-SP        [Jan Hurtado 37' (2ºT) |  Raphael Veiga 5' (1ºT), Wesley Ribeiro Silva 18' (1ºT), Luiz Adriano 27' (1ºT)]
[29 out 20]  21:30 Grêmio-RS                1-0 Juventude-RS                    .   Arena do Grêmio-Porto Alegre-RS             [Isaque 8' (1ºT)]
[03 nov 20]  19:00 Cuiabá-MT                0-0 Botafogo-RJ                      .  Arena Pantanal-Cuiaba-MT                    
[03 nov 20]  21:30 Internacional-RS         2-1 Atlético-GO                       . Beira-Rio-Porto Alegre-RS                   [Thiago Galhardo 9' (2ºT), Rodinei 31' (2ºT) |  Junior Brandao 40' (2ºT)]
[04 nov 20]  19:00 Ceará-CE                 1-0 Santos-SP                         . Arena Castelão-Fortaleza                    [Vina 25' (2ºT)]
[04 nov 20]  21:30 Flamengo-RJ              3-2 Athletico-PR                      . Maracanã-Rio de Janeiro-RJ                  [Pedro 24' (1ºT), Pedro 33' (1ºT), Michael 38' (2ºT) |  Erick 40' (1ºT), Bissoli 42' (2ºT)]
[04 nov 20]  21:30 America-MG               1-1 Corinthians-SP                    . Independência-Belo Horizonte-MG             [Rodolfo 38' (2ºT) |  Fagner 14' (2ºT)]
[05 nov 20]  19:00 Palmeiras-SP             1-0 Red Bull Bragantino-SP            . Allianz Parque-Sao Paulo-SP                 [Gabriel Veron 29' (1ºT)]
[05 nov 20]  21:30 Juventude-RS             0-1 Grêmio-RS                         . Alfredo Jaconi-Caxias do Sul-RS             [Thaciano 24' (2ºT)]
Quartas de Final 

[11 nov 20]  16:30 Palmeiras-SP             3-0 Ceará-CE         .                  Allianz Parque-Sao Paulo-SP                 [Gustavo Scarpa 34' (1ºT), Raphael Veiga 37' (1ºT), Gabriel Veron 39' (1ºT)]
[11 nov 20]  19:00 Cuiabá-MT                1-2 Grêmio-RS         .                 Arena Pantanal-Cuiaba-MT                    [Willians 19' (1ºT) |  Diego Souza 7' (1ºT), Jean Pyerre 43' (1ºT)]
[11 nov 20]  21:30 Flamengo-RJ              1-2 São Paulo-SP       .                Maracanã-Rio de Janeiro-RJ                  [Gabriel Barbosa 3' (2ºT) |  Brenner 1' (2ºT), Brenner 42' (2ºT)]
[11 nov 20]  21:30 Internacional-RS         0-1 America-MG          .               Beira-Rio-Porto Alegre-RS                   [Rodolfo 12' (1ºT)]
[18 nov 20]  16:30 Grêmio-RS                2-0 Cuiabá-MT            .              Arena do Grêmio-Porto Alegre-RS             [Diego Souza 9' (1ºT), Diego Souza 41' (1ºT)]
[18 nov 20]  19:00 Ceará-CE                 2-2 Palmeiras-SP          .             Arena Castelão-Fortaleza                    [Vina 12' (2ºT), Tiago 16' (2ºT) |  Raphael Veiga 27' (1ºT), Raphael Veiga 45+4' (1ºT)]
[18 nov 20]  21:30 São Paulo-SP             3-0 Flamengo-RJ            .            Morumbi-Sao Paulo-SP                        [Luciano 1' (2ºT), Luciano 10' (2ºT), Pablo 39' (2ºT)]
[18 nov 20]  21:30 America-MG               0-1 Internacional-RS        . PK: 6-5   Independência-Belo Horizonte-MG             [Yuri Alberto 45+4' (2ºT)]
Semi Finais 

[23 dez 20]  21:30 Grêmio-RS                1-0 São Paulo-SP    .                   Arena do Grêmio-Porto Alegre-RS             [Diego Souza 17' (2ºT)]
[23 dez 20]  21:30 Palmeiras-SP             1-1 America-MG       .                  Allianz Parque-Sao Paulo-SP                 [GUSTAVO GOMEZ 45+3' (1ºT) |  Ademir 19' (1ºT)]
[30 dez 20]  21:30 São Paulo-SP             0-0 Grêmio-RS         .                 Morumbi-Sao Paulo-SP                        
[30 dez 20]  21:30 America-MG               0-2 Palmeiras-SP       .                Independência-Belo Horizonte-MG             [Luiz Adriano 23' (2ºT), Rony 40' (2ºT)]
Final 

[28 fev 21]  21:00 Grêmio-RS                0-1 Palmeiras-SP        .               Arena do Grêmio-Porto Alegre-RS             [GUSTAVO GOMEZ 31' (1ºT)]
[07 mar 21]  18:00 Palmeiras-SP             2-0 Grêmio-RS            .              Allianz Parque-Sao Paulo-SP                 [Wesley Ribeiro Silva 8' (2ºT), Gabriel Menino 39' (2ºT)]
   """.split("\n")   

# Initialize a list to hold the results
results = []

stage = "first"

# Regular expression for capturing teams and scores, including accents
match_pattern = re.compile(
    r"\[(\d{2} \w{3} \d{2})\]\s+\d{2}\:\d{2}\s+([0-9A-Za-zÀ-ÿ\s/-]+)\s+(\d+\s*)-(s*\d+)\s+([0-9A-Za-zÀ-ÿ\s/-]+)", re.UNICODE
)

# Process each line
for line in lines:
    # line = line.strip()

    match = match_pattern.match(line)

    if match:
        date = match.group(1)
        home_team = match.group(2).strip()
        home_score = match.group(3)
        away_score = match.group(4)
        away_team = match.group(5).strip()

        # Store the extracted data in results
        results.append([convert_date(date), home_team, home_score, away_score, away_team, False, False, stage])

    if line.startswith("First Phase") or line.startswith("1a Fase"):
      stage = "first"

    if line.startswith("Second Phase") or line.startswith("2a Fase"):
      stage = "second"

    if line.startswith("Third Phase") or line.startswith("3a Fase"):
      stage = "third"

    if line.startswith("Fourth Phase") or line.startswith("4a Fase"):
      stage = "fourth"

    if line.startswith("Round16") or line.startswith("Oitavas de Final"):
      stage = "round16"

    if line.startswith("Quarterfinals") or line.startswith("Quarterfinal") or line.startswith("Quartas de Final"):
      stage = "quarter"

    if line.startswith("Semifinals") or line.startswith("Semifinal") or line.startswith("Semi Finais"):
      stage = "semi"

    if line.startswith("Final"):
      stage = "final"

    if line.startswith("Playoff"):
      stage = "relegation"

print("Matches:", len(results))
assert len(results) == 120

dataframe = pd.DataFrame(results, columns=["date", "home_team", "home_score", "away_score", "away_team", "neutral", "knockout", "stage"])
dataframe.to_csv(FOLDER + str(year) + ".csv")
