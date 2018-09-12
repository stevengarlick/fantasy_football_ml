import requests
from bs4 import BeautifulSoup,SoupStrainer
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

columns = ['year', 'awaytm', 'hometm', 'roof', 'surface', 'temp', 'wind', 'spread', 'ou']
df1 = pd.DataFrame(columns = columns)

page = urllib.request.urlopen("https://www.pro-football-reference.com/years/2018/games.htm")
boxscores = BeautifulSoup(page,'lxml')
for link in boxscores.findAll('a', href=True, text='boxscore'):
    url = 'https://www.pro-football-reference.com'
    fullurl = url + str(link['href'])
    page = requests.get(fullurl)
    soup = BeautifulSoup(page.content,'lxml')
    t = soup.find_all('table')[0]
    for td in t.find_all("tr")[1].find_all('td')[1]:
        awaytm = td.get_text(strip=True)
    for td in t.find_all("tr")[2].find_all('td')[1]:
        hometm = td.get_text(strip=True)
    print(awaytm + ' vs ' + hometm)
    year = '2018'
    path_to_extension = r'C:\Users\User1\1.16.18_0'
    chrome_options = Options()
    chrome_options.add_argument('load-extension=' + path_to_extension)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(fullurl)
    soup = BeautifulSoup(driver.page_source,'lxml')
    driver.quit()
    table = soup.find('table',{"class":"suppress_all sortable stats_table now_sortable"})
    for td in table.find_all("tr")[2].find_all('td'):
        roof = td.get_text(strip=True)
    if roof in ['dome','retractable roof (closed)','retractable roof (open)']:
        temp = 70
        wind = 0
        for td in table.find_all("tr")[3].find_all('td'):
            surface = td.get_text(strip=True)
        for td in table.find_all("tr")[4].find_all('td'):
            spread = td.get_text(strip=True)
        for td in table.find_all("tr")[5].find_all('td'):
            ou = td.get_text(strip=True)

    elif roof in ['outdoors']:
        for td in table.find_all("tr")[3].find_all('td'):
            surface = td.get_text(strip=True)
        for td in table.find_all("tr")[4].find_all('td'):
            text = td.get_text(strip=True)
            temp = text.split(" degrees",1)[0]
            try :
                wind = text.split(", wind ",2)[1][:2]
            except:
                wind = 0
                temp = 70
                for td in table.find_all("tr")[4].find_all('td'):
                    spread = td.get_text(strip=True)
                for td in table.find_all("tr")[5].find_all('td'):
                    ou = td.get_text(strip=True)

        for td in table.find_all("tr")[5].find_all('td'):
            spread = td.get_text(strip=True)
        try:
            for td in table.find_all("tr")[6].find_all('td'):
                ou = td.get_text(strip=True)
        except:
            temp = 70
            wind = 0
            for td in table.find_all("tr")[4].find_all('td'):
                spread = td.get_text(strip=True)
            for td in table.find_all("tr")[5].find_all('td'):
                ou = td.get_text(strip=True)
    else:
        for td in table.find_all("tr")[3].find_all('td'):
            roof = td.get_text(strip=True)
        if roof in ['dome','retractable roof (closed)','retractable roof (open)']:
            temp = 70
            wind = 0
            for td in table.find_all("tr")[4].find_all('td'):
                surface = td.get_text(strip=True)
            for td in table.find_all("tr")[5].find_all('td'):
                spread = td.get_text(strip=True)
            for td in table.find_all("tr")[6].find_all('td'):
                ou = td.get_text(strip=True)
        else:
            for td in table.find_all("tr")[4].find_all('td'):
                surface = td.get_text(strip=True)
            for td in table.find_all("tr")[5].find_all('td'):
                text = td.get_text(strip=True)
                temp = text.split(" degrees",1)[0]
                try :
                    wind = text.split(", wind ",2)[1][:2]
                except:
                    wind = 0

            for td in table.find_all("tr")[6].find_all('td'):
                spread = td.get_text(strip=True)
            for td in table.find_all("tr")[7].find_all('td'):
                ou = td.get_text(strip=True)

    record = [year, awaytm, hometm, roof, surface, temp, wind, spread, ou]
    df1 = df1.append(pd.DataFrame([record], columns = columns), ignore_index = True)
    df1.to_csv('/Users/User1/ml-seed-data/2018spreads.csv', sep='|')
