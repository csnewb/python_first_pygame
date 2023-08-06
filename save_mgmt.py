import json

def save_high_scores(scores):
    with open("high_scores.json", "w") as file:
        json.dump(scores, file)

def load_high_scores():
    try:
        with open("high_scores.json", "r") as file:
            scores = json.load(file)
            return scores
    except FileNotFoundError:
        return {}  # Return an empty dictionary if the file doesn't exist

def update_high_scores(MAX_SCORE, PLAYER_NAME, LEVEL, DIFFICULTY_LEVEL):
    # Load existing high scores
    scores = load_high_scores()

    # New score entry
    new_score = {
        "MAX_SCORE": MAX_SCORE,
        "PLAYER_NAME": PLAYER_NAME,
        "LEVEL": LEVEL,
        "DIFFICULTY_LEVEL": DIFFICULTY_LEVEL
    }

    # Add the new score to the scores list
    scores_list = scores.get("scores", [])
    scores_list.append(new_score)

    # Sort scores by MAX_SCORE in descending order and keep only the top 50
    scores_list.sort(key=lambda x: x["MAX_SCORE"], reverse=True)
    scores_list = scores_list[:50]

    # Save updated scores
    scores["scores"] = scores_list
    save_high_scores(scores)


def print_high_scores():
    scores_data = load_high_scores()
    scores_list = scores_data.get("scores", [])

    if not scores_list:
        print("No high scores available.")
        return

    print("High Scores:")
    print("----------------------------------------")
    print("Rank | Score | Name       | Level | Difficulty")
    print("----------------------------------------")

    for rank, score in enumerate(scores_list, 1):
        print(f"{rank:4} | {score['MAX_SCORE']:5} | {score['PLAYER_NAME'][:10]:10} | {score['LEVEL']:5} | {score['DIFFICULTY_LEVEL']}")

    print("----------------------------------------")
