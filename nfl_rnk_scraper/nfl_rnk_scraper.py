import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from datetime import timedelta
import time
import numpy as np

def date_run(url, site):
    week_num = 1
    date = startdate[7]
    columns = ['week', 'year', 'team', 'teams-opponent-' + site+'_currseason', 'teams-opponent-' + site+'_last3', 'teams-opponent-' + site+'_last1',
    'teams-opponent-' + site+'_home', 'teams-opponent-' + site+'_away', 'teams-opponent-' + site+'_lastseason']
    df1 = pd.DataFrame(columns = columns)

    while date < enddate[7]:
        page = requests.get(url + str(site) + '?' + date + '&date=' + date)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find('table',{"class":"tr-table datatable scrollable"})
        year = '2018'
        week = week_num

        for row in table.findAll('tr')[1:]:
            col = row.findAll('td')
            team = col[1].string
            currseason= col[2].string
            last3 = col[3].string
            last1 = col[4].string
            home = col[5].string
            away = col[6].string
            lastseason = col[7].string
            record = [week, year, team, currseason, last3, last1, home, away, lastseason]
            df1 = df1.append(pd.DataFrame([record], columns = columns), ignore_index = True)

        date = str(datetime.date(datetime.strptime(date, '%Y-%m-%d')) + timedelta(days=7))
        week_num = week_num + 1
    time.sleep(.3)
    time.sleep(4)

    return df1, year

##############################################################################

url = 'https://www.teamrankings.com/nfl/stat/'

#catoff = ['points-per-game','red-zone-scoring-attempts-per-game','red-zone-scoring-pct',
#'two-point-conversion-attempts-per-game','two-point-conversions-per-game',
#'yards-per-game','plays-per-game','fourth-downs-per-game',
#'fourth-down-conversion-pct', 'giveaways-per-game', 'penalties-per-game',
#'penalty-yards-per-game']

#catdef = ['opponent-points-per-game','opponent-red-zone-scoring-attempts-per-game','opponent-red-zone-scoring-pct',
#'opponent-two-point-conversion-attempts-per-game','opponent-two-point-conversions-per-game',
#'opponent-yards-per-game','opponent-plays-per-game','opponent-fourth-downs-per-game',
#'opponent-fourth-down-conversion-pct', 'takeaways-per-game', 'penalties-per-game',
#'penalty-yards-per-game']

#catoff = ['pass-attempts-per-game','rushing-attempts-per-game']
#catdef = ['opponent-pass-attempts-per-game','opponent-rushing-attempts-per-game']

#catoff = ['first-downs-per-game','third-downs-per-game','third-down-conversions-per-game']
#catdef = ['opponent-first-downs-per-game','opponent-third-downs-per-game','opponent-third-down-conversions-per-game']

catoff = ['opponent-points-per-game','opponent-red-zone-scoring-attempts-per-game','opponent-red-zone-scoring-pct',
'opponent-two-point-conversion-attempts-per-game','opponent-two-point-conversions-per-game',
'opponent-yards-per-game','opponent-plays-per-game','opponent-fourth-downs-per-game',
'opponent-fourth-down-conversion-pct', 'takeaways-per-game', 'penalties-per-game',
'penalty-yards-per-game']

catdef = ['points-per-game','red-zone-scoring-attempts-per-game','red-zone-scoring-pct',
'two-point-conversion-attempts-per-game','two-point-conversions-per-game',
'yards-per-game','plays-per-game','fourth-downs-per-game',
'fourth-down-conversion-pct', 'giveaways-per-game', 'penalties-per-game',
'penalty-yards-per-game']


startdate = ['2011-09-07','2012-09-04','2013-09-04','2014-09-03','2015-09-09','2016-09-07','2017-09-06','2018-09-05']

enddate = ['2012-01-01','2012-12-30','2013-12-29','2014-12-28','2016-01-03','2017-01-01','2017-12-31','2018-09-20']


df = pd.read_csv('/Users/s_garlick10/fantasy_football_ml/clean_data2.csv',header=0)

df[['week']] = df[['week']].astype('int')
df[['year']] = df[['year']].astype('int')
df[['team']] = df[['team']].astype('object')
df[['opponent']] = df[['opponent']].astype('object')

for site in catoff:
    df1, year = date_run(url, site)
    df1[['week']] = df1[['week']].astype('int')
    df1[['year']] = df1[['year']].astype('int')
    df1[['team']] = df1[['team']].astype('object')
    df = pd.merge(df, df1, on=['week','year','team'])

for site in catdef:
    df1, year = date_run(url, site)
    df1.columns.values[2] = 'opponent'
    df1[['week']] = df1[['week']].astype('int')
    df1[['year']] = df1[['year']].astype('int')
    df1[['opponent']] = df1[['opponent']].astype('object')
    df = pd.merge(df, df1, on=['week','year','opponent'])


df.to_csv('/Users/s_garlick10/fantasy_football_ml/' + str(year) + 'opponentstuff.csv', sep='|')
