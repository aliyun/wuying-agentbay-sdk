import json
from typing import List, Dict, Union, Any, Optional, Tuple, TypeVar, Generic, Type
from pydantic import BaseModel
from agentbay.api.base_service import BaseService, OperationResult
from agentbay.exceptions import BrowserError, AgentBayError
from agentbay.logger import get_logger

# Initialize logger for this module
logger = get_logger("browser_agent")

T = TypeVar("T", bound=BaseModel)


class ActOptions:
    """
    Options for configuring the behavior of the act method.
    """

    def __init__(
        self,
        action: str,
        timeoutMS: Optional[int] = None,
        iframes: Optional[bool] = None,
        dom_settle_timeout_ms: Optional[int] = None,
        variables: Optional[Dict[str, str]] = None,
        use_vision: Optional[bool] = None,
    ):
        self.action = action
        self.timeoutMS = timeoutMS
        self.iframes = iframes
        self.dom_settle_timeout_ms = dom_settle_timeout_ms
        self.variables = variables
        self.use_vision = use_vision


class ActResult:
    """
    Result of the act method.
    """

    def __init__(self, success: bool, message: str, action: str):
        self.success = success
        self.message = message
        self.action = action


class ObserveOptions:
    """
    Options for configuring the behavior of the observe method.
    """

    def __init__(
        self,
        instruction: str,
        iframes: Optional[bool] = None,
        dom_settle_timeout_ms: Optional[int] = None,
        use_vision: Optional[bool] = None,
    ):
        self.instruction = instruction
        self.iframes = iframes
        self.dom_settle_timeout_ms = dom_settle_timeout_ms
        self.use_vision = use_vision


class ObserveResult:
    """
    Result of the observe method.
    """

    def __init__(self, selector: str, description: str, method: str, arguments: dict):
        self.selector = selector
        self.description = description
        self.method = method
        self.arguments = arguments


class ExtractOptions(Generic[T]):
    """
    Options for configuring the behavior of the extract method.
    """

    def __init__(
        self,
        instruction: str,
        schema: Type[T],
        use_text_extract: Optional[bool] = None,
        selector: Optional[str] = None,
        iframe: Optional[bool] = None,
        dom_settle_timeout_ms: Optional[int] = None,
        use_vision: Optional[bool] = None,
    ):
        self.instruction = instruction
        self.schema = schema
        self.use_text_extract = use_text_extract
        self.selector = selector
        self.iframe = iframe
        self.dom_settle_timeout_ms = dom_settle_timeout_ms
        self.use_vision = use_vision


