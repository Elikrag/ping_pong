'''
Ping Pong Score Processor
'''

import os

import pandas as pd


SHEETS = [
    '2020 League Games',
    '2021 League Games',
    '2022 League Games',
]


def load_scores():
    scores = pd.read_excel('scores/scores.xlsx', 'League Games - June 2021')
    
    scores.columns = ['idx', 'date', 'location', 'table', 'winner', 'winner_score', 'loser', 'loser_score']
    del scores['idx']

    scores = scores.dropna(how='all')

    return scores

def save_results(data, name):
    filepath = os.path.join('results', f'{name}.xlsx')
    data.to_excel(filepath, sheet_name=name, index=False)


if __name__ == '__main__':
    scores = load_scores()
    games_by_player = segment_games_by_player(scores)

    overall_performance = compute_overall_performance(games_by_player)

    #average points for per game against opponent x
    #average points against per game against opponent x
    #win % against opponent x

    save_results(overall_performance, 'overall_performance')