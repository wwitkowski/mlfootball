import pandas as pd
import numpy as np
import requests
import json

from datetime import datetime
from ml_models import FootballPoissonModel


class Source:
    def __init__(self, link) -> None:
        self.link = link
        
    def download(self, date_column, date_parser=None, usecols=None):
        df = pd.read_csv(self.link, parse_dates=[date_column], date_parser=date_parser, usecols=usecols)
        return df


class FiveThirtyEight(Source):
    link = 'https://projects.fivethirtyeight.com/soccer-api/club/spi_matches.csv'
    
    def __init__(self) -> None:
        super().__init__(self.link)


class FootballData(Source):
    def __init__(self, season, league) -> None:
        self.link = f'http://www.football-data.co.uk/mmz4281/{season}/{league}.csv'
        super().__init__(self.link)


class Stats():
    def __init__(self, data):
        self.data = data

    @staticmethod
    def points(row):
        if row == 'D':
            return 1, 1
        elif row == 'H':
            return 3, 0
        else:
            return 0, 3

    def add_stats(self):	
        # Add nonshot and shot expected goals average
        self.data['avg_xg1'] = (self.data['xg1'] + self.data['nsxg1']) / 2
        self.data['avg_xg2'] = (self.data['xg2'] + self.data['nsxg2']) / 2
        self.data['adj_avg_xg1'] = (self.data['xg1'] + self.data['nsxg1'] + self.data['adj_score1']) / 3
        self.data['adj_avg_xg2'] = (self.data['xg2'] + self.data['nsxg2'] + self.data['adj_score2']) / 3       
        # Add points
        self.data['pts1'], self.data['pts2'] = zip(*self.data.apply(lambda row: self.points(row.FTR), axis=1))
        # Add expected points based on expected goals
        p = FootballPoissonModel()
        self.data[['xg1', 'xg2']] = self.data[['xg1', 'xg2']].fillna(value=0)
        h, d, a = p.predict_chances(self.data.xg1.values, self.data.xg2.values)
        self.data['xwin1'], self.data['xdraw'], self.data['xwin2'] = h, d, a
        self.data['xpts1'] = 3 * self.data['xwin1'] + self.data['xdraw']
        self.data['xpts2'] = 3 * self.data['xwin2'] + self.data['xdraw']
        self.data['xgshot1'] = self.data['xg1'] / self.data['shots1']
        self.data.xgshot1.replace([np.inf, -np.inf], 0, inplace=True)
        self.data['xgshot2'] = self.data['xg2'] / self.data['shots2']
        self.data.xgshot2.replace([np.inf, -np.inf], 0, inplace=True)
        self.data['convrate1'] = self.data['score1'] / self.data['shots1']
        self.data.convrate1.fillna(0, inplace=True)
        self.data['convrate2'] = self.data['score2'] / self.data['shots2']
        self.data.convrate2.fillna(0, inplace=True)
        self.data['cards1'] = self.data['yellow1'] + 2 * self.data['red1']
        self.data['cards2'] = self.data['yellow2'] + 2 * self.data['red2']
        self.data['datetime'] = pd.to_datetime(self.data['date'])
        data_temp = pd.concat([self.data[['season', 'datetime', 'league', 'team1']], 
            self.data[['season', 'datetime', 'league', 'team2']].rename(columns={'team2': 'team1'})]).sort_values(by=['season', 'datetime'])
        data_temp['matchday'] = data_temp.groupby(['season', 'league', 'team1'])['datetime'].rank(method='first')
        self.data = self.data.merge(data_temp, left_on=['datetime', 'league',  'team1'],  right_on=['datetime', 'league',  'team1'], how='left', suffixes=('', '_home'))
        self.data = self.data.merge(data_temp, left_on=['datetime', 'league',  'team2'],  right_on=['datetime', 'league',  'team1'], how='left', suffixes=('', '_away'))
        self.data.drop(['datetime', 'season_home', 'season_away', 'team1_away'], axis=1, inplace=True)

        return self.data

        

