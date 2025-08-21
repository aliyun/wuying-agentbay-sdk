import asyncio
import json
import re
from typing import List, Dict, Union, Any, Optional, Tuple, TypeVar, Generic, Type
from pydantic import BaseModel
from agentbay.api.base_service import BaseService, OperationResult
from agentbay.exceptions import BrowserError, AgentBayError
from agentbay.api.models import CallMcpToolRequest

T = TypeVar('T', bound=BaseModel)

class ActOptions:
    """
    Options for configuring the behavior of the act method.
    """
    def __init__(self, action: str, timeoutMS: Optional[int] = None, iframes: Optional[bool] = None, dom_settle_timeout_ms: Optional[int] = None):
        self.action = action
        self.timeoutMS = timeoutMS
        self.iframes = iframes
        self.dom_settle_timeout_ms = dom_settle_timeout_ms

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
    def __init__(self, instruction: str, returnActions: Optional[int] = None, iframes: Optional[bool] = None, dom_settle_timeout_ms: Optional[int] = None):
        self.instruction = instruction
        self.returnActions = returnActions
        self.iframes = iframes
        self.dom_settle_timeout_ms = dom_settle_timeout_ms

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
    def __init__(self,
                 instruction: str,
                 schema: Type[T],
                 use_text_extract: Optional[bool] = None,
                 selector: Optional[str] = None,
                 iframe: Optional[bool] = None,
                 dom_settle_timeout_ms: Optional[int] = None):
        self.instruction = instruction
        self.schema = schema
        self.use_text_extract = use_text_extract
        self.selector = selector
        self.iframe = iframe
        self.dom_settle_timeout_ms = dom_settle_timeout_ms

