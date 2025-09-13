# A simple 2-player High Card game with an object-oriented structure
# that separates strategies into their own classes.

import random

class Player:
    """
    Represents a player in the High Card game.
    Each player has a name, a score, and a list of numbers.
    """
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.numbers = list(range(1, 14))

    def remove_number(self, number):
        """Removes a chosen number from the player's list."""
        if number in self.numbers:
            self.numbers.remove(number)
            return True
        return False

    def __str__(self):
        """String representation of the player."""
        return self.name

class Strategy:
    """
    Base class for all game strategies.
    Specific strategies must inherit from this class and implement the play method.
    """
    def __init__(self, name):
        self.name = name

    def play(self, player_numbers, opponent_numbers):
        """
        Determines which number to play based on the game state.
        This method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclass must implement abstract method 'play'")

class RandomStrategy(Strategy):
    """
    A strategy that plays a random available number.
    """
    def __init__(self):
        super().__init__("Random")

    def play(self, player_numbers, opponent_numbers):
        return random.choice(player_numbers)

class HighCardStrategy(Strategy):
    """
    A strategy that always plays the highest available number.
    """
    def __init__(self):
        super().__init__("High Card")

    def play(self, player_numbers, opponent_numbers):
        return max(player_numbers)

class LowCardStrategy(Strategy):
    """
    A strategy that always plays the lowest available number.
    """
    def __init__(self):
        super().__init__("Low Card")

    def play(self, player_numbers, opponent_numbers):
        return min(player_numbers)

class StrategicPlay(Strategy):
    """
    A strategy that considers the opponent's numbers.
    It plays the lowest number that can beat the opponent's highest,
    or its own lowest if it cannot win.
    """
    def __init__(self):
        super().__init__("Strategic Play")

    def play(self, player_numbers, opponent_numbers):
        if not opponent_numbers:
            return max(player_numbers)

        opponent_highest = max(opponent_numbers)
        winning_cards = [card for card in player_numbers if card > opponent_highest]
        
        if winning_cards:
            return min(winning_cards)
        else:
            return min(player_numbers)


class Game:
    """
    Orchestrates the High Card game.
    Manages game state, players, and turn logic.
    """
    def __init__(self):
        self.player = Player("You")
        self.computer = Player("Computer")
        self.total_turns = 13
        self.current_turn = 1
        self.computer_strategy = None
        
        self.strategies = {
            "1": RandomStrategy(),
            "2": HighCardStrategy(),
            "3": LowCardStrategy(),
            "4": StrategicPlay()
        }

    # --- Game Logic Functions ---
    def _select_strategy(self):
        """Prompts the user to select a strategy for the computer."""
        print("Choose a strategy for the computer opponent:")
        for key, strategy_obj in self.strategies.items():
            print(f"  ({key}) {strategy_obj.name}")

        while True:
            choice = input("Enter your choice (1, 2, 3, or 4): ")
            if choice in self.strategies:
                self.computer_strategy = self.strategies[choice]
                print(f"You have selected the {self.computer_strategy.name} strategy.")
                break
            else:
                print("Invalid choice. Please enter a number from the list.")

    def _select_simulation_strategies(self):
        """Prompts the user to select two strategies for the simulation."""
        print("Choose two strategies to face off:")
        for key, strategy_obj in self.strategies.items():
            print(f"  ({key}) {strategy_obj.name}")

        while True:
            choice1 = input("Enter choice for Player 1: ")
            if choice1 in self.strategies:
                break
            print("Invalid choice. Please enter a valid number.")

        while True:
            choice2 = input("Enter choice for Player 2: ")
            if choice2 in self.strategies:
                break
            print("Invalid choice. Please enter a valid number.")

        strategy1 = self.strategies[choice1]
        strategy2 = self.strategies[choice2]

        print(f"\nSimulating a game between {strategy1.name} and {strategy2.name}...")
        return strategy1, strategy2

    def _display_status(self, current_turn, player1, player2):
        """Displays the current scores and turn number for the simulation."""
        print(f"\n--- Turn {current_turn}/{self.total_turns} ---")
        print(f"{player1.name}'s Score: {player1.score}")
        print(f"{player2.name}'s Score: {player2.score}")
        print("-" * 25)

    def _get_player_choice(self):
        """Prompts the human player for a number and validates the input."""
        while True:
            try:
                print(f"Your available numbers are: {sorted(self.player.numbers)}")
                choice = int(input(f"Choose a number to play: "))
                if self.player.remove_number(choice):
                    return choice
                else:
                    print("Invalid number. Please choose a number from your list.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def _update_game_state(self, player1_choice, player2_choice, player1, player2):
        """Compares choices, updates scores, and removes the played numbers."""
        print(f"{player1.name} played: {player1_choice}")
        print(f"{player2.name} played: {player2_choice}")

        if player1_choice > player2_choice:
            player1.score += 1
            print(f"{player1.name} wins this turn!")
        elif player2_choice > player1_choice:
            player2.score += 1
            print(f"{player2.name} wins this turn!")
        else:
            print("It's a tie! No one gets a point.")

        player1.remove_number(player1_choice)
        player2.remove_number(player2_choice)

    def _end_game(self, player1, player2):
        """Declares the final winner and ends the game."""
        print("\n" + "=" * 25)
        print("           GAME OVER           ")
        print("=" * 25)
        print(f"\nFinal Scores:")
        print(f"{player1.name} Score: {player1.score}")
        print(f"{player2.name} Score: {player2.score}")

        if player1.score > player2.score:
            print(f"\n{player1.name} wins the game!")
        elif player2.score > player1.score:
            print(f"\n{player2.name} wins the game!")
        else:
            print("\nIt's a tie game!")

    def play(self):
        """Main function to run the human vs. computer game."""
        print("Welcome to High Card Game!")
        print("Play against the computer. The higher number wins the turn. Most wins after 13 turns takes the game!")
        
        self._select_strategy()

        for _ in range(self.total_turns):
            self._display_status(self.current_turn, self.player, self.computer)
            
            player_choice = self._get_player_choice()
            computer_choice = self.computer_strategy.play(self.computer.numbers, self.player.numbers)
            
            self._update_game_state(player_choice, computer_choice, self.player, self.computer)
            
            self.current_turn += 1
        
        self._end_game(self.player, self.computer)

    def simulate_game(self):
        """Runs a simulation of two strategies playing against each other."""
        strategy1, strategy2 = self._select_simulation_strategies()
        
        player1 = Player(strategy1.name)
        player2 = Player(strategy2.name)

        for turn in range(1, self.total_turns + 1):
            self._display_status(turn, player1, player2)

            player1_choice = strategy1.play(player1.numbers, player2.numbers)
            player2_choice = strategy2.play(player2.numbers, player1.numbers)

            self._update_game_state(player1_choice, player2_choice, player1, player2)

        self._end_game(player1, player2)

# --- Run the game ---
if __name__ == "__main__":
    game = Game()
    
    while True:
        print("\nWhat would you like to do?")
        print("  (1) Play a game against a computer opponent")
        print("  (2) Simulate a game between two strategies")
        choice = input("Enter your choice (1 or 2): ")

        if choice == "1":
            game.play()
            break
        elif choice == "2":
            game.simulate_game()
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")
