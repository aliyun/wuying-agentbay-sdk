from typing import TYPE_CHECKING, Optional, Literal
import asyncio
import time
from agentbay.api.models import InitBrowserRequest
from agentbay.browser.browser_agent import BrowserAgent
from agentbay.api.base_service import BaseService
from agentbay.exceptions import BrowserError
from agentbay.config import BROWSER_DATA_PATH

if TYPE_CHECKING:
    from agentbay.session import Session

class BrowserViewport:
    """
    Browser viewport options.
    """
    def __init__(self, width: int = 1920, height: int = 1080):
        self.width = width
        self.height = height

    def to_map(self):
        viewport_map = dict()
        if self.width is not None:
            viewport_map['width'] = self.width
        if self.height is not None:
            viewport_map['height'] = self.height
        return viewport_map

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('width') is not None:
            self.width = m.get('width')
        if m.get('height') is not None:
            self.height = m.get('height')
        return self

class BrowserScreen:
    """
    Browser screen options.
    """
    def __init__(self, width: int = 1920, height: int = 1080):
        self.width = width
        self.height = height

    def to_map(self):
        screen_map = dict()
        if self.width is not None:
            screen_map['width'] = self.width
        if self.height is not None:
            screen_map['height'] = self.height
        return screen_map

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('width') is not None:
            self.width = m.get('width')
        if m.get('height') is not None:
            self.height = m.get('height')
        return self

class BrowserFingerprint:
    """
    Browser fingerprint options.
    """
    def __init__(
        self,
        devices: list[Literal["desktop", "mobile"]] = None,
        operating_systems: list[Literal["windows", "macos", "linux", "android", "ios"]] = None,
        locales: list[str] = None
    ):
        self.devices = devices
        self.operating_systems = operating_systems
        self.locales = locales

    def to_map(self):
        fingerprint_map = dict()
        if self.devices is not None:
            fingerprint_map['devices'] = self.devices
        if self.operating_systems is not None:
            fingerprint_map['operatingSystems'] = self.operating_systems
        if self.locales is not None:
            fingerprint_map['locales'] = self.locales
        return fingerprint_map

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('devices') is not None:
            self.devices = m.get('devices')
        if m.get('operatingSystems') is not None:
            self.operating_systems = m.get('operatingSystems')
        if m.get('locales') is not None:
            self.locales = m.get('locales')
        return self

class BrowserOption:
    """
    browser initialization options.
    """
    def __init__(
        self,
        use_stealth: bool = False,
        user_agent: str = None,
        viewport: BrowserViewport = None,
        screen: BrowserScreen = None,
        fingerprint: BrowserFingerprint = None,
    ):
        self.use_stealth = use_stealth
        self.user_agent = user_agent
        self.viewport = viewport
        self.screen = screen
        self.fingerprint = fingerprint

    def to_map(self):
        option_map = dict()
        if self.use_stealth is not None:
            option_map['useStealth'] = self.use_stealth
        if self.user_agent is not None:
            option_map['userAgent'] = self.user_agent
        if self.viewport is not None:
            option_map['viewport'] = self.viewport.to_map()
        if self.screen is not None:
            option_map['screen'] = self.screen.to_map()
        if self.fingerprint is not None:
            option_map['fingerprint'] = self.fingerprint.to_map()
        return option_map

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('useStealth') is not None:
            self.use_stealth = m.get('useStealth')
        else:
            self.use_stealth = False
        if m.get('userAgent') is not None:
            self.user_agent = m.get('userAgent')
        if m.get('viewport') is not None:
            self.viewport = BrowserViewport.from_map(m.get('viewport'))
        if m.get('screen') is not None:
            self.screen = BrowserScreen.from_map(m.get('screen'))
        if m.get('fingerprint') is not None:
            self.fingerprint = BrowserFingerprint.from_map(m.get('fingerprint'))
        return self

class Browser(BaseService):
    """
    Browser provides browser-related operations for the session.
    """
    def __init__(self, session: "Session"):
        self.session = session
        self._endpoint_url = None
        self._initialized = False
        self._option = None
        self.agent = BrowserAgent(self.session, self)

    def initialize(self, option: "BrowserOption") -> bool:
        """
        Initialize the browser instance with the given options.
        Returns True if successful, False otherwise.
        """
        if self.is_initialized():
            return True
        try:
            request = InitBrowserRequest(
                authorization=f"Bearer {self.session.get_api_key()}",
                session_id=self.session.get_session_id(),
                persistent_path=BROWSER_DATA_PATH,
                browser_option=option.to_map(),
            )
            response = self.session.get_client().init_browser(request)
            
            print(f"Response from init_browser: {response}")
            response_map = response.to_map()
            body = response_map.get("body", {})
            data = body.get("Data", {})
            success = data.get("Port") is not None
            if success:
                self._initialized = True
                self._option = option
                print("Browser instance was successfully initialized.")

            return success
        except Exception as e:
            print("Failed to initialize browser instance:", e)
            self._initialized = False
            self._endpoint_url = None
            self._option = None
            return False

    async def initialize_async(self, option: "BrowserOption") -> bool:
        """
        Initialize the browser instance with the given options asynchronously.
        Returns True if successful, False otherwise.
        """
        if self.is_initialized():
            return True
        try:
            request = InitBrowserRequest(
                authorization=f"Bearer {self.session.get_api_key()}",
                session_id=self.session.get_session_id(),
                persistent_path=BROWSER_DATA_PATH,
                browser_option=option.to_map(),
            )
            response = await self.session.get_client().init_browser_async(request)
            print(f"Response from init_browser: {response}")
            response_map = response.to_map()
            body = response_map.get("body", {})
            data = body.get("Data", {})
            success = data.get("Port") is not None
            if success:
                self._initialized = True
                self._option = option
                print("Browser instance successfully initialized")
            return success
        except Exception as e:
            print("Failed to initialize browser instance:", e)
            self._initialized = False
            self._endpoint_url = None
            self._option = None
            return False

    def _stop_browser(self):
        """
        Stop the browser instance, internal use only.
        """
        if self.is_initialized():
            self._call_mcp_tool("stopChrome", {})
        else:
            raise BrowserError("Browser is not initialized. Cannot stop browser.")

    def get_endpoint_url(self) -> str:
        """
        Returns the endpoint URL if the browser is initialized, otherwise raises an exception.
        When initialized, always fetches the latest CDP url from session.get_link().
        """
        if not self.is_initialized():
            raise BrowserError("Browser is not initialized. Cannot access endpoint URL.")
        try:
            cdp_url = self.session.get_link()
            self._endpoint_url = cdp_url.data
            return self._endpoint_url
        except Exception as e:
            raise BrowserError(f"Failed to get endpoint URL from session: {e}")

    def get_option(self) -> Optional["BrowserOption"]:
        """
        Returns the current BrowserOption used to initialize the browser, or None if not set.
        """
        return self._option

    def is_initialized(self) -> bool:
        """
        Returns True if the browser was initialized, False otherwise.
        """
        return self._initialized
