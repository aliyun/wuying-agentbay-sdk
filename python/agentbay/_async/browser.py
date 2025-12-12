import asyncio
import base64
import os
import time
import typing
from typing import TYPE_CHECKING, Literal, Optional, Union

from .._common.config import _BROWSER_DATA_PATH
from .._common.exceptions import BrowserError
from .._common.logger import _log_api_response_with_details, get_logger
from ..api.models import InitBrowserRequest
from .base_service import AsyncBaseService
from .browser_agent import AsyncBrowserAgent

# Initialize logger for this module
_logger = get_logger("browser")

if TYPE_CHECKING:
    from .._common.models import FingerprintFormat
    from .._common.models import BrowserOption
    from .session import AsyncSession

class AsyncBrowser(AsyncBaseService):
    """
    Browser provides browser-related operations for the session.
    """

    def __init__(self, session: "AsyncSession"):
        self.session = session
        self._endpoint_url = None
        self._initialized = False
        self._option = None
        self.agent = AsyncBrowserAgent(self.session, self)
        self.endpoint_router_port = None

    async def initialize(self, option: Optional["BrowserOption"] = None) -> bool:
        """
        Initialize the browser instance with the given options asynchronously.
        Returns True if successful, False otherwise.

        Args:
            option (BrowserOption, optional): Browser configuration options. If None, default options are used.

        Returns:
            bool: True if initialization was successful, False otherwise.

        Example:
            ```python
            create_result = await agent_bay.create()
            session = create_result.session
            # Use default options
            await session.browser.initialize()
            # Or with specific options
            browser_option = BrowserOption(use_stealth=True)
            await session.browser.initialize(browser_option)
            await session.delete()
            ```
        """
        if self.is_initialized():
            return True

        if option is None:
            option = BrowserOption()

        try:
            browser_option_dict = option._to_map()

            # Enable record if session.enableBrowserReplay is True
            if (
                hasattr(self.session, "enableBrowserReplay")
                and self.session.enableBrowserReplay
            ):
                browser_option_dict["enableRecord"] = True

            request = InitBrowserRequest(
                authorization=f"Bearer {self.session._get_api_key()}",
                session_id=self.session._get_session_id(),
                persistent_path=_BROWSER_DATA_PATH,
                browser_option=browser_option_dict,
            )
            # Use async client method
            response = await self.session._get_client().init_browser_async(request)
            _logger.debug(f"Response from init_browser: {response}")
            response_map = response.to_map()
            body = response_map.get("body", {})
            data = body.get("Data", {})
            success = data.get("Port") is not None
            if success:
                self.endpoint_router_port = data.get("Port")
                self._initialized = True
                self._option = option
                _log_api_response_with_details(
                    api_name="InitBrowser (async)",
                    success=True,
                    key_fields={
                        "port": data.get("Port"),
                        "status": "successfully initialized",
                    },
                )
                _logger.info("Browser instance successfully initialized")
            return success
        except Exception as e:
            _logger.exception(
                f"❌ Failed to initialize browser instance asynchronously"
            )
            self._initialized = False
            self._endpoint_url = None
            self._option = None
            return False

    async def init(self, option: Optional["BrowserOption"] = None) -> bool:
        """
        Alias for initialize.
        """
        return await self.initialize(option)

    async def destroy(self):
        """
        Destroy the browser instance manually.
        """
        await self._stop_browser()

    async def screenshot(self, page, full_page: bool = False, **options) -> bytes:
        """
        Takes a screenshot of the specified page with enhanced options and error handling.

        Args:
            page (Page): The Playwright Page object to take a screenshot of. This is a required parameter.
            full_page (bool): Whether to capture the full scrollable page. Defaults to False.
            **options: Additional screenshot options that will override defaults.
                      Common options include:
                      - type (str): Image type, either 'png' or 'jpeg' (default: 'png')
                      - quality (int): Quality of the image, between 0-100 (jpeg only)
                      - timeout (int): Maximum time in milliseconds (default: 60000)
                      - animations (str): How to handle animations (default: 'disabled')
                      - caret (str): How to handle the caret (default: 'hide')
                      - scale (str): Scale setting (default: 'css')

        Returns:
            bytes: Screenshot data as bytes.

        Raises:
            BrowserError: If browser is not initialized.
            RuntimeError: If screenshot capture fails.
        """
        # Check if browser is initialized
        if not self.is_initialized():
            raise BrowserError("Browser must be initialized before calling screenshot.")
        if page is None:
            raise ValueError("Page cannot be None")
        # Set default enhanced options
        enhanced_options = {
            "animations": "disabled",
            "caret": "hide",
            "scale": "css",
            "timeout": options.get("timeout", 60000),
            "full_page": full_page,  # Use the function parameter, not options
            "type": options.get("type", "png"),
        }

        # Update with user-provided options (but full_page is already set from function parameter)
        enhanced_options.update(options)

        try:
            # Wait for page to load
            # await page.wait_for_load_state("networkidle")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_load_state("domcontentloaded", timeout=30000)
            # Scroll to load all content (especially for lazy-loaded elements)
            await self._scroll_to_load_all_content_async(page)

            # Ensure images with data-src attributes are loaded
            await page.evaluate(
                """
                () => {
                    document.querySelectorAll('img[data-src]').forEach(img => {
                        if (!img.src && img.dataset.src) {
                            img.src = img.dataset.src;
                        }
                    });
                    // Also handle background-image[data-bg]
                    document.querySelectorAll('[data-bg]').forEach(el => {
                        if (!el.style.backgroundImage) {
                            el.style.backgroundImage = `url(${el.dataset.bg})`;
                        }
                    });
                }
            """
            )

            # Wait a bit for images to load
            await page.wait_for_timeout(1500)
            final_height = await page.evaluate("document.body.scrollHeight")
            await page.set_viewport_size(
                {"width": 1920, "height": min(final_height, 10000)}
            )

            # Take the screenshot
            screenshot_bytes = await page.screenshot(**enhanced_options)
            _logger.info("Screenshot captured successfully.")
            return screenshot_bytes

        except Exception as e:
            # Convert exception to string safely to avoid comparison issues
            try:
                error_str = str(e)
            except:
                error_str = "Unknown error occurred"
            error_msg = f"Failed to capture screenshot: {error_str}"
            _logger.error(error_msg)
            raise RuntimeError(error_msg) from e

    async def _scroll_to_load_all_content_async(
        self, page, max_scrolls: int = 8, delay_ms: int = 1200
    ):
        """Async version of _scroll_to_load_all_content."""
        last_height = 0
        for _ in range(max_scrolls):
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(delay_ms)
            new_height = await page.evaluate(
                "Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)"
            )
            if new_height == last_height:
                break
            last_height = new_height

    async def _stop_browser(self):
        """
        Stop the browser instance, internal use only.
        """
        if self.is_initialized():
            await self.session.call_mcp_tool("stopChrome", {})
        else:
            raise BrowserError("Browser is not initialized. Cannot stop browser.")

    async def get_endpoint_url(self) -> str:
        """
        Returns the endpoint URL if the browser is initialized, otherwise raises an exception.
        When initialized, always fetches the latest CDP url from session.get_link().

        Returns:
            str: The browser CDP endpoint URL.

        Raises:
            BrowserError: If browser is not initialized or endpoint URL cannot be retrieved.

        Example:
            ```python
            create_result = await agent_bay.create()
            session = create_result.session
            browser_option = BrowserOption()
            await session.browser.initialize(browser_option)
            endpoint_url = await session.browser.get_endpoint_url()
            print(f"CDP Endpoint: {endpoint_url}")
            await session.delete()
            ```
        """
        if not self.is_initialized():
            raise BrowserError(
                "Browser is not initialized. Cannot access endpoint URL."
            )
        try:
            if self.session.is_vpc:
                _logger.debug(
                    f"VPC mode, endpoint_router_port: {self.endpoint_router_port}"
                )
                self._endpoint_url = f"ws://{self.session.network_interface_ip}:{self.endpoint_router_port}"
            else:
                from ..api.models import GetCdpLinkRequest

                request = GetCdpLinkRequest(
                    authorization=f"Bearer {self.session.agent_bay.api_key}",
                    session_id=self.session.session_id,
                )
                # Async call
                response = await self.session.agent_bay.client.get_cdp_link_async(
                    request
                )
                if response.body and response.body.success and response.body.data:
                    self._endpoint_url = response.body.data.url
                else:
                    error_msg = (
                        response.body.message if response.body else "Unknown error"
                    )
                    raise BrowserError(f"Failed to get CDP link: {error_msg}")
            return self._endpoint_url
        except Exception as e:
            raise BrowserError(f"Failed to get endpoint URL from session: {e}")

    def get_option(self) -> Optional["BrowserOption"]:
        """
        Returns the current BrowserOption used to initialize the browser, or None if not set.

        Returns:
            Optional[BrowserOption]: The browser options if initialized, None otherwise.

        Example:
            ```python
            create_result = await agent_bay.create()
            session = create_result.session
            browser_option = BrowserOption(use_stealth=True)
            await session.browser.initialize(browser_option)
            current_options = session.browser.get_option()
            print(f"Stealth mode: {current_options.use_stealth}")
            await session.delete()
            ```
        """
        return self._option

    def is_initialized(self) -> bool:
        """
        Returns True if the browser was initialized, False otherwise.

        Returns:
            bool: True if browser is initialized, False otherwise.

        Example:
            ```python
            create_result = await agent_bay.create()
            session = create_result.session
            print(f"Initialized: {session.browser.is_initialized()}")
            browser_option = BrowserOption()
            await session.browser.initialize(browser_option)
            print(f"Initialized: {session.browser.is_initialized()}")
            await session.delete()
            ```
        """
        return self._initialized
