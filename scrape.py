from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import bs4
import re
import csv

# (at Lap Times page) document.querySelector("div#__next > div:nth-child(7) > div:nth-child(3) > div:nth-child(1) > table") = JS command to get HTML table, then copy/paste to test.html

def getData():
    #Open test.html
    f = open("test.html","rb")
    page = f.read()

    page_soup = soup(page,"html.parser")
    rows = page_soup.find_all("tr")

    driverLaps = []
    for row in rows[1:]:
        driver = row.find("td")
        laptimes = []
        for time in row.findAll("td")[1:]:
            if time.text == '':
                continue
            minute = re.findall("([0-9]+):",time.text)
            second = re.findall(":([0-9]*.[0-9]*)",time.text)
            totalTime = 0
            if len(minute) > 0: 
                totalTime += int(minute[0])*60
            totalTime += float(second[0])
            laptimes.append(round(totalTime,3))
        driverLaps.append([driver.text]+laptimes)
    
    with open("races/csv.csv","w",newline='') as csvfile:
        raceNo = 7  #change this number for different races
        csvwriter = csv.writer(csvfile)
        for row in driverLaps:
            laptimes = row[1:]
            driver = row[0]
            for i in range(len(laptimes)):
                csvwriter.writerow([raceNo,driver,i+1,laptimes[i]])
    csvfile.close()

getData()