'''
Ping Pong Score Processor
'''

import os

import pandas as pd

from score_processor import segment_games_by_player, compute_overall_performance


SHEETS = [
    '2020 League Games',
    '2021 League Games',
    '2022 League Games',
]


def load_scores():
    scores = []
    for sheet in SHEETS:
        scores.append(pd.read_excel('scores/scores.xlsx', sheet))
 
    scores = pd.concat(scores)
    
    scores.columns = ['idx', 'date', 'location', 'table', 'winner', 'winner_score', 'loser', 'loser_score']
    del scores['idx']

    scores = scores.dropna()

    return scores

def save_results(data, name):
    filepath = os.path.join('results', f'{name}.xlsx')
    data.to_excel(filepath, sheet_name=name, index=False)


if __name__ == '__main__':
    print('PROCESSING SCORES: IN PROGRESS\n')

    scores = load_scores()
    games_by_player = segment_games_by_player(scores)

    overall_performance = compute_overall_performance(games_by_player)

    print('OVERALL PERFORMANCE\n')
    print(f'{overall_performance}\n')

    #TODO: performance by season

    #TODO: head to head performance:
    #   average points for per game against opponent x
    #   average points against per game against opponent x
    #   win % against opponent x

    save_results(overall_performance, 'overall_performance')

    print('PROCESSING SCORES: COMPLETE')