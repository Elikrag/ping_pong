import pandas as pd
import numpy as np


IDX_MAP = {
    'date': 0,
    'location': 1,
    'table': 2,
    'winner': 3,
    'winner_score': 4,
    'loser': 5,
    'loser_score': 6,
    'season': 7
}


def segment_games_by_player(scores):
    games_by_player = {}

    winning_players = [name.lower() for name in scores.winner.unique()]
    losing_players = [name.lower() for name in scores.loser.unique()]
    players = np.unique(winning_players + losing_players)

    for player in players:
        player_games = []

        for i, date in enumerate(scores.date):
            if scores.iloc[i, IDX_MAP['winner']].lower() == player:
                player_games.append({
                    'player': player,
                    'date': date,
                    'season': scores.iloc[i, IDX_MAP['season']],
                    'player_score': scores.iloc[i, IDX_MAP['winner_score']],
                    'opponent_score': scores.iloc[i, IDX_MAP['loser_score']],
                    'win/loss': 'win',
                    'opponent': scores.iloc[i, IDX_MAP['loser']].lower()
                })

            elif scores.iloc[i, IDX_MAP['loser']].lower() == player:            
                player_games.append({
                    'player': player,
                    'date': date,
                    'season': scores.iloc[i, IDX_MAP['season']],
                    'player_score': scores.iloc[i, IDX_MAP['loser_score']],
                    'opponent_score': scores.iloc[i, IDX_MAP['winner_score']],
                    'win/loss': 'loss',
                    'opponent': scores.iloc[i, IDX_MAP['winner']].lower()
                })

        games_by_player[player] = pd.DataFrame(player_games, columns=['date', 'season', 'player', 'player_score', 'opponent_score', 'win/loss', 'opponent'])

    return games_by_player


def compute_overall_performance(games_by_player):
    overall_performance = []
    
    for player, games in games_by_player.items():
        win_loss_counts = games['win/loss'].value_counts()
        wins = win_loss_counts.get('win') if not win_loss_counts.get('win') == None else 0
        losses = win_loss_counts.get('loss') if not win_loss_counts.get('loss') == None else 0

        overall_performance.append({
            'player': player,
            'games_played': games.shape[0],
            'wins': wins,
            'losses': losses,
            'win %': round(wins/games.shape[0] * 100, 2),
            'avg_pfpg': round(games['player_score'].sum() / games.shape[0], 2),
            'avg_papg': round(games['opponent_score'].sum() / games.shape[0], 2)
        })

    overall_performance = pd.DataFrame(overall_performance, columns=['player', 'games_played', 'wins', 'losses', 'win %', 'avg_pfpg', 'avg_papg'])

    overall_performance = overall_performance.sort_values(by='win %', ascending=False)

    return overall_performance


def compute_season_by_season_performance(games_by_player, seasons):
    performance_by_season = {season: [] for season in seasons}

    for season in seasons: 
        for player, games in games_by_player.items():
            season_games = games.loc[games['season'] == season]

            if season_games.empty:
                continue

            win_loss_counts = season_games['win/loss'].value_counts()
            wins = win_loss_counts.get('win') if not win_loss_counts.get('win') == None else 0
            losses = win_loss_counts.get('loss') if not win_loss_counts.get('loss') == None else 0

            performance_by_season[season].append({
                'player': player,
                'games_played': season_games.shape[0],
                'wins': wins,
                'losses': losses,
                'win %': round(wins/season_games.shape[0] * 100, 2),
                'avg_pfpg': round(season_games['player_score'].sum() / season_games.shape[0], 2),
                'avg_papg': round(season_games['opponent_score'].sum() / season_games.shape[0], 2)
            })

    performance_by_season_dfs = []
    for season, results in performance_by_season.items():
        season_performance =  pd.DataFrame(results, columns=['player', 'games_played', 'wins', 'losses', 'win %', 'avg_pfpg', 'avg_papg'])
        season_performance = season_performance.sort_values(by='win %', ascending=False)
        
        performance_by_season_dfs.append(season_performance)

    return performance_by_season_dfs