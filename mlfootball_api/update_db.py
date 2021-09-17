import pandas as pd
import numpy as np
import requests

from datetime import datetime


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
    leagues = ['E0', 'E1', 'D1', 'D2', 'I1', 'I2', 'F1', 'N1', 'SP1', 'P1', 'SP2']
    now = datetime.now().strftime('%y')
    season_now = f'{now}{int(now)+1}'
    df_fd = pd.DataFrame()
    for league in leagues:
        source_fd = FootballData(season=season_now, league=league)
        df_temp = source_fd.download(date_column='Date', date_parser=date_parser, usecols=columns)
        df_fd = pd.concat([df_fd, df_temp], ignore_index=True)

    # Rename team names for merging
    df_mapping = pd.read_csv('mapping.csv')
    mapping = df_mapping.set_index('replace').to_dict()['replace_with']
    df_fd.replace(mapping, inplace=True)
    
    # Merge dataframes
    lkeys = ['date', 'team1', 'team2']
    rkeys = ['Date', 'HomeTeam', 'AwayTeam']
    df = pd.merge(df_fte, df_fd, how='left', left_on=lkeys, right_on=rkeys)

    r = requests.get(url='http://127.0.0.1:8000/api/lastupdate')
    last_db_updated = r.json()['last_updated']

    df = df[df['date'] > last_db_updated]
    print(df.head(10))






