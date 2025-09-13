from strategies.strategy import Strategy
import random

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
