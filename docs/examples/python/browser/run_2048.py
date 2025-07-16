"""
Example demonstrating AIBrowser capabilites with AgentBay SDK.
This example shows how to use PageUseAgent to run 2048 game, including:
- Create AIBrowser session
- Use playwright to connect to AIBrowser instance through CDP protocol
- Utilize PageUseAgent to run 2048 game
"""

import os
import time
import asyncio
from typing import List, Literal, Optional, Tuple, Deque
from collections import deque

from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams
from agentbay.browser.browser import BrowserOption
from agentbay.browser.browser_agent import ExtractOptions, BrowserError

from mini_max import MiniMax

from playwright.async_api import async_playwright
from pydantic import BaseModel, Field


class GameState(BaseModel):
    score: Optional[int] = Field(
        None, description="Current score from the score counter."
    )
    highestTile: Optional[int] = Field(
        None, description="Highest tile value currently present on the board."
    )
    grid: List[List[int]] = Field(
        ..., description="4x4 grid of tile values (empty spaces as 0)."
    )


class MoveAnalysis(BaseModel):
    move: Literal["up", "down", "left", "right"] = Field(
        ..., description="The best move to make (up/down/left/right)."
    )
    confidence: float = Field(
        ..., description="Confidence score for the recommended move (0.0 to 1.0)."
    )
    reasoning: str = Field(..., description="Detailed reasoning for the chosen move.")


MoveHistoryEntry = Tuple[Tuple[Tuple[int, ...], ...], str]


def transpose_grid(grid: List[List[int]]) -> List[List[int]]:
    if not grid:
        return []

    return list(map(list, zip(*grid)))


def format_grid_for_llm_instruction(grid_data: List[List[int]]) -> str:
    formatted_rows = []
    for i, row in enumerate(grid_data):
        formatted_rows.append(f"row{i+1}: {row}")
    return "\n".join(formatted_rows)


def format_original_grid_for_llm_instruction(grid_data: List[List[int]]) -> str:
    """Formats the 4x4 grid into a string suitable for LLM instruction (row-major)."""
    lines = []
    for i, row in enumerate(grid_data):
        lines.append(f"             row{i + 1}: {', '.join(map(str, row))}")
    return "\n".join(lines)

async def main():
    # Get API key from environment variable
    api_key = os.getenv("AGENTBAY_API_KEY")
    if not api_key:
        print("Error: AGENTBAY_API_KEY environment variable not set")
        return

    # Initialize AgentBay client
    print("Initializing AgentBay client...")
    agent_bay = AgentBay(api_key=api_key)

    # Create a session
    print("Creating a new session...")
    params = CreateSessionParams(
        image_id="browser_latest",  # Specify the image ID
    )
    session_result = agent_bay.create(params)

    if session_result.success:
        session = session_result.session
        print(f"Session created with ID: {session.session_id}")

        if await session.browser.initialize_async(BrowserOption()):
            print("Browser initialized successfully")
            endpoint_url = session.browser.get_endpoint_url()
            print("endpoint_url =", endpoint_url)

            helper = MiniMax()
            move_history: Deque[MoveHistoryEntry] = deque(maxlen=3)
            last_grid_state = None
            moves_map = {0: "left", 1: "up", 2: "right", 3: "down"}
            all_possible_moves = ["left", "up", "right", "down"]
            page = None

            async with async_playwright() as p:
                browser = await p.chromium.connect_over_cdp(endpoint_url)
                try:
                    page = await browser.new_page()
                    print("🌐 Navigating to 2048...")
                    await page.goto("https://ovolve.github.io/2048-AI/", timeout=180000)
                    print("🌐 Navigated to 2048 done")
                    await page.wait_for_selector(".grid-container", timeout=10000)

                    while True:
                        print("🔄 Game loop iteration...")
                        await asyncio.sleep(0.3)

                        # Get current game state
                        print("📊 Extracting game state...")
                        options = ExtractOptions(
                            instruction="Extract the current game state: 1. Score from the score counter 2. All tile values in the 4x4 grid (empty spaces as 0) 3. Highest tile value present",
                            schema=GameState
                        )
                        success, gameStates = await session.browser.agent.extract_async(page, options)
                        if success:
                            gameState = gameStates[0]
                            transposed_grid = transpose_grid(gameState.grid)
                            # transposed_grid = gameState.grid
                            print(f"transposed grid: {transposed_grid}")
                            print("🤔 Analyzing board for next move...")
                            current_grid_flat = tuple(tile for row in transposed_grid for tile in row)

                            if last_grid_state is not None and current_grid_flat == last_grid_state:
                                print(
                                    "🚨 Grid has not changed from the last iteration. This might indicate a stuck state."
                                )
                            last_grid_state = current_grid_flat

                            helper.grid = [tile for row in transposed_grid for tile in row]
                            helper.StartSearch()

                            moves_map = {0: "left", 1: "up", 2: "right", 3: "down"}
                            best_move_str = moves_map.get(helper.best_operation, "no_move")
                            selected_move = best_move_str
                            print(
                                f"Calculated mini max move: {best_move_str} (explored {helper.node} nodes, max_depth={helper.max_depth})."
                            )
                            current_grid_tuple = tuple(tuple(row) for row in gameState.grid)

                            move_history.append((current_grid_tuple, best_move_str))

                            if len(move_history) == 3:
                                recent_combinations = list(move_history)
                                is_cycling = False
                                if (
                                    all(item == recent_combinations[0] for item in recent_combinations)
                                    and best_move_str != "no_move"
                                ):
                                    is_cycling = True
                                    print(
                                        f"Detected a continuous cycle! The pattern {recent_combinations[0]} repeated {3} times."
                                    )

                                if is_cycling:
                                    print("Breaking out of cycle with alternative moves!")
                                    move_history.clear()

                                    available_moves = [
                                        m
                                        for m in all_possible_moves
                                        if m != best_move_str and m != "no_move"
                                    ]
                                    if available_moves:
                                        import random

                                        selected_move = random.choice(available_moves)

                            move_key = {
                                "up": "ArrowUp",
                                "down": "ArrowDown",
                                "left": "ArrowLeft",
                                "right": "ArrowRight",
                                "no_move": "Escape",
                            }[selected_move]
                            # }[analysis.move]

                            await page.keyboard.press(move_key)
                        else:
                            print("❌ Failed to extract game state, retry observing")

                except Exception as error:
                    print(f"❌ Error in game loop: {error}")
                    try:
                        if page is not None:
                            is_game_over = await page.evaluate(
                                "() => document.querySelector('.game-over') !== null"
                            )
                            if is_game_over:
                                print("🏁 Game Over!")
                                return

                    except Exception as inner_e:
                        print(f"Could not check game over status: {inner_e}")
                    raise
        else:
            print("Failed to initialize browser")

if __name__ == "__main__":
    asyncio.run(main())