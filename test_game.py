import pytest
from game import Player, Match, get_all_strategies
from strategies.strategy import Strategy
from app import app

# A dummy strategy for testing purposes
class DummyStrategy(Strategy):
    def __init__(self, fixed_choice):
        super().__init__("Dummy")
        self.fixed_choice = fixed_choice

    def play(self, player_numbers, opponent_numbers):
        return self.fixed_choice

def test_player_initialization():
    p = Player("Test", num_cards=5)
    assert p.name == "Test"
    assert p.score == 0
    assert p.numbers == [1, 2, 3, 4, 5]
    assert p.played_numbers == []

def test_player_remove_number():
    p = Player("Test", num_cards=5)
    assert p.remove_number(3) == True
    assert p.numbers == [1, 2, 4, 5]
    assert p.remove_number(3) == False

def test_match_turn_logic_normal():
    p1 = Player("P1", num_cards=10)
    p2 = Player("P2", num_cards=10)
    # 5 vs 3
    s1 = DummyStrategy(5)
    s2 = DummyStrategy(3)
    match = Match(p1, p2, s1, s2, num_cards=10)
    
    match._update_game_state(5, 3)
    assert p1.score == 1
    assert p2.score == 0
    assert 5 not in p1.numbers
    assert 3 not in p2.numbers

def test_match_turn_logic_one_beats_max():
    p1 = Player("P1", num_cards=10)
    p2 = Player("P2", num_cards=10)
    s1 = DummyStrategy(1)
    s2 = DummyStrategy(10)
    match = Match(p1, p2, s1, s2, num_cards=10)
    
    match._update_game_state(1, 10)
    # 1 should beat max (10)
    assert p1.score == 1
    assert p2.score == 0

def test_match_turn_logic_tie():
    p1 = Player("P1", num_cards=10)
    p2 = Player("P2", num_cards=10)
    s1 = DummyStrategy(7)
    s2 = DummyStrategy(7)
    match = Match(p1, p2, s1, s2, num_cards=10)
    
    match._update_game_state(7, 7)
    assert p1.score == 0.5
    assert p2.score == 0.5

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_api_strategies(client):
    response = client.get('/api/strategies')
    assert response.status_code == 200
    data = response.get_json()
    assert "1" in data
    assert data["1"] == "Random"

def test_api_play_start(client):
    response = client.post('/api/play/start', json={"strategy_id": "1", "num_cards": 5})
    assert response.status_code == 200
    data = response.get_json()
    assert data["total_turns"] == 5
    assert len(data["player_numbers"]) == 5

def test_api_simulate(client):
    response = client.post('/api/simulate', json={
        "strat1_id": "1", 
        "strat2_id": "2", 
        "num_games": 10,
        "num_cards": 10
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "player1_wins" in data
    assert "player2_wins" in data
    assert "ties" in data
