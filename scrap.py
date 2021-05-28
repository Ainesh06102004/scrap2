from typing import final
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv
import requests

START_URL = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser = webdriver.Chrome("./chromedriver")
browser.get(START_URL)

time.sleep(10)

planet_data = []
newplanetdata = []
headers = ["NAME", "LIGHT-YEARS FROM EARTH", "PLANET MASS", "STELLAR MAGNITUDE", "DISCOVERY DATE",
           "HYPERLINK", "PLANET TYPE", "PLANET RADIUS", "ORBITAL RADIUS", "ORBITAL PERIOD", "ECCENTRICITY"]


def scrap():
    for i in range(440):
        soup = BeautifulSoup(browser.page_source, "html.parser")

        for ul_tag in soup.find_all("ul", attrs={"class": "exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if(index == 0):
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            
            hyperlink_li_tag = li_tags[0]
            temp_list.append("https://exoplanets.nasa.gov" + hyperlink_li_tag.find_all("a", href = True)[0]["href"])
            planet_data.append(temp_list)
        browser.find_element_by_xpath(
            '//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()

    """with open("scrapdata.csv", 'w') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(planet_data)"""


def scrapmoredata(hyperlink):
    page = requests.get(hyperlink)
    soup = BeautifulSoup(page.content, "html.parser")

    for tr_tag in soup.find_all("tr", attrs={"class": "fact_row"}):
        td_tags = tr_tag.find_all("td")
        templist = []

        for tdtag in td_tags:
            try:
                templist.append(tdtag.find_all(
                    "div", attrs={"class": "value"})[0].contents[0])
            except:
                templist.append("")

        newplanetdata.append(templist)


scrap()

for data in planet_data:
    scrapmoredata(data[5])

finalplanetdata = []

for index, data in enumerate(planet_data):
    finalplanetdata.append(data + finalplanetdata[index])

with open("finaldata.csv", 'w') as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(finalplanetdata)
