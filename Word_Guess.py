from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def load_words(filename):

    file_path = BASE_DIR / filename

    with open(file_path, "r", encoding="utf-8") as file:
        words = [line.strip().lower() for line in file if line.strip()]

    return words


def process_guess(game_state, guess):

    if guess in game_state["guessed_letters"]:
        return "already_guessed"

    game_state["guessed_letters"].add(guess)

    if guess in game_state["word"]:

        for i, ch in enumerate(game_state["word"]):
            if ch == guess:
                game_state["shown"][i] = guess

        if "-" not in game_state["shown"]:
            return "win"

        return "correct"

    game_state["attempts"] += 1

    if game_state["attempts"] >= game_state["max_attempts"]:
        return "lose"

    return "wrong"