# Rock–Paper–Scissors–Plus AI Referee

## Overview
This project implements a minimal AI referee chatbot for a **best-of-3 Rock–Paper–Scissors–Plus** game using **Google ADK** concepts.

The agent enforces rules, tracks state across turns, validates inputs, resolves rounds, and ends the game automatically.

---

## State Model
The game state is stored in a structured `GameState` dataclass:
- `round`: current round number
- `user_score`, `bot_score`
- `user_bomb_used`, `bot_bomb_used`
- `game_over`

State **does not live in the prompt** and is mutated only via tools.

---

## Agent & Tool Design

### Agent
- Single referee agent
- Responsible only for orchestration and explanation
- Delegates all logic and mutation to tools

### Tools (Explicit)
1. **validate_move**
   - Checks legality of a move
   - Enforces one-time bomb rule

2. **resolve_round**
   - Encapsulates all win/draw logic
   - Deterministic and stateless

3. **update_game_state**
   - Mutates and persists game state
   - Enforces round limit

This cleanly separates:
- Intent understanding
- Game logic
- State mutation
- Response generation

---

## Tradeoffs
- Bot strategy is intentionally simple (random legal move)
- CLI loop included only for demonstration
- No advanced NLU — assumes simple text input

---

## Improvements With More Time
- Smarter bot strategy
- Structured JSON outputs for UI integration
- Multi-agent separation (Referee vs Player agent)
- Test suite for edge cases

---

## Why This Design Works
- Correct logic
- Explicit ADK tool usage
- Clear state persistence
- Simple, inspectable, and extensible

