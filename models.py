from typing import List
import numpy as np
import random


class Player:
    def __init__(self, id: str, name: str, shots: List[int] = [], goals: List[int] = [], assists: List[int] = [], saves: List[int] = [], score: List[int] = []):
        self.id = id
        self.name = name
        self.shots = shots
        self.goals = goals
        self.assists = assists
        self.saves = saves
        self.score = score

    def add_stats(self, average_core: dict) -> None:
        self.shots.append(average_core['shots'])
        self.goals.append(average_core['goals'])
        self.assists.append(average_core['assists'])
        self.saves.append(average_core['saves'])
        self.score.append(average_core['score'])

    def get_week(self, week: int) -> dict:
        return {
            'shots': self.shots[week],
            'goals': self.goals[week],
            'assists': self.assists[week],
            'saves': self.saves[week],
            'score': self.score[week]
        }

    def get_average_stats(self) -> dict:
        average_stats = {
            'id': self.id,
            'name': self.name,
            'shots': np.mean(self.shots),
            'goals': np.mean(self.goals),
            'assists': np.mean(self.assists),
            'saves': np.mean(self.saves),
            'game_score': np.mean(self.score),
        }
        average_stats['fantasy_score'] = self.calculate_fantasy_score(average_stats)

        return average_stats
    
    def calculate_fantasy_score(self, stats: dict, position: str = '') -> float:
        POSITION_MULTIPLIER = 1.5
        FANTASY_POINTS = {
            'goals': 50,
            'assists': 25,
            'saves': 25,
            'shots': 15,
            'game_score': 1
        }

        total_score = 0
        for stat, value in FANTASY_POINTS.items():
            if position == 'striker' and stat == 'goals':
                total_score += value * stats[stat] * POSITION_MULTIPLIER
            elif position == 'midfielder' and stat == 'assists':
                total_score += value * stats[stat] * POSITION_MULTIPLIER
            elif position == 'goalie' and stat == 'saves':
                total_score += value * stats[stat] * POSITION_MULTIPLIER
            else:
                total_score += value * stats[stat]
        return total_score

    def __str__(self) -> str:
        return self.name
    
    def __dict__(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'shots': self.shots,
            'goals': self.goals,
            'assists': self.assists,
            'saves': self.saves,
            'score': self.score
        }


class Team:
    def __init__(self, player_id: str, team_name: str):
        self.team_id = int(random.random() * 100000)
        self.player_id = player_id
        self.team_name = team_name
        self.players = []

        random.shuffle

    def load_team(self, players: List[Player]) -> None:
        self.players = players

    def add_player(self, player: Player) -> None:
        self.players.append(player)

    def remove_player(self, player: Player) -> None:
        if player not in self.players:
            return
        else:
            self.players.remove(player)

    def __str__(self) -> str:
        return self.team_name


class League:
    def __init__(self, teams: List[Team] = []):
        self.league_id = int(random.random() * 100000)
        self.teams = teams

    def add_team(self, team: Team) -> None:
        self.teams.append(team)

    def shuffle_teams(self) -> None:
        random.shuffle(self.teams)


class Draft:
    def __init__(self, league: League, available_players: List[Player]):
        self.draft_id = int(random.random() * 100000)
        self.league = league
        self.available_players = available_players

    def start(self, random_seeding: bool = True, snake: bool = True) -> None:
        ROUNDS = 7

        if random_seeding:
            self.league.shuffle_teams()

        for round in range(ROUNDS):
            for team in (self.league.teams if round % 2 == 0 or not snake else self.league.teams[::-1]):
                # Display who is currently drafting
                print(f'ROUND {round + 1}: {team}')

                # Display available players
                for i, player in enumerate(self.available_players):
                    print(f'[{i}] {player}')

                # Have user select player from available players
                user_selection = int(input("RLFantasy> "))
                while user_selection >= self.available_players.__len__() or user_selection < 0:
                    user_selection = int(input("RLFantasy> "))

                # Add player to players team
                team.add_player(self.available_players[user_selection])
                # Remove player from available players
                self.available_players.pop(user_selection)
