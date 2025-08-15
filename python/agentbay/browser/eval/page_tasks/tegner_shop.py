import logging
import asyncio
import json
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Any, Dict
from datetime import datetime
from dotenv import load_dotenv
from agentbay.browser.eval.page_agent import PageAgent

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


from pydantic import BaseModel, Field, HttpUrl, field_validator
from typing import List
from urllib.parse import urljoin


class ProductInfo(BaseModel):
    name: str
    price: str
    link: Optional[HttpUrl] = Field(
        None, description="The absolute URL to the product's detail page."
    )

    @field_validator("link", mode="before")
    @classmethod
    def validate_and_clean_link(cls, v: Any) -> Optional[str]:
        if not isinstance(v, str) or not v:
            return None

        if v.startswith("/"):
            base_url = "https://tegner.shop"
            return urljoin(base_url, v)

        if v.startswith("#"):
            return None

        return v


class InspectionResult(BaseModel):
    products: List[ProductInfo]


class InspectionResult(BaseModel):
    products: List[ProductInfo] = Field(..., description="A list of all products.")


async def run(agent: PageAgent, logger: logging.Logger, config: Dict[str, Any]):
    """
    Performs a paginated e-commerce site inspection.
    """
    try:
        await agent.goto("https://tegner.shop/")
        await agent.act("Click 'All products' button or link")
        all_extracted_products = []
        page_count = 1
        while True:
            page_result: InspectionResult = await agent.extract(
                instruction="Extract all products visible on the current page. For each product, get its name, price, and the complete, absolute URL to its product page.",
                schema=InspectionResult,
                use_text_extract=True,
            )
            if page_result and page_result.products:
                logger.info(
                    f"  > Found {len(page_result.products)} products on this page."
                )
                all_extracted_products.extend(page_result.products)
            else:
                logger.warning(
                    "  > No products found on this page, continuing to next page check."
                )
            
            logger.info("  > Checking for a 'Next' page button...")
            action_result = await agent.act("Scroll down to the bottom of the page.")
            action_result = await agent.act(
                "Click the 'Next' button or a link that navigates to the next page. "
                "This button is often marked with text 'Next', '>', or '→'."
            )
            if action_result and action_result.success:
                logger.info("  > Successfully navigated to the next page.")
                page_count += 1
                await asyncio.sleep(3)
            else:
                logger.info(
                    "> Could not find or click a 'Next' button. Reached the last page."
                )
                break

        logger.info("\n--- Final Inspection Report ---")
        total_products = len(all_extracted_products)
        logger.info(
            f"Extraction complete. Scanned {page_count} pages and found a total of {total_products} products."
        )

        if all_extracted_products:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"/Users/hangsu/Downloads/inspection_results_{timestamp}.json"

            logger.info(
                f"\n--- Saving {total_products} products to file: {output_filename} ---"
            )

            try:
                products_as_dicts = [
                    p.model_dump(mode="json") for p in all_extracted_products
                ]
                with open(output_filename, "w", encoding="utf-8") as f:
                    json.dump(products_as_dicts, f, ensure_ascii=False, indent=2)

                logger.info(f"✅ Successfully saved results to {output_filename}")

            except Exception as e:
                logger.error(f"❌ Failed to save results to file: {e}")

        logger.info("\n✅ Paginated inspection demo finished successfully.")

        logger.info("\n✅ Paginated inspection demo finished successfully.")

    except Exception as e:
        logger.error(
            f"❌ An error occurred during the paginated inspection: {e}", exc_info=True
        )
    finally:
        if "agent" in locals() and hasattr(agent, "close"):
            await agent.close()