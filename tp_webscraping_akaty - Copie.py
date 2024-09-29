# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 05:23:13 2024

@author: Godwin AKATY
"""

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv

# Exemple de listes de statistiques avec leur code
statistic_codes = [ ("PIB", "NY.GDP.MKTP.CD","2"),("IDH", "SP.POP.IDH.IN","1"),("Esperance_de_vie", "SP.DYN.LE00.IN","3")]

# Récupérer la liste des pays avec leurs codes
url = "https://perspective.usherbrooke.ca/bilan/BMEncyclopedie/BMEncycloListePays.jsp"
service=Service(ChromeDriverManager().install())
driver=webdriver.Chrome(service=service)
driver.get(url)
html=driver.page_source
soup=BeautifulSoup(html,"html.parser")
countries=soup.find("section", class_="maingroup")
name_code_pays=[]
for country in countries.find_all("li"):
    country_name = country.a.text.strip()
    country_code = country.a['href'].split('/')[-1]
    name_code_pays.append({'name': country_name, 'code': country_code})

# Fonction pour récupérer les informations sur différentes statistiques d'un pays

def get_country_stats(country_code,stat_code,numero_theme):
    link = "https://perspective.usherbrooke.ca/bilan/servlet/BMTendanceStatPays?langue=fr&codePays=" + country_code + "&codeStat="+stat_code+"&codeTheme="+numero_theme+""
    service=Service(ChromeDriverManager().install())
    driver=webdriver.Chrome(service=service)
    driver.get(link)
    response=driver.page_source
    soup = BeautifulSoup(response, "html.parser")
    table = soup.find_all('td')
    s_data = []
    for year in range(1960, 2022):
        available = False
        for i in range(0, len(table), 3):
            year_value = int(table[i].text.strip())
            if year == year_value:
                s_value = table[i+1].text.strip().replace("\xa0", "")
                s_data.append(s_value)
                available = True
                break
        if not available:
            s_data.append('')
    return s_data

# Écrire les données dans des fichiers CSV

def write_country_data_to_csv(lescodes, stats_data):
    for stat_name, stat_code ,numero in stats_data:
        with open(f"{stat_name}.csv", 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Pays', 'Code'] + [str(year) for year in range(1960, 2022)]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for country in lescodes:
                gdp_data = get_country_stats(country['code'], stat_code,numero)
                writer.writerow({'Pays': country['name'], 'Code': country['code'], **{str(year): gdp_data[idx] for idx, year in enumerate(range(1960, 2022))}})

# Exécution
write_country_data_to_csv(lescodes=name_code_pays,stats_data=statistic_codes)