class BrowserAgent(BaseService):
    """
    BrowserAgent handles browser automation and agent logic.
    """

    def __init__(self, session, browser):
        self.session = session
        self.browser = browser

    def navigate(self, url: str) -> str:
        """
        Navigates a specific page to the given URL.
        This is a synchronous wrapper around `navigate_async`.

        Args:
            url: The URL to navigate to.

        Returns:
            A string indicating the result of the navigation.
        """
        if not self.browser.is_initialized():
            raise BrowserError("Browser must be initialized before calling goto.")
        try:
            args = {
                "url": url,
            }
            response = self._call_mcp_tool_timeout("page_use_navigate", args)
            if response.success:
                return response.data
            else:
                return f"Goto failed: {response.error_message}"
        except Exception as e:
            raise BrowserError(f"Failed to call goto: {e}") from e

    async def navigate_async(self, url: str) -> str:
        """
        Navigates a specific page to the given URL asynchronously.

        Args:
            url: The URL to navigate to.

        Returns:
            A string indicating the result of the navigation.
        """
        if not self.browser.is_initialized():
            raise BrowserError("Browser must be initialized before calling goto_async.")
        try:
            args = {
                "url": url,
            }
            response = self._call_mcp_tool_timeout("page_use_navigate", args)
            if response.success:
                return response.data
            else:
                return f"Goto failed: {response.error_message}"
        except Exception as e:
            raise BrowserError(f"Failed to call goto_async: {e}") from e

    def screenshot(
        self,
        page=None,
        full_page: bool = True,
        quality: int = 80,
        clip: Optional[Dict[str, float]] = None,
        timeout: Optional[int] = None,
    ) -> str:
        """
        Takes a screenshot of the specified page.

        Args:
            page (Optional[Page]): The Playwright Page object to take a screenshot of. If None,
                                   the agent's currently focused page will be used.
            full_page (bool): Whether to capture the full scrollable page.
            quality (int): The quality of the image (0-100), for JPEG format.
            clip (Optional[Dict[str, float]]): An object specifying the clipping region {x, y, width, height}.
            timeout (Optional[int]): Custom timeout for the operation in milliseconds.

        Returns:
            str: A base64 encoded data URL of the screenshot, or an error message.
        """
        if not self.browser.is_initialized():
            raise BrowserError("Browser must be initialized before calling screenshot.")
        try:
            page_id, context_id = self._get_page_and_context_index(page)
            args = {
                "context_id": context_id,
                "page_id": page_id,
                "full_page": full_page,
                "quality": quality,
            }
            if clip:
                args["clip"] = clip
            if timeout:
                args["timeout"] = timeout

            response = self._call_mcp_tool_timeout("page_use_screenshot", args)
            if response.success:
                return response.data
            else:
                return f"Screenshot failed: {response.error_message}"
        except Exception as e:
            raise BrowserError(f"Failed to call screenshot: {e}") from e

    async def screenshot_async(
        self,
        page=None,
        full_page: bool = True,
        quality: int = 80,
        clip: Optional[Dict[str, float]] = None,
        timeout: Optional[int] = None,
    ) -> str:
        """
        Asynchronously takes a screenshot of the specified page.

        Args:
            page (Optional[Page]): The Playwright Page object to take a screenshot of. If None,
                                   the agent's currently focused page will be used.
            full_page (bool): Whether to capture the full scrollable page.
            quality (int): The quality of the image (0-100), for JPEG format.
            clip (Optional[Dict[str, float]]): An object specifying the clipping region {x, y, width, height}.
            timeout (Optional[int]): Custom timeout for the operation in milliseconds.

        Returns:
            str: A base64 encoded data URL of the screenshot, or an error message.
        """
        if not self.browser.is_initialized():
            raise BrowserError(
                "Browser must be initialized before calling screenshot_async."
            )
        try:
            page_id, context_id = self._get_page_and_context_index(page)
            args = {
                "context_id": context_id,
                "page_id": page_id,
                "full_page": full_page,
                "quality": quality,
            }
            if clip:
                args["clip"] = clip
            if timeout:
                args["timeout"] = timeout

            response = self._call_mcp_tool_timeout("page_use_screenshot", args)
            if response.success:
                return response.data
            else:
                return f"Screenshot failed: {response.error_message}"
        except Exception as e:
            raise BrowserError(f"Failed to call screenshot_async: {e}") from e

    async def close_async(self) -> bool:
        """
        Asynchronously closes the remote browser agent session.
        This will terminate the browser process managed by the agent.
        """
        try:
            print("Closing remote browser agent session...")
            response = self._call_mcp_tool_timeout("page_use_close_session", args={})
            if response.success:
                print(f"Session close status: {response.data}")
                return True
            else:
                print(f"Failed to close session: {response.error_message}")
                return False
        except Exception as e:
            raise BrowserError(f"Failed to call close_async: {e}") from e

    def act(
        self,
        action_input: Union[ObserveResult, ActOptions],
        page=None,
    ) -> "ActResult":
        """
        Perform an action on a web page, using ActOptions to configure behavior.

        Args:
            page (Optional[Page]): The Playwright Page object to act on. If None, the agent's
                                   currently focused page will be used automatically.
            action_input (Union[ObserveResult, ActOptions]): The action to perform, either as a
                                                             pre-defined ObserveResult or custom ActOptions.
        Returns:
            ActResult: The result of the action.
        """
        if not self.browser.is_initialized():
            raise BrowserError("Browser must be initialized before calling act.")
        try:
            page_index, context_index = self._get_page_and_context_index(page)
            print(
                f"Acting on page: {page}, page_index: {page_index}, context_index: {context_index}"
            )
            args = {
                "context_id": context_index,
                "page_id": page_index,
            }
            if isinstance(action_input, ActOptions):
                args["action"] = action_input.action
                if action_input.variables is not None:
                    args["variables"] = action_input.variables
                if action_input.timeoutMS is not None:
                    args["timeout_ms"] = action_input.timeoutMS
                if action_input.iframes is not None:
                    args["iframes"] = action_input.iframes
                if action_input.dom_settle_timeout_ms is not None:
                    args["dom_settle_timeout_ms"] = action_input.dom_settle_timeout_ms
                if action_input.use_vision is not None:
                    args["use_vision"] = action_input.use_vision
                args["action"] = action_input.action
            elif isinstance(action_input, ObserveResult):
                action_dict = {
                    "method": action_input.method,
                    "arguments": (
                        json.loads(action_input.arguments)
                        if isinstance(action_input.arguments, str)
                        else action_input.arguments
                    ),
                }
                args["action"] = json.dumps(action_dict)
            response = self._call_mcp_tool_timeout("page_use_act", args)
            if response.success:
                logger.debug(f"Response from CallMcpTool - page_use_act: {response.data}")
                import json as _json

                if isinstance(response.data, str):
                    data = _json.loads(response.data)
                else:
                    data = response.data
                # Map snake_case keys to ActResult members
                message = data.get("message", "")
                action = data.get("action", "")
                return ActResult(success=True, message=message, action=action)
            else:
                return ActResult(
                    success=False, message=response.error_message, action=""
                )
        except Exception as e:
            raise BrowserError(f"Failed to act: {e}")

    async def act_async(
        self,
        action_input: Union[ObserveResult, ActOptions],
        page=None,
    ) -> "ActResult":
        """
        Asynchronously perform an action on a web page.

        Args:
            page (Optional[Page]): The Playwright Page object to act on. If None, the agent's
                                   currently focused page will be used automatically.
            action_input (Union[ObserveResult, ActOptions]): The action to perform.

        Returns:
            ActResult: The result of the action.
        """
        if not self.browser.is_initialized():
            raise BrowserError("Browser must be initialized before calling act_async.")
        try:
            page_index, context_index = await self._get_page_and_context_index_async(
                page
            )
            print(
                f"Acting on page: {page}, page_index: {page_index}, context_index: {context_index}"
            )
            args = {
                "context_id": context_index,
                "page_id": page_index,
            }
            if isinstance(action_input, ActOptions):
                args["action"] = action_input.action
                if action_input.variables is not None:
                    args["variables"] = action_input.variables
                if action_input.timeoutMS is not None:
                    args["timeout_ms"] = action_input.timeoutMS
                if action_input.iframes is not None:
                    args["iframes"] = action_input.iframes
                if action_input.dom_settle_timeout_ms is not None:
                    args["dom_settle_timeout_ms"] = action_input.dom_settle_timeout_ms
                if action_input.use_vision is not None:
                    args["use_vision"] = action_input.use_vision
            elif isinstance(action_input, ObserveResult):
                action_dict = {
                    "method": action_input.method,
                    "arguments": (
                        json.loads(action_input.arguments)
                        if isinstance(action_input.arguments, str)
                        else action_input.arguments
                    ),
                }
                args["action"] = json.dumps(action_dict)
            response = self._call_mcp_tool_timeout("page_use_act", args)
            if response.success:
                logger.debug(f"Response from CallMcpTool - page_use_act: {response.data}")
                import json as _json

                if isinstance(response.data, str):
                    data = _json.loads(response.data)
                else:
                    data = response.data
                # Map snake_case keys to ActResult members
                message = data.get("message", "")
                action = data.get("action", "")
                return ActResult(success=True, message=message, action=action)
            else:
                return ActResult(
                    success=False, message=response.error_message, action=""
                )
        except Exception as e:
            raise BrowserError(f"Failed to act: {e}")

    def observe(
        self,
        options: ObserveOptions,
        page=None,
    ) -> Tuple[bool, List[ObserveResult]]:
        """
        Observe elements or state on a web page.

        Args:
            page (Optional[Page]): The Playwright Page object to observe. If None, the agent's
                                   currently focused page will be used.
            options (ObserveOptions): Options to configure the observation behavior.

        Returns:
            Tuple[bool, List[ObserveResult]]: A tuple containing a success boolean and a list
                                              of observation results.
        """
        if not self.browser.is_initialized():
            raise BrowserError("Browser must be initialized before calling observe.")
        try:
            page_index, context_index = self._get_page_and_context_index(page)
            print(
                f"Observing page: {page}, page_index: {page_index}, context_index: {context_index}"
            )
            args = {
                "context_id": context_index,
                "page_id": page_index,
                "instruction": options.instruction,
            }
            if options.iframes is not None:
                args["iframes"] = options.iframes
            if options.dom_settle_timeout_ms is not None:
                args["dom_settle_timeout_ms"] = options.dom_settle_timeout_ms
            if options.use_vision is not None:
                args["use_vision"] = options.use_vision
            response = self._call_mcp_tool_timeout("page_use_observe", args)
            logger.debug(f"Response from CallMcpTool - page_use_observe: {response}")

            if response.success:
                logger.debug(f"Response from CallMcpTool - page_use_observe: {response.data}")
                import json as _json

                if isinstance(response.data, str):
                    data = _json.loads(response.data)
                else:
                    raise BrowserError("Observe response data is not a json!!!")

                results = []
                observeResults = json.loads(data.get("observe_result", ""))
                print("observeResults =", observeResults)

                for item in observeResults:
                    selector = item.get("selector", "")
                    description = item.get("description", "")
                    method = item.get("method", "")
                    arguments = item.get("arguments", {})
                    results.append(
                        ObserveResult(selector, description, method, arguments)
                    )

                return True, results
            else:
                print(
                    f"Response from CallMcpTool - page_use_observe:",
                    response.error_message,
                )
                return False, []

        except Exception as e:
            raise BrowserError(f"Failed to observe: {e}")

    async def observe_async(
        self,
        options: ObserveOptions,
        page=None,
    ) -> Tuple[bool, List[ObserveResult]]:
        """
        Asynchronously observe elements or state on a web page.

        Args:
            page (Optional[Page]): The Playwright Page object to observe. If None, the agent's
                                   currently focused page will be used.
            options (ObserveOptions): Options to configure the observation behavior.

        Returns:
            Tuple[bool, List[ObserveResult]]: A tuple containing a success boolean and a list
                                              of observation results.
        """
        if not self.browser.is_initialized():
            raise BrowserError(
                "Browser must be initialized before calling observe_async."
            )
        try:
            page_index, context_index = await self._get_page_and_context_index_async(
                page
            )
            print(
                f"Observing page: {page}, page_index: {page_index}, context_index: {context_index}"
            )
            args = {
                "context_id": context_index,
                "page_id": page_index,
                "instruction": options.instruction,
            }
            if options.iframes is not None:
                args["iframes"] = options.iframes
            if options.dom_settle_timeout_ms is not None:
                args["dom_settle_timeout_ms"] = options.dom_settle_timeout_ms
            if options.use_vision is not None:
                args["use_vision"] = options.use_vision
            response = self._call_mcp_tool_timeout("page_use_observe", args)
            logger.debug(f"Response from CallMcpTool - page_use_observe: {response}")

            if response.success:
                logger.debug(f"Response from CallMcpTool - page_use_observe: {response.data}")
                import json as _json

                if isinstance(response.data, str):
                    data = _json.loads(response.data)
                else:
                    raise BrowserError("Observe response data is not a json!!!")

                results = []
                observeResults = json.loads(data.get("observe_result", ""))
                print("observeResults =", observeResults)

                for item in observeResults:
                    selector = item.get("selector", "")
                    description = item.get("description", "")
                    method = item.get("method", "")
                    arguments_str = item.get("arguments", "{}")
                    try:
                        arguments_dict = _json.loads(arguments_str)
                    except _json.JSONDecodeError:
                        print(
                            f"Warning: Could not parse arguments as JSON: {arguments_str}"
                        )
                        arguments_dict = arguments_str
                    results.append(
                        ObserveResult(selector, description, method, arguments_dict)
                    )

                return True, results
            else:
                print(
                    f"Response from CallMcpTool - page_use_observe:",
                    response.error_message,
                )
                return False, []

        except Exception as e:
            raise BrowserError(f"Failed to observe: {e}")

    def extract(self, options: ExtractOptions, page=None) -> Tuple[bool, T]:
        """
        Extract information from a web page.

        Args:
            page (Optional[Page]): The Playwright Page object to extract from. If None, the agent's
                                   currently focused page will be used.
            options (ExtractOptions): Options to configure the extraction, including schema.

        Returns:
            Tuple[bool, T]: A tuple containing a success boolean and the extracted data as a
                            Pydantic model instance, or None on failure.
        """
        if not self.browser.is_initialized():
            raise BrowserError("Browser must be initialized before calling extract.")
        try:
            page_index, context_index = self._get_page_and_context_index(page)
            args = {
                "context_id": context_index,
                "page_id": page_index,
                "instruction": options.instruction,
                "schema": "schema: " + json.dumps(options.schema.model_json_schema()),
            }
            print(
                f"Extracting from page: {page}, page_index: {page_index}, context_index: {context_index}, args: {args}"
            )
            if options.use_text_extract is not None:
                args["use_text_extract"] = options.use_text_extract
            if options.use_vision is not None:
                args["use_vision"] = options.use_vision
            if options.selector is not None:
                args["selector"] = options.selector
            if options.iframe is not None:
                args["iframe"] = options.iframe
            if options.dom_settle_timeout_ms is not None:
                args["dom_settle_timeout_ms"] = options.dom_settle_timeout_ms

            response = self._call_mcp_tool_timeout("page_use_extract", args)
            logger.debug(f"Response from CallMcpTool - page_use_extract: {response}")

            if response.success:
                logger.debug(f"Response from CallMcpTool - page_use_extract: {response.data}")
                import json as _json

                if isinstance(response.data, str):
                    data = _json.loads(response.data)
                else:
                    data = response.data
                print("extract data =", data)
                extract_result = data.get("extract_result", "")
                print("extract_result =", extract_result)
                extract_obj = options.schema.model_validate_json(extract_result)
                return True, extract_obj
            else:
                print(
                    f"Response from CallMcpTool - page_use_extract:",
                    response.error_message,
                )
                return False, None
        except Exception as e:
            raise BrowserError(f"Failed to extract: {e}")

    async def extract_async(
        self,
        options: ExtractOptions,
        page=None,
    ) -> Tuple[bool, T]:
        """
        Asynchronously extract information from a web page.

        Args:
            page (Optional[Page]): The Playwright Page object to extract from. If None, the agent's
                                   currently focused page will be used.
            options (ExtractOptions): Options to configure the extraction, including schema.

        Returns:
            Tuple[bool, T]: A tuple containing a success boolean and the extracted data as a
                            Pydantic model instance, or None on failure.
        """
        if not self.browser.is_initialized():
            raise BrowserError(
                "Browser must be initialized before calling extract  _async."
            )
        try:
            page_index, context_index = await self._get_page_and_context_index_async(
                page
            )
            args = {
                "context_id": context_index,
                "page_id": page_index,
                "instruction": options.instruction,
                "schema": "schema: " + json.dumps(options.schema.model_json_schema()),
            }
            print(
                f"Extracting from page: {page}, page_index: {page_index}, context_index: {context_index}, args: {args}"
            )
            if options.use_text_extract is not None:
                args["use_text_extract"] = options.use_text_extract
            if options.use_vision is not None:
                args["use_vision"] = options.use_vision
            if options.selector is not None:
                args["selector"] = options.selector
            if options.iframe is not None:
                args["iframe"] = options.iframe
            if options.dom_settle_timeout_ms is not None:
                args["dom_settle_timeout_ms"] = options.dom_settle_timeout_ms

            response = self._call_mcp_tool_timeout("page_use_extract", args)
            logger.debug(f"Response from CallMcpTool - page_use_extract: {response}")

            if response.success:
                logger.debug(f"Response from CallMcpTool - page_use_extract: {response.data}")
                import json as _json

                if isinstance(response.data, str):
                    data = _json.loads(response.data)
                else:
                    data = response.data
                print("extract data =", data)
                extract_result = data.get("extract_result", "")
                print("extract_result =", extract_result)
                extract_obj = options.schema.model_validate_json(extract_result)
                return True, extract_obj
            else:
                print(
                    f"Response from CallMcpTool - page_use_extract:",
                    response.error_message,
                )
                return False, None
        except Exception as e:
            raise BrowserError(f"Failed to extract: {e}")

    def _get_page_and_context_index(self, page):
        """
        Given a Playwright Page object, return its page index within the context and the context index within the browser.
        Args:
            page: Playwright Page object
        Returns:
            (str, int): (page_index, context_index)
        Raises:
            BrowserError: If indices cannot be determined.
        """
        if page is None:
            return None, 0

        try:
            cdp_session = page.context.new_cdp_session(page)
            target_info = cdp_session.send("Target.getTargetInfo")
            page_index = target_info["targetInfo"]["targetId"]
            cdp_session.detach()
            if hasattr(page.context.browser, "contexts"):
                context_index = page.context.browser.contexts.index(page.context)
            else:
                context_index = 0
            return page_index, 0
        except Exception as e:
            raise BrowserError(f"Failed to get page/context index: {e}")

    async def _get_page_and_context_index_async(self, page):
        """
        Async version of _get_page_and_context_index for getting page and context indices asynchronously.
        Args:
            page: Playwright Page object
        Returns:
            (str, int): (page_index, context_index)
        Raises:
            BrowserError: If indices cannot be determined.
        """
        if page is None:
            return None, 0
        try:
            cdp_session = await page.context.new_cdp_session(page)
            target_info = await cdp_session.send("Target.getTargetInfo")
            page_index = target_info["targetInfo"]["targetId"]
            await cdp_session.detach()
            if hasattr(page.context.browser, "contexts"):
                context_index = page.context.browser.contexts.index(page.context)
            else:
                context_index = 0
            return page_index, 0
        except Exception as e:
            raise BrowserError(f"Failed to get page/context index: {e}")

    def _handle_error(self, e):
        """
        Handle and convert exceptions. This method should be overridden by subclasses
        to provide specific error handling.

        Args:
            e (Exception): The exception to handle.

        Returns:
            Exception: The handled exception.
        """
        if isinstance(e, BrowserError):
            return e
        if isinstance(e, AgentBayError):
            return BrowserError(str(e))
        return e

    def _call_mcp_tool_timeout(
        self, name: str, args: Dict[str, Any]
    ) -> OperationResult:
        """
        Call MCP tool with timeout.
        """
        return self._call_mcp_tool(
            name, args, read_timeout=60000, connect_timeout=60000
        )
