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

class TopTwoRandomStrategy(Strategy):
    """
    Plays the highest available card with 50% probability,
    and the second highest available card with 50% probability.
    """
    def __init__(self):
        super().__init__("Top Two Random")

    def play(self, player_numbers, opponent_numbers):
        if len(player_numbers) == 1:
            return player_numbers[0]
        sorted_nums = sorted(player_numbers, reverse=True)
        return random.choice(sorted_nums[:2])

class BottomTwoRandomStrategy(Strategy):
    """
    Plays the lowest available card with 50% probability,
    and the second lowest available card with 50% probability.
    """
    def __init__(self):
        super().__init__("Bottom Two Random")

    def play(self, player_numbers, opponent_numbers):
        if len(player_numbers) == 1:
            return player_numbers[0]
        sorted_nums = sorted(player_numbers)
        return random.choice(sorted_nums[:2])
