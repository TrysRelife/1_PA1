import json
import os

SCORE_FILE = "high_scores.json" # File to store scores
MAX_SCORES_PER_ALGO = 10       # Max scores to keep per algorithm

def load_scores():
    """
    Loads high scores from the JSON file.
    Returns default structure if file missing or invalid.
    """
    default_scores = {"minimax": [], "alphabeta": []}
    if not os.path.exists(SCORE_FILE):
        return default_scores
    try:
        with open(SCORE_FILE, 'r') as f:
            scores = json.load(f)
            # Ensure basic structure exists
            if "minimax" not in scores: scores["minimax"] = []
            if "alphabeta" not in scores: scores["alphabeta"] = []
            return scores
    except (json.JSONDecodeError, IOError, TypeError) as e:
        print(f"Error loading scores from {SCORE_FILE}: {e}. Returning empty scores.")
        return default_scores

def save_scores(scores):
    """Saves the provided scores dictionary to the JSON file."""
    try:
        with open(SCORE_FILE, 'w') as f:
            json.dump(scores, f, indent=4) # Save with indentation
    except IOError as e:
        print(f"Error saving scores to {SCORE_FILE}: {e}")

def add_score(game_data):
    """
    Adds a new game result to the high scores list for the relevant algorithm.
    Keeps only the latest N scores and saves back to the file.
    """
    # Validate input data
    if not isinstance(game_data, dict) or \
       'algorithm' not in game_data or \
       game_data['algorithm'] not in ['minimax', 'alphabeta']:
        print(f"Invalid game data provided for scoring: {game_data}. Score not added.")
        return

    algo = game_data['algorithm']
    scores = load_scores() # Load current scores

    # Append new score data
    scores[algo].append(game_data)

    # Keep only the latest N scores
    scores[algo] = scores[algo][-MAX_SCORES_PER_ALGO:]

    save_scores(scores) # Save updated scores