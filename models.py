from typing import List
import random


class Player:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    def __str__(self) -> str:
        return self.name


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