if __name__ == '__main__':
    # Download FiveThirtyEight csv
    source_fte = FiveThirtyEight()
    df_fte = source_fte.download(date_column='date')
    
    # Download FootballData csvs and concatenate
    date_parser = lambda x: datetime.strptime(x, '%d/%m/%Y')
    columns = [
        'Date', 'HomeTeam', 'AwayTeam', 'FTR', 'HS', 'AS', 'HST', 'AST', 
		'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'MaxH', 'MaxD',
        'MaxA', 'AvgH', 'AvgD', 'AvgA', 'Max>2.5', 'Max<2.5', 'Avg>2.5', 'Avg<2.5']
    rename_dict = {
        'BbMxH': 'MaxH', 'BbMxD': 'MaxD', 'BbMxA': 'MaxA', 'BbAvH': 'AvgH', 'BbAvD': 'AvgD', 'BbAvA': 'AvgA',
        'HS': 'shots1', 'AS': 'shots2', 'HST': 'shotsot1', 'AST': 'shotsot2', 'HF': 'fouls1', 'AF': 'fouls2', 
        'HC': 'corners1', 'AC': 'corners2', 'HY': 'yellow1', 'AY': 'yellow2', 'HR': 'red1', 'AR': 'red2',
        'Max>2.5': 'maxover', 'Max<2.5': 'maxunder', 'Avg>2.5': 'avgover', 'Avg<2.5': 'avgunder'}
    leagues = ['E0', 'E1', 'D1', 'D2', 'I1', 'I2', 'F1', 'N1', 'SP1', 'P1', 'SP2']
    now = datetime.now().strftime('%y')
    season_now = f'{now}{int(now)+1}'
    df_fd = pd.DataFrame()
    for league in leagues:
        source_fd = FootballData(season=season_now, league=league)
        df_temp = source_fd.download(date_column='Date', date_parser=date_parser, usecols=columns)
        df_temp.rename(columns=rename_dict, inplace=True)
        df_fd = pd.concat([df_fd, df_temp], ignore_index=True)

    # Rename team names for merging
    df_mapping = pd.read_csv('mapping.csv')
    mapping = df_mapping.set_index('replace').to_dict()['replace_with']
    df_fd.replace(mapping, inplace=True)
    
    # Merge dataframes
    lkeys = ['date', 'team1', 'team2']
    rkeys = ['Date', 'HomeTeam', 'AwayTeam']
    df_update = pd.merge(df_fte, df_fd, how='left', left_on=lkeys, right_on=rkeys)
    print(df_update['FTR'].isnull().sum())

    # Get last db update date
    r = requests.get(url='http://127.0.0.1:8000/api/lastupdate')
    last_db_updated = r.json()['last_updated']
    print(f'Lastest updated scores found on {last_db_updated}.')

    # df_update = pd.read_csv('update.csv')
    # Add stats
    stats = Stats(df_update)
    df_update = stats.add_stats()
    df_update.drop(rkeys, axis=1, inplace=True)

    # Filter downloaded data
    df_update = df_update[df_update['date'] > last_db_updated]
    df_update['date'] = df_update['date'].dt.strftime('%Y-%m-%d')
    columns = {
        'matchday': 'matchday_home',
        'FTR': 'ftr',
        'MaxH': 'maxh', 
        'MaxD': 'maxd',
        'MaxA': 'maxa', 
        'AvgH': 'avgh', 
        'AvgD': 'avgd', 
        'AvgA': 'avga'
    }
    df_update.rename(columns=columns, inplace=True)
    
    # Delete old rows
    del_r = requests.delete(url=f'http://127.0.0.1:8000/api/matches/{last_db_updated}/')
    deleted_count = del_r.json()['count']
    print(f'Deleted {deleted_count} rows. Updating with {df_update.shape[0]} new rows.')

    # Upload updated
    data = df_update.to_json(orient="records")
    data_parsed = json.loads(data)
    uptd_r = requests.post(url='http://127.0.0.1:8000/api/matches/', json=data_parsed)
    print(uptd_r.text)





