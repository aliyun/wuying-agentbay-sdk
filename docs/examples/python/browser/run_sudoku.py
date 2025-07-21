"""
Example demonstrating AIBrowser capabilites with AgentBay SDK.
This example shows how to use PageUseAgent to run sudoku game, including:
- Create AIBrowser session
- Use playwright to connect to AIBrowser instance through CDP protocol
- Utilize PageUseAgent to run sudoku game
"""

import os
import asyncio
from typing import List

from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams
from agentbay.browser.browser import BrowserOption
from agentbay.browser.browser_agent import ExtractOptions, ActOptions

from playwright.async_api import async_playwright
from pydantic import BaseModel, Field

class SudokuBoard(BaseModel):
    board: List[List[int]] = Field(..., description="9x9 sudoku board, 0 for empty")

class SudokuSolution(BaseModel):
    solution: List[List[int]] = Field(..., description="9x9 solved sudoku board")

def format_board_for_llm(board: List[List[int]]) -> str:
    return "\n".join(["  [" + ", ".join(map(str, row)) + "]" for row in board])

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

            async with async_playwright() as p:
                browser = await p.chromium.connect_over_cdp(endpoint_url)
                try:
                    page = await browser.new_page()
                    print("🌐 Navigating to Sudoku site...")
                    url = "https://widget.websudoku.com/"
                    await page.goto(url)
                    await page.wait_for_selector("#puzzle_grid", timeout=10000)

                    # 1. Extract the board
                    success = False
                    while not success:
                        print("📊 Extracting sudoku board...")
                        options = ExtractOptions(
                            instruction="Extract the current sudoku board as a 9x9 array. Each cell should be a number (1-9) if filled, or 0 if empty.",
                            schema=SudokuBoard
                        )
                        success, board_objs = await session.browser.agent.extract_async(page, options)
                        if not success:
                            print("❌ Failed to extract sudoku board, retry extracting")
                            await asyncio.sleep(3)

                    board = board_objs[0].board
                    print(
                        "Current Board:\n" + "\n".join([" ".join(map(str, row)) for row in board])
                    )
                    original_board = [row[:] for row in board]

                    # 2. Solve the sudoku
                    success, solution_objs = await session.browser.agent.extract_async(
                        page,
                        ExtractOptions(
                            instruction=
                            "You are an expert sudoku solver. Given the following sudoku board as a 9x9 array (0 means empty), solve the sudoku and return the completed 9x9 array as 'solution'.\n\n"
                            "Sudoku rules:\n"
                            "- Each row must contain the digits 1-9 with no repeats.\n"
                            "- Each column must contain the digits 1-9 with no repeats.\n"
                            "- Each of the nine 3x3 subgrids must contain the digits 1-9 with no repeats.\n"
                            "- Only fill in the cells that are 0.\n"
                            "- The solution must be unique and valid.\n\n"
                            f"board = [\n{format_board_for_llm(board)}\n]\n\n"
                            "Return:\n{\n  solution: number[][] // 9x9, all filled, valid sudoku\n}",
                            schema=SudokuSolution
                        )
                    )
                    solution = solution_objs[0].solution
                    print("Solved Board:\n" + "\n".join([" ".join(map(str, row)) for row in solution]))

                    # 3. Fill the solution (only first row for demo)
                    for row in range(1):
                        for col in range(9):
                            if original_board[row][col] == 0:
                                input_id = f"f{col}{row}"
                                print(f"Type '{solution[row][col]}' into the cell with id '{input_id}'")
                                # Use the new act method for natural language action
                                await session.browser.agent.act_async(page, ActOptions(action=f"Type '{solution[row][col]}' into the cell with id '{input_id}'"))
                                await asyncio.sleep(0.5)

                    print("✅ Finished! The board has been solved and filled in the browser.")

                except Exception as error:
                    print(f"❌ Error in game loop: {error}")
        else:
            print("Failed to initialize browser")

if __name__ == "__main__":
    asyncio.run(main())