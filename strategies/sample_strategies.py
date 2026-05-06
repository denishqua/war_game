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
