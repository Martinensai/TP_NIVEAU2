# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 00:42:00 2024

@author: Godwin AKATY
"""



import requests
from bs4 import BeautifulSoup
import csv


#pip install selenium
#pip install webdriver

url = "https://www.scrapethissite.com/pages/simple/"

response = requests.get(url)
response.encoding = "utf-8"

if response.status_code == 200:
    html = response.text
    soup = soup = BeautifulSoup(html, 'html.parser')
    countries = soup.find_all('div', class_="col-md-4 country")
    with open ("pays.csv", "w", newline = "", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Pays", "Capital", "Population", "Superficie"])
        for country in countries :
            name = country.find('h3',class_ = "country-name").text.strip()
            capital =  country.find('span',class_ = "country-capital").text.strip()
            population = country.find('span',class_ = "country-population").text.strip()
            area = country.find('span',class_ = "country-area").text.strip()
            writer.writerow([name,capital,population,area])
        
    
else:
    print("erreur :"+response.status_code)