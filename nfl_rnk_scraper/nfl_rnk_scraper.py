import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from datetime import timedelta
import time

def date_run(url, site):
    week_num = 1
    date = startdate[1]
    columns = ['week', 'year', 'team', site+'_currseason', site+'_last3', site+'_last1', site+'_home', site+'_away', site+'_lastseason']
    df1 = pd.DataFrame(columns = columns)

    while date < enddate[1]:
        page = requests.get(url + str(site) + '?' + date + '&date=' + date)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find('table',{"class":"tr-table datatable scrollable"})
        year = '2013'
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

catoff = ['points-per-game','red-zone-scoring-attempts-per-game','red-zone-scoring-pct',
'two-point-conversion-attempts-per-game','two-point-conversions-per-game',
'yards-per-game','plays-per-game','fourth-downs-per-game',
'fourth-down-conversion-pct', 'giveaways-per-game', 'penalties-per-game',
'penalty-yards-per-game']

catdef = ['opponent-points-per-game','opponent-red-zone-scoring-attempts-per-game','opponent-red-zone-scoring-pct',
'opponent-two-point-conversion-attempts-per-game','opponent-two-point-conversions-per-game',
'opponent-yards-per-game','opponent-plays-per-game','opponent-fourth-downs-per-game',
'opponent-fourth-down-conversion-pct', 'takeaways-per-game', 'penalties-per-game',
'penalty-yards-per-game']

startdate = ['2012-09-04','2013-09-04','2014-09-03','2015-09-09','2016-09-08','2017-09-06']

enddate = ['2012-12-30','2013-12-29','2014-12-28','2016-01-03','2017-01-01','2017-12-31']

df = pd.read_csv('/Users/User1/ml-seed-data/schedule.csv',header=0)
df2 = pd.read_csv('/Users/User1/ml-seed-data/fga.csv',header=0)
df = pd.merge(df, df2, on=['week','year','team'])
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

df.to_csv('/Users/User1/ml-seed-data/' + year + '.csv', sep='|')
