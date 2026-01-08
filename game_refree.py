from dataclasses import dataclass
from typing import Dict
import random


try:
    from google.adk.agent import Agent
    from google.adk.tools import tool
except ImportError:
    def tool(func):
        return func

    class Agent:
        def __init__(self, name, instructions, tools):
            self.name = name
            self.instructions = instructions
            self.tools = tools



@dataclass
class GameState:
    round: int = 0
    user_score: int = 0
    bot_score: int = 0
    user_bomb_used: bool = False
    bot_bomb_used: bool = False
    max_rounds: int = 3
    game_over: bool = False


STATE = GameState()

VALID_MOVES = {"rock", "paper", "scissors", "bomb"}



@tool
def validate_move(player: str, move: str) -> Dict:
    move = move.lower()

    if move not in VALID_MOVES:
        return {"valid": False, "reason": "Invalid move"}

    if move == "bomb":
        if player == "user" and STATE.user_bomb_used:
            return {"valid": False, "reason": "User bomb already used"}
        if player == "bot" and STATE.bot_bomb_used:
            return {"valid": False, "reason": "Bot bomb already used"}

    return {"valid": True, "move": move}


@tool
def resolve_round(user_move: str, bot_move: str) -> Dict:
    if user_move == bot_move:
        return {"winner": "draw"}

    if user_move == "bomb" and bot_move == "bomb":
        return {"winner": "draw"}

    if user_move == "bomb":
        return {"winner": "user"}

    if bot_move == "bomb":
        return {"winner": "bot"}

    rules = {
        "rock": "scissors",
        "paper": "rock",
        "scissors": "paper"
    }

    if rules[user_move] == bot_move:
        return {"winner": "user"}

    return {"winner": "bot"}


@tool
def update_game_state(result: str, user_move: str, bot_move: str) -> Dict:
    STATE.round += 1

    if user_move == "bomb":
        STATE.user_bomb_used = True
    if bot_move == "bomb":
        STATE.bot_bomb_used = True

    if result == "user":
        STATE.user_score += 1
    elif result == "bot":
        STATE.bot_score += 1

    if STATE.round >= STATE.max_rounds:
        STATE.game_over = True

    return {
        "round": STATE.round,
        "user_score": STATE.user_score,
        "bot_score": STATE.bot_score,
        "game_over": STATE.game_over
    }


referee_agent = Agent(
    name="rps_plus_referee",
    instructions="""
Rules:
- Best of 3 rounds
- Moves: rock, paper, scissors, bomb
- Bomb beats all, but only once per player
- Bomb vs bomb = draw
- Invalid input wastes the round
""",
    tools=[validate_move, resolve_round, update_game_state]
)



def play_game():
    print("\n Rock–Paper–Scissors–Plus")
    print("Best of 3 rounds")
    print("Moves: rock, paper, scissors, bomb (once)")
    print("Invalid input wastes the round\n")

    while not STATE.game_over:
        print(f"--- Round {STATE.round + 1} ---")
        user_input = input("Your move: ").strip().lower()

        user_check = validate_move("user", user_input)

        if not user_check["valid"]:
            print(f" Invalid move: {user_check['reason']}")
            update_game_state("draw", "invalid", "none")
            continue

        bot_choices = list(VALID_MOVES)
        if STATE.bot_bomb_used:
            bot_choices.remove("bomb")

        bot_move = random.choice(bot_choices)

        result = resolve_round(user_check["move"], bot_move)
        update_game_state(result["winner"], user_check["move"], bot_move)

        print(f"You played: {user_check['move']}")
        print(f"Bot played: {bot_move}")
        print(f"Round result: {result['winner'].upper()}")
        print(f"Score → You: {STATE.user_score} | Bot: {STATE.bot_score}\n")

    print(" GAME OVER")
    if STATE.user_score > STATE.bot_score:
        print(" Final Result: YOU WIN")
    elif STATE.bot_score > STATE.user_score:
        print(" Final Result: BOT WINS")
    else:
        print(" Final Result: DRAW")


if __name__ == "__main__":
    play_game()
