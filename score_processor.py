import pandas as pd
import numpy as np


def segment_games_by_player(scores):
    games_by_player = {}

    winning_players = [name.lower() for name in scores.winner.unique()]
    losing_players = [name.lower() for name in scores.loser.unique()]
    players = np.unique(winning_players + losing_players)

    for player in players:
        player_games = pd.DataFrame(columns=['date', 'player', 'player_score', 'opponent_score', 'win/loss', 'opponent'])

        for i, date in enumerate(scores.date):
            if scores.winner[i].lower() == player:
                player_games = player_games.append(
                    {
                        'player': player,
                        'date': date,
                        'player_score': scores.winner_score[i],
                        'opponent_score': scores.loser_score[i],
                        'win/loss': 'win',
                        'opponent': scores.loser[i].lower()
                    }, 
                    ignore_index=True
                )

            elif scores.loser[i].lower() == player:            
                player_games = player_games.append(
                    {
                        'player': player,
                        'date': date,
                        'player_score': scores.loser_score[i],
                        'opponent_score': scores.winner_score[i],
                        'win/loss': 'loss',
                        'opponent': scores.winner[i].lower()
                    }, 
                    ignore_index=True
                )

        games_by_player[player] = player_games

    return games_by_player


def compute_overall_performance(games_by_player):
    overall_performance = pd.DataFrame(columns=['player', 'games_played', 'wins', 'losses', 'win %', 'avg_pfpg', 'avg_papg'])

    for player, games in games_by_player.items():
        win_loss_counts = games['win/loss'].value_counts()
        wins = win_loss_counts.get('win') if not win_loss_counts.get('win') == None else 0
        losses = win_loss_counts.get('loss') if not win_loss_counts.get('loss') == None else 0

        overall_performance = overall_performance.append(
            {
                'player': player,
                'games_played': games.shape[0],
                'wins': wins,
                'losses': losses,
                'win %': round(wins/games.shape[0] * 100, 2),
                'avg_pfpg': round(games['player_score'].sum() / games.shape[0], 2),
                'avg_papg': round(games['opponent_score'].sum() / games.shape[0], 2)
            },
            ignore_index=True
        )

    overall_performance = overall_performance.sort_values(by='win %', ascending=False)

    print(overall_performance)

    return overall_performance
