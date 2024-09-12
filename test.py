from models import Player, Team, League, Draft

available_players = [Player(i, f'Linke{i}') for i in range(16)]
teams = [Team(0, 'Turbos Cheeks'), Team(1, 'Jizzo')]
league = League(teams=teams)

draft = Draft(league, available_players)
draft.start()

for team in teams:
    print(team)
    for player in team.players:
        print(player)
    print()