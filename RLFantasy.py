import csv
import os

# File to store the user data
csv_file = 'users.csv'

# Function to check if the CSV file exists, if not create it
def initialize_csv():
    if not os.path.exists(csv_file):
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['username', 'password'])

# Function to sign up a new user
def sign_up():
    username = input("Enter new username: ")
    password = input("Enter new password: ")
    
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password])
    
    print("Sign up successful! You can now log in.")

# Function to log in an existing user
def log_in():
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if row[0] == username and row[1] == password:
                print("Login successful!")
                return True
    print("Login unsuccessful. Please try again.")
    return False

# Main loop of the program
def main():
    initialize_csv()
    
    while True:
        print("\nMenu:")
        print("1. Log In")
        print("2. Sign Up")
        print("q. Quit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            log_in()
        elif choice == '2':
            sign_up()
        elif choice == 'q':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()