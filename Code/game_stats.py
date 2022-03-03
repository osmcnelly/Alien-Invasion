import json

class GameStats:
    """Track Statistics for Alien Invansion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

        # Start Alien Invasion in an inactive state
        self.game_active = False

        # High score is accessed from the JSON file 
        # using the get_saved_high_score() method.
        self.high_score = self.get_saved_high_score()
    
    def get_saved_high_score(self):
        """Gets high score from file, if it exists."""
        try:
            with open('user_scores.json') as f:
                return json.load(f)
        except FileNotFoundError:
            return 0

    def _check_high_score(self):
        """
        Check if current score is higher than the saved high score and update 
        the JSON file if it is.
        """
        saved_high_score = self.get_saved_high_score()
        if self.high_score > saved_high_score:
            with open('user_scores.json', 'w', encoding='utf-8') as f:
                json.dump(self.high_score, f)

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    