class BrowserAgent(BaseService):
    """
    BrowserAgent handles browser automation and agent logic.
    """
    def __init__(self, session, browser):
        self.session = session
        self.browser = browser

    def act(self, page, action_input: Union[ObserveResult, ActOptions]) -> 'ActResult':
        """
        Perform an action on the given Playwright Page object, using ActOptions to configure behavior.
        Also gets the page index and corresponding context index.
        Returns:
            ActResult: The result of the action.
        """
        if not self.browser.is_initialized():
            raise BrowserError("Browser must be initialized before calling act.")
        try:
            page_index, context_index = self._get_page_and_context_index(page)
            print(f"Acting on page: {page}, page_index: {page_index}, context_index: {context_index}")
            args = {
                "context_id": context_index,
                "page_id": page_index,
            }
            if isinstance(action_input, ActOptions):
                if action_input.timeoutMS is not None:
                    args["timeout_ms"] = action_input.timeoutMS
                if action_input.iframes is not None:
                    args["iframes"] = action_input.iframes
                if action_input.dom_settle_timeout_ms is not None:
                    args["dom_settle_timeout_ms"] = action_input.dom_settle_timeout_ms
                args["action"] = action_input.action
            elif isinstance(action_input, ObserveResult):
                action_dict = {
                    "method": action_input.method,
                    "arguments": json.loads(action_input.arguments) if isinstance(action_input.arguments, str) else action_input.arguments
                }
                args["action"] = json.dumps(action_dict)
            response = self._call_mcp_tool_timeout("page_use_act", args)
            if response.success:
                print(f"Response from CallMcpTool - page_use_act:", response.data)
                import json as _json
                if isinstance(response.data, str):
                    data = _json.loads(response.data)
                else:
                    data = response.data
                # Map snake_case keys to ActResult members
                success = data.get("success", False)
                message = data.get("message", "")
                action = data.get("action", "")
                return ActResult(success=success, message=message, action=action)
            else:
                return ActResult(success=False, message=response.error_message, action="")
        except Exception as e:
            raise BrowserError(f"Failed to act: {e}")

    async def act_async(self, page, action_input: Union[ObserveResult, ActOptions]) -> 'ActResult':
        """
        Async version of act method for performing actions on the given Playwright Page object.
        Gets the page index and corresponding context index asynchronously.
        Returns:
            ActResult: The result of the action.
        """
        if not self.browser.is_initialized():
            raise BrowserError("Browser must be initialized before calling act_async.")
        try:
            page_index, context_index = await self._get_page_and_context_index_async(page)
            print(f"Acting on page: {page}, page_index: {page_index}, context_index: {context_index}")
            args = {
                "context_id": context_index,
                "page_id": page_index,
            }
            if isinstance(action_input, ActOptions):
                args["action"] = action_input.action
                if action_input.timeoutMS is not None:
                    args["timeout_ms"] = action_input.timeoutMS
                if action_input.iframes is not None:
                    args["iframes"] = action_input.iframes
                if action_input.dom_settle_timeout_ms is not None:
                    args["dom_settle_timeout_ms"] = action_input.dom_settle_timeout_ms
            elif isinstance(action_input, ObserveResult):
                action_dict = {
                    "method": action_input.method,
                    "arguments": json.loads(action_input.arguments) if isinstance(action_input.arguments, str) else action_input.arguments
                }
                args["action"] = json.dumps(action_dict)
            response = self._call_mcp_tool_timeout("page_use_act", args)
            if response.success:
                print(f"Response from CallMcpTool - page_use_act:", response.data)
                import json as _json
                if isinstance(response.data, str):
                    data = _json.loads(response.data)
                else:
                    data = response.data
                # Map snake_case keys to ActResult members
                success = data.get("success", False)
                message = data.get("message", "")
                action = data.get("action", "")
                return ActResult(success=success, message=message, action=action)
            else:
                return ActResult(success=False, message=response.error_message, action="")
        except Exception as e:
            raise BrowserError(f"Failed to act: {e}")

    def observe(self, page, options: ObserveOptions) -> Tuple[bool, List[ObserveResult]]:
        """
        Observe elements or state on the given Playwright Page object, using ObserveOptions to configure behavior.
        Gets the page and context index and calls the MCP tool 'page_use_observe'.
        Returns:
            Tuple[bool, List[ObserveResult]]: A tuple containing (success, results) where success is a boolean
            indicating whether the observe operation succeeded, and results is a list of ObserveResult objects.
        """
        if not self.browser.is_initialized():
            raise BrowserError("Browser must be initialized before calling observe.")
        try:
            page_index, context_index = self._get_page_and_context_index(page)
            print(f"Observing page: {page}, page_index: {page_index}, context_index: {context_index}")
            args = {
                "context_id": context_index,
                "page_id": page_index,
                "instruction": options.instruction,
            }
            if options.returnActions is not None:
                args["return_actions"] = options.returnActions
            if options.iframes is not None:
                args["iframes"] = options.iframes
            if options.dom_settle_timeout_ms is not None:
                args["dom_settle_timeout_ms"] = options.dom_settle_timeout_ms
            response = self._call_mcp_tool_timeout("page_use_observe", args)
            print("Response from CallMcpTool - page_use_observe:", response)

            if response.success:
                print(f"Response from CallMcpTool - page_use_observe:", response.data)
                import json as _json
                if isinstance(response.data, str):
                    data = _json.loads(response.data)
                else:
                    raise BrowserError("Observe response data is not a json!!!")
        
                # Check if observe was successful
                success = data.get("success", False)
                if not success:
                    return False, []

                results = []
                observeResults = json.loads(data.get("observe_result", ""))
                print("observeResults =", observeResults)
                
                for item in observeResults:
                    selector = item.get("selector", "")
                    description = item.get("description", "")
                    method = item.get("method", "")
                    arguments = item.get("arguments", {})
                    results.append(ObserveResult(selector, description, method, arguments))
                
                return success, results
            else:
                print(f"Response from CallMcpTool - page_use_observe:", response.error_message)
                return False, []

        except Exception as e:
            raise BrowserError(f"Failed to observe: {e}")

    async def observe_async(self, page, options: ObserveOptions) -> Tuple[bool, List[ObserveResult]]:
        """
        Async version of observe method for observing elements or state on the given Playwright Page object.
        Gets the page and context index and calls the MCP tool 'page_use_observe' asynchronously.
        Returns:
            Tuple[bool, List[ObserveResult]]: A tuple containing (success, results) where success is a boolean
            indicating whether the observe operation succeeded, and results is a list of ObserveResult objects.
        """
        if not self.browser.is_initialized():
            raise BrowserError("Browser must be initialized before calling observe_async.")
        try:
            page_index, context_index = await self._get_page_and_context_index_async(page)
            print(f"Observing page: {page}, page_index: {page_index}, context_index: {context_index}")
            args = {
                "context_id": context_index,
                "page_id": page_index,
                "instruction": options.instruction,
            }
            if options.returnActions is not None:
                args["return_actions"] = options.returnActions
            if options.iframes is not None:
                args["iframes"] = options.iframes
            if options.dom_settle_timeout_ms is not None:
                args["dom_settle_timeout_ms"] = options.dom_settle_timeout_ms
            response = self._call_mcp_tool_timeout("page_use_observe", args)
            print("Response from CallMcpTool - page_use_observe:", response)

            if response.success:
                print(f"Response from CallMcpTool - page_use_observe:", response.data)
                import json as _json
                if isinstance(response.data, str):
                    data = _json.loads(response.data)
                else:
                    raise BrowserError("Observe response data is not a json!!!")
        
                # Check if observe was successful
                success = data.get("success", False)
                if not success:
                    return False, []

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
                        print(f"Warning: Could not parse arguments as JSON: {arguments_str}")
                        arguments_dict = arguments_str
                    results.append(ObserveResult(selector, description, method, arguments_dict))
                
                return success, results
            else:
                print(f"Response from CallMcpTool - page_use_observe:", response.error_message)
                return False, []
                
        except Exception as e:
            raise BrowserError(f"Failed to observe: {e}")

    def extract(self, page, options: ExtractOptions) -> Tuple[bool, T]:
        """
        Extract information from the given Playwright Page object.
        Gets the page and context index and calls the MCP tool 'page_use_extract'.
        """
        if not self.browser.is_initialized():
            raise BrowserError("Browser must be initialized before calling extract.")
        try:
            page_index, context_index = self._get_page_and_context_index(page)
            args = {
                "context_id": context_index,
                "page_id": page_index,
                "instruction": options.instruction,
                "schema": 'schema: ' + json.dumps(options.schema.model_json_schema())
            }
            print(f"Extracting from page: {page}, page_index: {page_index}, context_index: {context_index}, args: {args}")
            if options.use_text_extract is not None:
                args["use_text_extract"] = options.use_text_extract
            if options.selector is not None:
                args["selector"] = options.selector
            if options.iframe is not None:
                args["iframe"] = options.iframe
            if options.dom_settle_timeout_ms is not None:
                args["dom_settle_timeout_ms"] = options.dom_settle_timeout_ms

            response = self._call_mcp_tool_timeout("page_use_extract", args)
            print("Response from CallMcpTool - page_use_extract:", response)

            if response.success:
                print(f"Response from CallMcpTool - page_use_extract:", response.data)
                import json as _json
                if isinstance(response.data, str):
                    data = _json.loads(response.data)
                else:
                    data = response.data
                print("extract data =", data)
                success = data.get("success", False)
                extract_result = data.get("extract_result", "")
                print("extract_result =", extract_result)
                extract_obj = None
                if success:
                    extract_obj = options.schema.model_validate_json(extract_result)
                else:
                    print(f"Extract failed due to: {extract_result}")
                return success, extract_obj
            else:
                print(f"Response from CallMcpTool - page_use_extract:", response.error_message)
                return False, None
        except Exception as e:
            raise BrowserError(f"Failed to extract: {e}")

    async def extract_async(self, page, options: ExtractOptions) -> Tuple[bool, T]:
        """
        Async version of extract method for extracting information from the given Playwright Page object.
        Gets the page and context index and calls the MCP tool 'page_use_extract' asynchronously.
        """
        if not self.browser.is_initialized():
            raise BrowserError("Browser must be initialized before calling extract  _async.")
        try:
            page_index, context_index = await self._get_page_and_context_index_async(page)
            args = {
                "context_id": context_index,
                "page_id": page_index,
                "instruction": options.instruction,
                "schema": 'schema: ' + json.dumps(options.schema.model_json_schema())
            }
            print(f"Extracting from page: {page}, page_index: {page_index}, context_index: {context_index}, args: {args}")
            if options.use_text_extract is not None:
                args["use_text_extract"] = options.use_text_extract
            if options.selector is not None:
                args["selector"] = options.selector
            if options.iframe is not None:
                args["iframe"] = options.iframe
            if options.dom_settle_timeout_ms is not None:
                args["dom_settle_timeout_ms"] = options.dom_settle_timeout_ms

            response = self._call_mcp_tool_timeout("page_use_extract", args)
            print("Response from CallMcpTool - page_use_extract:", response)

            if response.success:
                print(f"Response from CallMcpTool - page_use_extract:", response.data)
                import json as _json
                if isinstance(response.data, str):
                    data = _json.loads(response.data)
                else:
                    data = response.data
                print("extract data =", data)
                success = data.get("success", False)
                extract_result = data.get("extract_result", "")
                print("extract_result =", extract_result)
                extract_obj = None
                if success:
                    extract_obj = options.schema.model_validate_json(extract_result)
                else:
                    print(f"Extract failed due to: {extract_result}")
                return success, extract_obj
            else:
                print(f"Response from CallMcpTool - page_use_extract:", response.error_message)
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
            raise BrowserError("Page is None")
            
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

    def _call_mcp_tool_timeout(self, name: str, args: Dict[str, Any]) -> OperationResult:
        """
        Call MCP tool with timeout.
        """
        return self._call_mcp_tool(name, args, read_timeout=60000, connect_timeout=60000)