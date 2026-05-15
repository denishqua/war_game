# High Card Game Simulation & Web Interface

A Python-based "High Card" game engine featuring a modern, interactive web interface built with Flask. This project evolved from a simple Python console game into a complex competitive simulation environment.

## Features

- **Interactive Web UI**: A premium, responsive interface to play the High Card game against various AI strategies.
- **Advanced Game Rules**:
  - Custom "1 beats Max" rule: The lowest card (1) can beat the highest card in the deck.
  - Tie-breaker logic and 0.5-point scoring for ties.
- **AI Strategies**: Features multiple bot strategies ranging from simple random play to an advanced "Optimum" strategy utilizing mixed-strategy game theory.
- **Simulation Mode**: Pit different AI strategies against each other over thousands of games to see which performs better.
- **Tournament Mode**: Evaluate and rank all available bot strategies against a baseline strategy over large-scale simulations.

## Project Structure

- `app.py`: The Flask web server providing the API and serving the frontend.
- `game.py`: The core game engine containing the rules, player logic, and match simulation.
- `test_game.py`: Unit tests for the game engine logic.
- `strategies/`: Directory containing different AI bot strategies.
- `templates/`: HTML templates for the Flask application.
- `static/`: Static assets including CSS and JavaScript for the web frontend.

## Installation & Setup

1. Ensure you have Python 3 installed.
2. Install the required dependencies:
   ```bash
   pip install flask pytest
   ```

## Usage

To start the web application, simply run:

```bash
python app.py
```

Then, open your web browser and navigate to `http://127.0.0.1:5000` to interact with the game.

## Testing

To run the unit tests for the game logic:

```bash
pytest test_game.py
```
