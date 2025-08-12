import logging
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from mcp_server.page_agent import PageAgent


class PrimaryCenter(BaseModel):
    zone_name: str = Field(..., description="The name of the Zone.")
    primary_center_name: str = Field(
        ..., description="The name of the Primary Center (city/town)."
    )
    area_code: str = Field(..., description="The area code for the Primary Center.")


class AreaCodeData(BaseModel):
    primary_center_list: List[PrimaryCenter]


async def run(agent: PageAgent, logger: logging.Logger, config: Dict[str, Any]) -> dict:
    await agent.goto(
        "https://browserbase.github.io/stagehand-eval-sites/sites/ncc-area-codes/",
        wait_until="domcontentloaded",
    )

    extract_method = config.get("extract_method", "domExtract")
    use_text_extract = extract_method == "textExtract"

    instruction = (
        "Extract ALL the Primary Center names and their corresponding Area Code, "
        "and the name of their corresponding Zone."
    )

    extracted_data: AreaCodeData = await agent.extract(
        instruction=instruction,
        schema=AreaCodeData,
        use_text_extract=use_text_extract,
    )

    if not extracted_data or not extracted_data.primary_center_list:
        return {"_success": False, "error": "Extraction failed to return any data."}

    primary_center_list = extracted_data.primary_center_list
    expected_length = 56
    expected_first_item = {
        "zone_name": "Lagos Zone",
        "primary_center_name": "Lagos",
        "area_code": "01",
    }
    expected_last_item = {
        "zone_name": "South-East",
        "primary_center_name": "Yenagoa",
        "area_code": "089",
    }

    if len(primary_center_list) != expected_length:
        error_msg = f"Validation failed: Expected {expected_length} items, but got {len(primary_center_list)}."
        logger.error(error_msg)
        return {"_success": False, "error": error_msg}

    first_item = primary_center_list[0].model_dump()
    if first_item != expected_first_item:
        error_msg = f"Validation failed: First item mismatch. Expected {expected_first_item}, got {first_item}."
        logger.error(error_msg)
        return {"_success": False, "error": error_msg}

    last_item = primary_center_list[-1].model_dump()
    if last_item != expected_last_item:
        error_msg = f"Validation failed: Last item mismatch. Expected {expected_last_item}, got {last_item}."
        logger.error(error_msg)
        return {"_success": False, "error": error_msg}

    logger.info("✅ Validation passed for extract_area_codes.")
    return {"_success": True}
