import logging
from pydantic import BaseModel
from typing import List, Dict, Any
from mcp_server.page_agent import PageAgent


class Company(BaseModel):
    company: str
    batch: str


class CompanyList(BaseModel):
    companies: List[Company]


async def run(agent: PageAgent, logger: logging.Logger, config: Dict[str, Any]) -> dict:
    await agent.goto(
        "https://browserbase.github.io/stagehand-eval-sites/sites/aigrant/"
    )

    instruction = (
        "Extract all companies that received the AI grant and group them with their "
        "batch numbers as an array of objects. Each object should contain the "
        "company name and its corresponding batch number."
    )

    extract_method = config.get("extract_method", "domExtract")
    use_text_extract = extract_method == "textExtract"

    extracted_data = await agent.extract(
        instruction=instruction,
        schema=CompanyList,
        use_text_extract=use_text_extract,
    )

    companies = extracted_data.companies
    expected_length = 91
    expected_first_item = {"company": "Goodfire", "batch": "4"}

    if len(companies) != expected_length:
        error_msg = f"Incorrect number of companies. Expected {expected_length}, got {len(companies)}"
        logger.error(error_msg)
        return {"_success": False, "error": error_msg}

    first_item = companies[0]
    if (
        first_item.company != expected_first_item["company"]
        or first_item.batch != expected_first_item["batch"]
    ):
        error_msg = f"First item mismatch. Expected {expected_first_item}, got {first_item.dict()}"
        logger.error(error_msg)
        return {"_success": False, "error": error_msg}

    return {"_success": True}
