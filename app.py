from flask import Flask, render_template, request, jsonify
from game import Player, Match, get_all_strategies, NUM_CARDS

app = Flask(__name__)

# Very simple local state
current_state = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/strategies")
def strategies():
    strats = get_all_strategies()
    return jsonify({k: v.name for k, v in strats.items()})

@app.route("/api/play/start", methods=["POST"])
def play_start():
    data = request.json
    strategy_id = data.get("strategy_id", "1")
    num_cards = int(data.get("num_cards", 10))
    
    strats = get_all_strategies()
    computer_strategy = strats.get(strategy_id, strats["1"])
    
    player1 = Player("You", num_cards)
    player2 = Player("Computer", num_cards)
    
    # We create a Match instance but we won't call play_match(). We just use it for _update_game_state.
    match = Match(player1, player2, None, computer_strategy, verbose=False, num_cards=num_cards)
    
    current_state['match'] = match
    current_state['turn'] = 1
    
    return jsonify({
        "player_numbers": player1.numbers,
        "opponent_numbers": player2.numbers,
        "player_score": player1.score,
        "opponent_score": player2.score,
        "turn": current_state['turn'],
        "total_turns": num_cards,
        "game_over": False
    })

@app.route("/api/play/turn", methods=["POST"])
def play_turn():
    if 'match' not in current_state:
        return jsonify({"error": "No game started"}), 400
        
    match = current_state['match']
    data = request.json
    p1_choice = data.get("choice")
    
    if p1_choice not in match.player1.numbers:
        return jsonify({"error": "Invalid choice"}), 400
        
    p2_choice = match.strategy2.play(match.player2.numbers, match.player1.numbers)
    
    # We call update_game_state directly.
    match._update_game_state(p1_choice, p2_choice)
    
    current_state['turn'] += 1
    game_over = current_state['turn'] > match.total_turns
    
    result_text = "Tie!"
    if match.player1.played_numbers[-1] == p1_choice:
        # Determine who won this specific turn to send back in UI
        if p1_choice == 1 and p2_choice == match.total_turns:
            result_text = f"You won the turn! (1 beats {match.total_turns})"
        elif p2_choice == 1 and p1_choice == match.total_turns:
            result_text = f"Computer won the turn! (1 beats {match.total_turns})"
        elif p1_choice > p2_choice:
            result_text = "You won the turn!"
        elif p2_choice > p1_choice:
            result_text = "Computer won the turn!"
            
    final_winner = None
    if game_over:
        if match.player1.score > match.player2.score:
            final_winner = "You"
        elif match.player2.score > match.player1.score:
            final_winner = "Computer"
        else:
            final_winner = "Tie"

    return jsonify({
        "player_numbers": match.player1.numbers,
        "opponent_numbers": match.player2.numbers,
        "player_score": match.player1.score,
        "opponent_score": match.player2.score,
        "turn": min(current_state['turn'], match.total_turns),
        "total_turns": match.total_turns,
        "game_over": game_over,
        "turn_result": {
            "player_played": p1_choice,
            "computer_played": p2_choice,
            "text": result_text
        },
        "final_winner": final_winner
    })

@app.route("/api/simulate", methods=["POST"])
def simulate():
    data = request.json
    strat1_id = data.get("strat1_id", "1")
    strat2_id = data.get("strat2_id", "2")
    num_games = int(data.get("num_games", 100))
    num_cards = int(data.get("num_cards", 10))
    
    strats = get_all_strategies()
    s1 = strats.get(strat1_id, strats["1"])
    s2 = strats.get(strat2_id, strats["2"])
    
    player1_wins = 0
    player2_wins = 0
    ties = 0
    
    for _ in range(num_games):
        p1 = Player(s1.name, num_cards)
        p2 = Player(s2.name, num_cards)
        m = Match(p1, p2, s1, s2, verbose=False, num_cards=num_cards)
        res = m.play_match()
        if res == 1:
            player1_wins += 1
        elif res == 2:
            player2_wins += 1
        else:
            ties += 1
            
    return jsonify({
        "strat1_name": s1.name,
        "strat2_name": s2.name,
        "player1_wins": player1_wins,
        "player2_wins": player2_wins,
        "ties": ties
    })

@app.route("/api/tournament", methods=["POST"])
def tournament():
    data = request.json
    num_games = int(data.get("num_games", 10000))
    num_cards = int(data.get("num_cards", 10))
    
    strats = get_all_strategies()
    random_strategy = strats["1"]
    
    results = []
    
    for s1 in strats.values():
        s1_wins = 0
        s2_wins = 0
        ties = 0
        
        for _ in range(num_games):
            p1 = Player(s1.name, num_cards)
            p2 = Player(random_strategy.name, num_cards)
            m = Match(p1, p2, s1, random_strategy, verbose=False, num_cards=num_cards)
            res = m.play_match()
            if res == 1:
                s1_wins += 1
            elif res == 2:
                s2_wins += 1
            else:
                ties += 1
                
        if s1.name == random_strategy.name and s2_wins > s1_wins:
            s1_wins, s2_wins = s2_wins, s1_wins
            
        results.append({
            "strategy": s1.name,
            "wins": s1_wins,
            "losses": s2_wins,
            "ties": ties
        })
        
    results.sort(key=lambda x: x["wins"], reverse=True)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
