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
import random

from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams
from agentbay.browser.browser import BrowserOption
from agentbay.browser.browser_agent import ExtractOptions, BrowserError

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
    move: Optional[int] = Field(
        None, description="The best move to make (0: up, 1: down, 2: left, 3: right, 4: none)."
    )
    confidence: float = Field(
        ..., description="Confidence score for the recommended move (0.0 to 1.0)."
    )
    reasoning: str = Field(..., description="Detailed reasoning for the chosen move.")

def transpose_grid(grid: List[List[int]]) -> List[List[int]]:
    if not grid:
        return []

    return list(map(list, zip(*grid)))

def format_grid_for_llm_instruction(grid_data: List[List[int]]) -> str:
    formatted_rows = []
    for i, row in enumerate(grid_data):
        formatted_rows.append(f"row{i+1}: {row}")
    return "\n".join(formatted_rows)

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
            page = None

            async with async_playwright() as p:
                browser = await p.chromium.connect_over_cdp(endpoint_url)
                try:
                    page = await browser.new_page()
                    print("🌐 Navigating to 2048...")
                    await page.goto("https://ovolve.github.io/2048-AI/", wait_until="domcontentloaded", timeout=180000)
                    print("🌐 Navigated to 2048 done")
                    await page.wait_for_selector(".grid-container", timeout=10000)

                    last_transposed_grid = None
                    transposed_grid_not_changed_times = 0
                    last_move_history = []

                    while True:
                        print("🔄 Game loop iteration...")
                        await asyncio.sleep(0.3)

                        # Get current game state
                        print("📊 Extracting game state...")
                        options = ExtractOptions(
                            instruction=
                            """
                            Extract the current game state:
                            1. Score from the score counter
                            2. All tile values and their positions in the 4x4 grid must be extracted. 
                               Each tile's value and position can be obtained from the tile-position-x-y class, where x (1 to 4) is the column and y (1 to 4) is the row.
                               For example, tile-position-4-1 means the tile is in column 4, row 1.
                               The value of the tile is given by the number in the tile's class.
                               For example, <div class='tile tile-2 tile-position-1-4 tile-new'>2</div> means a tile with value 2 at column 1, row 4;
                               and <div class='tile tile-2 tile-position-4-1 tile-new'>2</div> means a tile with value 2 at column 4, row 1.
                               Empty spaces should be represented as 0 in the grid.
                               For instance, if the only tiles present are the two above, the grid should be:[[0, 0, 0, 2], [0, 0, 0, 0], [0, 0, 0, 0], [2, 0, 0, 0]]
                            3. Highest tile value present
                            """,
                            schema=GameState
                        )
                        success, gameStates = await session.browser.agent.extract_async(page, options)
                        if success:
                            gameState = gameStates[0]
                            transposed_grid = transpose_grid(gameState.grid)
                            # transposed_grid = gameState.grid
                            print(f"transposed grid: {transposed_grid}")
                            print(f"gameState: {gameState}")
                            grid_instruction = format_grid_for_llm_instruction(transposed_grid)

                            if last_transposed_grid is not None and transposed_grid == last_transposed_grid:
                                transposed_grid_not_changed_times += 1
                            else:
                                transposed_grid_not_changed_times = 0
                                last_move_history = []
                            last_transposed_grid = transposed_grid

                            instruction_str = f"""
                            Based on the current game state:
                            - Score: {gameState.score}
                            - Highest tile: {gameState.highestTile}
                            - Grid: This is a 4x4 matrix ordered by row (top to bottom) and column (left to right). The rows are stacked vertically, and tiles can move vertically between rows or horizontally between columns:{grid_instruction}
                            What is the best move (up/down/left/right)? Consider:
                            1. Keeping high value tiles in corners (bottom left, bottom right, top left, top right)
                            2. Maintaining a clear path to merge tiles
                            3. Avoiding moves that could block merges
                            4. Avoiding moves that merge no blocks as possible
                            5. Only adjacent tiles of the same value can merge
                            6. Making a move will move all tiles in that direction until they hit a tile of a different value or the edge of the board
                            7. Tiles cannot move past the edge of the board
                            8. Each move must move at least one tile
                            """

                            if transposed_grid_not_changed_times >= 1:
                                instruction_str += f"""
                                9. Do not generate move value in {last_move_history}
                                10. If last move value {last_move_history[-1]} moves up or down, then generate move value with left or right direction, otherwise generate move value with up or down direction
                                """

                            next_move_options = ExtractOptions(
                                instruction=instruction_str,
                                schema=MoveAnalysis
                            )
                            success, next_move = await session.browser.agent.extract_async(page, next_move_options)
                            if success:
                                selected_move = next_move[0].move
                            else:
                                print("❌ Failed to extract next move, retry observing")
                                continue
                            last_move_history.append(selected_move)

                            move_key = {
                                0: "ArrowUp",
                                1: "ArrowDown",
                                2: "ArrowLeft",
                                3: "ArrowRight",
                                4: "Escape",
                            }[selected_move if selected_move is not None else 4]    

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