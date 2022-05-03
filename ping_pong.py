'''
Ping Pong Score Processor
'''

import os

import pandas as pd

from score_processor import *


SHEETS = [
    '2020 League Games',
    '2021 League Games',
    '2022 League Games',
]


def load_scores():
    scores = []
    for sheet in SHEETS:
        season_scores = pd.read_excel('scores/scores.xlsx', sheet)

        season = sheet.split()[0]
        season_scores['season'] = [season]*season_scores.shape[0]

        scores.append(season_scores)
 
    scores = pd.concat(scores)
    
    scores.columns = ['idx', 'date', 'location', 'table', 'winner', 'winner_score', 'loser', 'loser_score', 'season']
    del scores['idx']

    scores = scores.dropna()

    return scores

def save_results(dataframes, sheet_names):
    filepath = os.path.join('results', 'processed_scores.xlsx')

    writer = pd.ExcelWriter(filepath, engine='xlsxwriter')
    for df, sheet in zip(dataframes, sheet_names):
        df.to_excel(writer, sheet_name=sheet, index=False)

    writer.save()


if __name__ == '__main__':
    print('PROCESSING SCORES: IN PROGRESS\n')

    scores = load_scores()
    games_by_player = segment_games_by_player(scores)

    print('---------------------- OVERALL PERFORMANCE ----------------------\n')
    overall_performance = compute_overall_performance(games_by_player)
    print(f'{overall_performance}\n')

    print('---------------------- PERFORMANCE BY SEASON --------------------\n')
    seasons = [sheet.split()[0] for sheet in SHEETS]
    performances_by_season = compute_season_by_season_performance(games_by_player, seasons)

    for i, season in enumerate(seasons):
        print(f'\t\t\t{season} SEASON\n')
        print(f'{performances_by_season[i]}\n')
    
    print('---------------------- HEAD TO HEAD PERFORMANCE -----------------\n')
    head_to_heads = compute_head_to_head_overall_performance(games_by_player)

    for head_to_head in head_to_heads:
        print(f'{head_to_head}\n')

    print('---------------------- SAVING RESULTS ---------------------------\n')

    results = [overall_performance]
    results.extend(performances_by_season)
    results.extend(head_to_heads)

    sheet_names = ['overall_performance']
    sheet_names.extend(seasons)
    sheet_names.extend(games_by_player.keys())

    save_results(results, sheet_names)

    print('PROCESSING SCORES: COMPLETE')