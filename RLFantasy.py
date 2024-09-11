import csv
import os

# File paths
user_csv = 'users.csv'
players_csv = 'players.csv'
leagues_csv = 'leagues.csv'
teams_csv = 'teams.csv'

# Initialize necessary CSV files if they don't exist
def initialize_csv():
    if not os.path.exists(user_csv):
        with open(user_csv, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['username', 'password', 'role'])  # 'role' can be 'admin' or 'user'
            writer.writerow(['admin', 'admin123', 'admin'])  # Default admin account

    if not os.path.exists(players_csv):
        with open(players_csv, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['player_name'])  # List of available players
    
    if not os.path.exists(leagues_csv):
        with open(leagues_csv, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['league_code', 'league_name', 'admin'])

    if not os.path.exists(teams_csv):
        with open(teams_csv, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['username', 'league_code', 'team_name', 'players'])  # Players will be a comma-separated list

# User sign up
def sign_up():
    username = input("Enter new username: ")
    password = input("Enter new password: ")
    
    with open(user_csv, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password, 'user'])  # New users are regular users by default
    
    print("Sign up successful! You can now log in.")

# Log in existing user
def log_in():
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    with open(user_csv, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if row[0] == username and row[1] == password:
                print("Login successful!")
                return row  # Return user info: [username, password, role]
    print("Login unsuccessful. Please try again.")
    return None

# Admin functionality: Create fantasy league
def create_league(admin_username):
    league_name = input("Enter league name: ")
    league_code = input("Enter unique league code: ")
    
    with open(leagues_csv, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([league_code, league_name, admin_username])
    
    print(f"League '{league_name}' created with code '{league_code}'.")

# User functionality: Join league
def join_league(username):
    league_code = input("Enter league code to join: ")
    team_name = input("Enter your team name: ")
    
    with open(leagues_csv, 'r') as leagues_file:
        leagues = list(csv.reader(leagues_file))
    
    if not any(league_code == row[0] for row in leagues):
        print("League not found.")
        return
    
    # Add user to league with their team
    with open(teams_csv, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, league_code, team_name, ''])  # Empty team initially
    
    print(f"Joined league '{league_code}' with team '{team_name}'.")

# Manage teams: Add/Remove players to/from the team
def manage_team(username, league_code):
    team_found = False
    with open(teams_csv, 'r') as file:
        teams = list(csv.reader(file))
    
    for row in teams:
        if row[0] == username and row[1] == league_code:
            team_found = True
            current_players = row[3].split(',') if row[3] else []
            break
    
    if not team_found:
        print("You are not in this league.")
        return
    
    while True:
        print(f"\nYour current team: {current_players}")
        print("1. Add player")
        print("2. Remove player")
        print("3. Exit team management")
        choice = input("Enter choice: ")
        
        if choice == '1':
            add_player_to_team(username, league_code, current_players)
        elif choice == '2':
            remove_player_from_team(username, league_code, current_players)
        elif choice == '3':
            break
        else:
            print("Invalid choice.")

def add_player_to_team(username, league_code, current_players):
    player_name = input("Enter player name to add: ")
    
    # Check if the player is available
    with open(players_csv, 'r') as file:
        players = [row[0] for row in csv.reader(file)]
    
    if player_name not in players:
        print("Player not found in available players.")
        return
    
    # Ensure the player isn't already on any team in the league
    with open(teams_csv, 'r') as file:
        teams = csv.reader(file)
        for row in teams:
            if row[1] == league_code and player_name in row[3]:
                print("Player is already taken in this league.")
                return
    
    current_players.append(player_name)
    
    # Update the team
    update_team_in_csv(username, league_code, current_players)
    print(f"Added {player_name} to your team.")

def remove_player_from_team(username, league_code, current_players):
    player_name = input("Enter player name to remove: ")
    
    if player_name not in current_players:
        print("Player not found in your team.")
        return
    
    current_players.remove(player_name)
    
    # Update the team
    update_team_in_csv(username, league_code, current_players)
    print(f"Removed {player_name} from your team.")

# Helper function to update the team in the CSV
def update_team_in_csv(username, league_code, current_players):
    with open(teams_csv, 'r') as file:
        teams = list(csv.reader(file))
    
    for row in teams:
        if row[0] == username and row[1] == league_code:
            row[3] = ','.join(current_players)  # Update the player list
    
    with open(teams_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(teams)

# Main program loop
def main():
    initialize_csv()
    
    user = None
    while not user:
        print("\nMenu:")
        print("1. Log In")
        print("2. Sign Up")
        print("q. Quit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            user = log_in()
        elif choice == '2':
            sign_up()
        elif choice == 'q':
            print("Goodbye!")
            return
        else:
            print("Invalid choice.")
    
    username, _, role = user
    
    # After logging in, check user role
    if role == 'admin':
        while True:
            print(f"\nWelcome Admin: {username}")
            print("1. Create Fantasy League")
            print("2. Manage Teams")
            print("q. Log out")
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                create_league(username)
            elif choice == '2':
                league_code = input("Enter league code to manage: ")
                manage_team(username, league_code)
            elif choice == 'q':
                print("Logged out.")
                break
            else:
                print("Invalid choice.")
    else:
        while True:
            print(f"\nWelcome User: {username}")
            print("1. Join League")
            print("2. Manage Your Team")
            print("q. Log out")
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                join_league(username)
            elif choice == '2':
                league_code = input("Enter league code: ")
                manage_team(username, league_code)
            elif choice == 'q':
                print("Logged out.")
                break
            else:
                print("Invalid choice.")

if __name__ == "__main__":
    main()
