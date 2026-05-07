import sys
import random

from strategies.strategy import Strategy
from strategies.sampleStrategies import (RandomStrategy, HighCardStrategy,
                                          LowCardStrategy, TopTwoRandomStrategy, BottomTwoRandomStrategy)
from strategies.aiGeneratedStrategies import GeminiStrategy1, StrategicPlay, RandomFirstStrategicPlay, HalfOneHalfTwoStrategicPlay

NUM_CARDS = 10

def get_all_strategies():
    """Registry of all available AI strategies."""
    return {
        "1": RandomStrategy(),
        "2": HighCardStrategy(),
        "3": LowCardStrategy(),
        "4": StrategicPlay(),
        "5": GeminiStrategy1(),
        "6": RandomFirstStrategicPlay(),
        "7": HalfOneHalfTwoStrategicPlay(),
        "8": TopTwoRandomStrategy(),
        "9": BottomTwoRandomStrategy()
    }

class HumanStrategy(Strategy):
    """A strategy that prompts a human player for input."""
    def __init__(self, player_obj):
        super().__init__("Human")
        self.player_obj = player_obj

    def play(self, player_numbers, opponent_numbers):
        while True:
            try:
                print(f"Your available numbers are: {sorted(self.player_obj.numbers)}")
                choice = int(input("Choose a number to play: "))
                if self.player_obj.remove_number(choice):
                    return choice
                else:
                    print("Invalid number. Please choose a number from your list.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

class Player:
    """
    Represents a player in the High Card game.
    """
    def __init__(self, name, num_cards=10):
        self.name = name
        self.score = 0
        self.numbers = list(range(1, num_cards + 1))
        self.played_numbers = []

    def remove_number(self, number):
        """Removes a chosen number from the player's list."""
        if number in self.numbers:
            self.numbers.remove(number)
            return True
        return False

    def __str__(self):
        return self.name

class Match:
    """
    Orchestrates a single High Card game match between two players using provided strategies.
    """
    def __init__(self, player1, player2, strategy1, strategy2, verbose=False, num_cards=10):
        self.player1 = player1
        self.player2 = player2
        self.strategy1 = strategy1
        self.strategy2 = strategy2
        self.verbose = verbose
        self.total_turns = num_cards

    def _display_status(self, current_turn):
        print(f"\n--- Turn {current_turn}/{self.total_turns} ---")
        print(f"{self.player1.name}'s Score: {self.player1.score}")
        print(f"{self.player2.name}'s Score: {self.player2.score}")
        print("-" * 25)

    def _update_game_state(self, p1_choice, p2_choice):
        if self.verbose:
            print(f"{self.player1.name} played: {p1_choice}")
            print(f"{self.player2.name} played: {p2_choice}")

        if p1_choice == 1 and p2_choice == self.total_turns:
            self.player1.score += 1
            if self.verbose: print(f"{self.player1.name} wins this turn! (1 beats {self.total_turns})")
        elif p2_choice == 1 and p1_choice == self.total_turns:
            self.player2.score += 1
            if self.verbose: print(f"{self.player2.name} wins this turn! (1 beats {self.total_turns})")
        elif p1_choice > p2_choice:
            self.player1.score += 1
            if self.verbose: print(f"{self.player1.name} wins this turn!")
        elif p2_choice > p1_choice:
            self.player2.score += 1
            if self.verbose: print(f"{self.player2.name} wins this turn!")
        else:
            self.player1.score += 0.5
            self.player2.score += 0.5
            if self.verbose: print("It's a tie! Each player gets 0.5 points.")

        self.player1.played_numbers.append(p1_choice)
        self.player2.played_numbers.append(p2_choice)
        # Note: remove_number is handled here for AI, but HumanStrategy handles it early.
        # We need to make sure HumanStrategy doesn't double-remove.
        # So instead, let the Match handle all removals.
        self.player1.remove_number(p1_choice)
        self.player2.remove_number(p2_choice)

    def play_match(self):
        """Runs the match and returns the result (1 for P1 win, 2 for P2 win, 0 for tie)."""
        for turn in range(1, self.total_turns + 1):
            if self.verbose:
                self._display_status(turn)
            
            p1_choice = self.strategy1.play(self.player1.numbers, self.player2.numbers)
            p2_choice = self.strategy2.play(self.player2.numbers, self.player1.numbers)
            
            self._update_game_state(p1_choice, p2_choice)

        return self._end_match()

    def _end_match(self):
        if self.verbose:
            print("\n" + "=" * 25)
            print("           GAME OVER           ")
            print("=" * 25)
            print(f"\nFinal Scores:")
            print(f"{self.player1.name} Score: {self.player1.score}")
            print(f"{self.player2.name} Score: {self.player2.score}")

        if self.player1.score > self.player2.score:
            if self.verbose: print(f"\n{self.player1.name} wins the game!")
            return 1
        elif self.player2.score > self.player1.score:
            if self.verbose: print(f"\n{self.player2.name} wins the game!")
            return 2
        else:
            if self.verbose: print("\nIt's a tie game!")
            return 0


class GameController:
    """
    Handles the Command Line Interface and Game Modes.
    """
    def __init__(self):
        self.strategies = get_all_strategies()

    def _select_strategy(self, prompt="Choose a strategy:"):
        print(prompt)
        for key, strategy_obj in self.strategies.items():
            print(f"  ({key}) {strategy_obj.name}")

        while True:
            choice = input("Enter your choice: ")
            if choice in self.strategies:
                return self.strategies[choice]
            print("Invalid choice. Please enter a number from the list.")

    def run_interactive_mode(self):
        print("Welcome to High Card Game!")
        print(f"Play against the computer. The higher number wins the turn (but 1 beats {NUM_CARDS}). Most wins after {NUM_CARDS} turn(s) takes the game!")
        
        computer_strategy = self._select_strategy("Choose a strategy for the computer opponent:")
        print(f"You have selected the {computer_strategy.name} strategy.")

        player1 = Player("You")
        player2 = Player("Computer")
        human_strategy = HumanStrategy(player1)

        match = Match(player1, player2, human_strategy, computer_strategy, verbose=True)
        match.play_match()

    def run_simulation_mode(self):
        try:
            num_games = int(input("How many games would you like to simulate? "))
        except ValueError:
            print("Invalid number, defaulting to 100 games.")
            num_games = 100
            
        verbose_input = input("Enable verbose output to see each turn? (y/n): ").strip().lower()
        verbose = (verbose_input == 'y')
        
        print("\nChoose two strategies to face off:")
        strat1 = self._select_strategy("Select Player 1:")
        strat2 = self._select_strategy("Select Player 2:")
        
        print(f"\nSimulating a game between {strat1.name} and {strat2.name}...")
        
        ties = 0
        player1_wins = 0 
        player2_wins = 0
        
        for _ in range(num_games):
            p1 = Player(strat1.name)
            p2 = Player(strat2.name)
            match = Match(p1, p2, strat1, strat2, verbose=verbose)
            result = match.play_match()
            
            if result == 1:
                player1_wins += 1
            elif result == 2:
                player2_wins += 1
            else:
                ties += 1
                
        print(f"\nResults after {num_games} games:")
        print(f"{strat1.name} wins: {player1_wins}")
        print(f"{strat2.name} wins: {player2_wins}")
        print(f"Ties: {ties}")

    def run_tournament_mode(self):
        random_strategy = self.strategies["1"]
        matchup_results = []
        num_games = 100000
        
        print(f"\nRunning tournament against Random... ({num_games} games per matchup)")
        
        for s1 in self.strategies.values():
            s1_wins = 0
            s2_wins = 0
            ties = 0
            
            for _ in range(num_games):
                p1 = Player(s1.name)
                p2 = Player(random_strategy.name)
                match = Match(p1, p2, s1, random_strategy, verbose=False)
                res = match.play_match()
                
                if res == 1:
                    s1_wins += 1
                elif res == 2:
                    s2_wins += 1
                else:
                    ties += 1
                    
            # For Random vs Random, make sure the higher win rate is displayed as s1_wins
            if s1.name == random_strategy.name and s2_wins > s1_wins:
                s1_wins, s2_wins = s2_wins, s1_wins
                    
            matchup_results.append((s1.name, random_strategy.name, s1_wins, s2_wins, ties))
            
        print("\nTournament Against Random Results:")
        print(f"{'Strategy':<25} | {'Wins vs Random':<15} | {'Losses':<8} | {'Ties':<6}")
        print("-" * 62)
        matchup_results.sort(key=lambda x: x[2], reverse=True)
        for p1, p2, w1, w2, t in matchup_results:
            print(f"{p1:<25} | {w1:<15} | {w2:<8} | {t:<6}")

    def run(self):
        while True:
            print("\nWhat would you like to do?")
            print("  (1) Play a game against a computer opponent")
            print("  (2) Simulate a matchup between two strategies")
            print("  (3) Evaluate all strategies against Random")
            choice = input("Enter your choice (1, 2, or 3): ")

            if choice == "1":
                self.run_interactive_mode()
                break
            elif choice == "2":
                self.run_simulation_mode()
                break
            elif choice == "3":
                self.run_tournament_mode()
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    controller = GameController()
    controller.run()
