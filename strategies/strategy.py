from abc import ABC, abstractmethod

class Strategy(ABC):
    """
    Base class for all game strategies.
    Specific strategies must inherit from this class and implement the play method.
    """
    def __init__(self, name):
        self.name = name
    
    @abstractmethod
    def play(self, player_numbers, opponent_numbers):
        """
        Determines which number to play based on the game state.
        This method must be implemented by subclasses.
        """
