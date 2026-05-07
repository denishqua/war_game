from strategies.strategy import Strategy

class GeminiStrategy1(Strategy):
    """
    A strong mixed strategy that avoids predictability.
    It identifies 'guaranteed wins', uses 1 strategically to snipe the max card,
    and otherwise randomizes its play to remain unexploitable.
    """
    def __init__(self):
        super().__init__("Gemini Strategy 1")

    def play(self, player_numbers, opponent_numbers):
        import random
        try:
            from game import NUM_CARDS
        except ImportError:
            NUM_CARDS = 10 # Fallback
            
        opponent_highest = max(opponent_numbers) if opponent_numbers else 0
        winning_cards = [c for c in player_numbers if c > opponent_highest]
        
        if winning_cards:
            candidate = min(winning_cards)
            if candidate == NUM_CARDS and 1 in opponent_numbers:
                pass # Not a guaranteed win
            else:
                return candidate

        if 1 in player_numbers and NUM_CARDS in opponent_numbers:
            if random.random() < 0.3:
                return 1

        if NUM_CARDS in player_numbers and 1 in opponent_numbers:
            available = [c for c in player_numbers if c != NUM_CARDS]
            if available:
                return random.choice(available)

        return random.choice(player_numbers)

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

class RandomFirstStrategicPlay(Strategy):
    """
    Same as Strategic Play, but plays a random card on the very first turn
    to add unpredictability.
    """
    def __init__(self):
        super().__init__("Random First Strategic")

    def play(self, player_numbers, opponent_numbers):
        import random
        try:
            from game import NUM_CARDS
        except ImportError:
            NUM_CARDS = 10
            
        if len(player_numbers) == NUM_CARDS:
            return random.choice(player_numbers)
            
        if not opponent_numbers:
            return max(player_numbers)

        opponent_highest = max(opponent_numbers)
        winning_cards = [card for card in player_numbers if card > opponent_highest]
        
        if winning_cards:
            return min(winning_cards)
        else:
            return min(player_numbers)

class HalfOneHalfTwoStrategicPlay(Strategy):
    """
    On the first turn, it plays 1 50% of the time and 2 the other 50%.
    Afterwards, it plays the same as Strategic Play.
    """
    def __init__(self):
        super().__init__("Half 1 Half 2 Strategic")

    def play(self, player_numbers, opponent_numbers):
        import random
        try:
            from game import NUM_CARDS
        except ImportError:
            NUM_CARDS = 10
            
        if len(player_numbers) == NUM_CARDS:
            return 2
            
        if not opponent_numbers:
            return max(player_numbers)

        opponent_highest = max(opponent_numbers)
        winning_cards = [card for card in player_numbers if card > opponent_highest]
        
        if winning_cards:
            return min(winning_cards)
        else:
            return min(player_numbers)

