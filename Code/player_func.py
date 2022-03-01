import json

def initialize_user_db():
    """
    Initialize the user_database.json file if it doesn't exist. This is only 
    performed the first time the game is ever run, or if the user_database.json 
    file is deleted. It creates the json file containing an empty list.
    """
    filename = 'user_database.json'
    with open(filename, 'w', encoding='utf-8') as f:
            json.dump([], f, indent=2)
    get_player_name()

def get_player_name():
    """
    Prompt for user's name. If it exists in the JSON file, leave it unchanged &
    call the read_current_user function. Else, create a dictionary in the JSON 
    file for the user and call the current_user function to store them as the 
    current user.
    """
    filename = 'user_database.json'
       
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            users = json.load(f)
            username = input("What is your name: ") 
            for i in range(0, len(users)):
                if username.title() in users[i]:                      
                    write_current_user(username.title())
                    greet_player()    
                    return username.title()                      
            try:                
                with open(filename, 'w', encoding='utf-8') as f:
                    entry = {username.title(): {'High Score': None}}                    
                    users.append(entry)
                    json.dump(users, f, indent=2)                
                write_current_user(username.title())    
                greet_player()
                return username.title() 
            except FileNotFoundError:
                initialize_user_db()
    except FileNotFoundError:
        initialize_user_db()


def write_current_user(input):
    """
    Update the current_user.json file. This allows us to track who is currently
    playing, making it easy to do things like greet them, or access their 
    individual high score.
    """
    filename = 'current_user.json'

    with open(filename, 'w', encoding='utf-8') as f:            
        cu = {'Current User': input}
        current = []
        current.append(cu)
        json.dump(current, f, indent=2)
    return current

def read_current_user():
    """
    Get stored username from current_user.json. This method is used to access
    the current player after it is written by write_current_user().
    """
    filename = 'current_user.json'

    with open(filename, 'r', encoding='utf=8') as f:
        data = json.load(f)
        return data[0]["Current User"]

def update_score(input):
    """
    Function for updating scores in the JSON file. Input is the user's attempts.
    This reads the json file to find the specific player's score. If the current 
    score is lower than the recorded score, the json file is update. If the users
    score returns null, the score is set to default and then the actual score is
    recorded.
    """
    filename = 'user_database.json'
    player = read_current_user()
    current_score = input
    with open(filename, 'r', encoding='utf=8') as f:
        data = json.load(f)
    for i in range(0, len(data)):
        if player in data[i]:
            high_score = data[i][player]["High Score"]
            try:
                if current_score <  high_score:
                    data[i][player]["High Score"] = current_score
                    with open(filename, "w", encoding='utf-8') as f:
                        json.dump(data, f, indent=2)
                    print("Wow! That's a new high score!")
            except TypeError:
                if high_score == None:
                    high_score = 'default'
                    data[i][player]["High Score"] = current_score
                    with open(filename, "w", encoding='utf-8') as f:
                        json.dump(data, f, indent=2)

def display_all_high_scores():
    """
    Retrieve and display the user's current high score. This method loads the
    user database json file and prints each player's name and high score. Because
    the user data is a list of dictionaries, I first iterate over every index in 
    the list and then iterate through the dictionary in each index.
    """
    
    filename = 'user_database.json'

    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for i in range(0, len(data)):
        for player in data[i]:
            print(f"\nPlayer: {player}")
            print(f"  High Score: {data[i][player]['High Score']}")

            
    

        

                    
                
            

        


    










