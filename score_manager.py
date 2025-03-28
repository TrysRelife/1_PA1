import json
import os

SCORE_FILE = "high_scores.json" # Name of the file to store scores
MAX_SCORES_PER_ALGO = 10       # Maximum number of scores to keep for each algorithm

def load_scores():
    """Loads scores from the JSON file. Returns default structure if file is missing or invalid."""
    # Default structure if no file exists or loading fails
    default_scores = {"minimax": [], "alphabeta": []}
    if not os.path.exists(SCORE_FILE):
        return default_scores
    try:
        with open(SCORE_FILE, 'r') as f:
            scores = json.load(f)
            # Ensure the basic keys exist even if the file was partially corrupted
            if "minimax" not in scores: scores["minimax"] = []
            if "alphabeta" not in scores: scores["alphabeta"] = []
            return scores
    except (json.JSONDecodeError, IOError, TypeError) as e:
        # Handle potential errors during file reading or JSON parsing
        print(f"Error loading scores from {SCORE_FILE}: {e}. Returning empty scores.")
        return default_scores

def save_scores(scores):
    """Saves the scores dictionary to the JSON file."""
    try:
        with open(SCORE_FILE, 'w') as f:
            # Save with indentation for readability
            json.dump(scores, f, indent=4)
    except IOError as e:
        print(f"Error saving scores to {SCORE_FILE}: {e}")

def add_score(game_data):
    """Adds a new game result to the scores list for the relevant algorithm."""

    algo = game_data['algorithm']
    scores = load_scores() # Load the current scores

    # Append the new game result data
    scores[algo].append(game_data)

    # Trim the list to keep only the latest N scores (FIFO if N exceeded)
    scores[algo] = scores[algo][-MAX_SCORES_PER_ALGO:]

    save_scores(scores) # Save the updated scores back to the file