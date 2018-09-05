import requests
from bs4 import BeautifulSoup,SoupStrainer
import urllib.request
from selenium import webdriver
import pandas as pd

columns = ['year', 'awaytm', 'hometm', 'spread', 'ou']
df1 = pd.DataFrame(columns = columns)

page = urllib.request.urlopen("https://www.pro-football-reference.com/years/2012/games.htm")
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
    year = '2012'
    driver = webdriver.Chrome()
    driver.get(fullurl)
    soup = BeautifulSoup(driver.page_source,'lxml')
    driver.quit()
    table = soup.find('table',{"class":"suppress_all sortable stats_table now_sortable"})
    i = 1
    while i < 7:
        try:
            test = table.find_all("tr")[i].find_all('th')
        except:
            i = 8
        else:
            for th in table.find_all("tr")[i].find_all('th'):
                if th.get_text(strip=True) == 'Vegas Line':
                    for td in table.find_all("tr")[i].find_all('td'):
                        spread = td.get_text(strip=True)

                    for td in table.find_all("tr")[i+1].find_all('td'):
                        ou = td.get_text(strip=True)
                        i = 8
                else:
                    i = i + 1

    record = [year, awaytm, hometm, spread, ou]
    df1 = df1.append(pd.DataFrame([record], columns = columns), ignore_index = True)

df.to_csv('/Users/s_garlick10/seed-data/2012spreads.csv', sep='|')
