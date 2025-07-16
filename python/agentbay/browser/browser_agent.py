import asyncio
import json
import re
from typing import List, Dict, Union, Any, Optional, Tuple, TypeVar, Generic, Type
from pydantic import BaseModel

from agentbay.exceptions import BrowserError
from agentbay.api.models import CallMcpToolRequest

T = TypeVar('T', bound=BaseModel)

class ActOptions:
    """
    Options for configuring the behavior of the act method.
    """
    def __init__(self, action: str, timeoutMS: Optional[int] = None, iframes: Optional[bool] = None, domSettleTimeoutMS: Optional[int] = None):
        self.action = action
        self.timeoutMS = timeoutMS
        self.iframes = iframes
        self.domSettleTimeoutMS = domSettleTimeoutMS

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
    def __init__(self, instruction: str, returnActions: Optional[int] = None, iframes: Optional[bool] = None, domSettleTimeoutMS: Optional[int] = None):
        self.instruction = instruction
        self.returnActions = returnActions
        self.iframes = iframes
        self.domSettleTimeoutMS = domSettleTimeoutMS

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
                 selector: Optional[str] = None,
                 iframe: Optional[bool] = None,
                 domSettleTimeoutsMS: Optional[int] = None):
        self.instruction = instruction
        self.schema = schema
        self.selector = selector
        self.iframe = iframe
        self.domSettleTimeoutsMS = domSettleTimeoutsMS

class BrowserAgent:
    """
    BrowserAgent handles browser automation and agent logic.
    """
    def __init__(self, session, browser):
        self.session = session
        self.browser = browser

    def act(self, page, options: ActOptions) -> 'ActResult':
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
                "action": options.action,
            }
            if options.timeoutMS is not None:
                args["timeout_ms"] = options.timeoutMS
            if options.iframes is not None:
                args["iframes"] = options.iframes
            if options.domSettleTimeoutMS is not None:
                args["dom_settle_timeout_ms"] = options.domSettleTimeoutMS
            response = self.call_mcp_tool("page_use_act", args)
            print("Response from CallMcpTool - page_use_act:", response)
            import json as _json
            if isinstance(response, str):
                data = _json.loads(response)
            else:
                data = response
            # Map snake_case keys to ActResult members
            success = data.get("success", False)
            message = data.get("message", "")
            action = data.get("action", "")
            return ActResult(success=success, message=message, action=action)
        except Exception as e:
            raise BrowserError(f"Failed to get page/context index: {e}")

    async def act_async(self, page, options: ActOptions) -> 'ActResult':
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
                "action": options.action,
            }
            if options.timeoutMS is not None:
                args["timeout_ms"] = options.timeoutMS
            if options.iframes is not None:
                args["iframes"] = options.iframes
            if options.domSettleTimeoutMS is not None:
                args["dom_settle_timeout_ms"] = options.domSettleTimeoutMS
            response = self.call_mcp_tool("page_use_act", args)
            print("Response from CallMcpTool - page_use_act:", response)
            import json as _json
            if isinstance(response, str):
                data = _json.loads(response)
            else:
                data = response
            # Map snake_case keys to ActResult members
            success = data.get("success", False)
            message = data.get("message", "")
            action = data.get("action", "")
            return ActResult(success=success, message=message, action=action)
        except Exception as e:
            raise BrowserError(f"Failed to get page/context index: {e}")

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
            if options.domSettleTimeoutMS is not None:
                args["dom_settle_timeout_ms"] = options.domSettleTimeoutMS
            response = self.call_mcp_tool("page_use_observe", args)
            print("Response from CallMcpTool - page_use_observe:", response)
            import json as _json
            if isinstance(response, str):
                data = _json.loads(response)
            else:
                raise BrowserError("Observe response data is not a json!!!")
     
            results = []
            observeResults = json.loads(data.get("observe_result", ""))
            print("observeResults =", observeResults)
            
            # Check if observe was successful
            success = data.get("success", False)
            
            for item in observeResults:
                selector = item.get("selector", "")
                description = item.get("description", "")
                method = item.get("method", "")
                arguments = item.get("arguments", {})
                results.append(ObserveResult(selector, description, method, arguments))
            
            return success, results
        except Exception as e:
            raise BrowserError(f"Failed to get page/context index: {e}")

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
            if options.domSettleTimeoutMS is not None:
                args["dom_settle_timeout_ms"] = options.domSettleTimeoutMS
            response = self.call_mcp_tool("page_use_observe", args)
            print("Response from CallMcpTool - page_use_observe:", response)
            import json as _json
            if isinstance(response, str):
                data = _json.loads(response)
            else:
                raise BrowserError("Observe response data is not a json!!!")
     
            results = []
            observeResults = json.loads(data.get("observe_result", ""))
            print("observeResults =", observeResults)
            
            # Check if observe was successful
            success = data.get("success", False)
            
            for item in observeResults:
                selector = item.get("selector", "")
                description = item.get("description", "")
                method = item.get("method", "")
                arguments = item.get("arguments", {})
                results.append(ObserveResult(selector, description, method, arguments))
            
            return success, results
        except Exception as e:
            raise BrowserError(f"Failed to get page/context index: {e}")

    

    def extract(self, page, options: ExtractOptions) -> Tuple[bool, List[T]]:
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
            if options.selector is not None:
                args["selector"] = options.selector
            if options.iframe is not None:
                args["iframe"] = options.iframe
            if options.domSettleTimeoutsMS is not None:
                args["dom_settle_timeouts_ms"] = options.domSettleTimeoutsMS

            response = self.call_mcp_tool("page_use_extract", args)
            print("Response from CallMcpTool - page_use_extract:", response)
            import json as _json
            if isinstance(response, str):
                data = _json.loads(response)
            else:
                data = response
            print("extract data =", data)
            success = data.get("success", False)
            extract_objs = []
            if success:
                extract_results = json.loads(data.get("extract_result", ""))
                for extract_result in extract_results:
                    print("extract_result =", extract_result)
                    extract_objs.append(options.schema.model_validate(extract_result))
            else:
                extract_results = data.get("extract_result", "")
                print("Extract failed due to: ", extract_results)
            return success, extract_objs
        except Exception as e:
            raise BrowserError(f"Failed to get page/context index: {e}")

    async def extract_async(self, page, options: ExtractOptions) -> Tuple[bool, List[T]]:
        """
        Async version of extract method for extracting information from the given Playwright Page object.
        Gets the page and context index and calls the MCP tool 'page_use_extract' asynchronously.
        """
        if not self.browser.is_initialized():
            raise BrowserError("Browser must be initialized before calling extract_async.")
        try:
            page_index, context_index = await self._get_page_and_context_index_async(page)
            args = {
                "context_id": context_index,
                "page_id": page_index,
                "instruction": options.instruction,
                "schema": 'schema: ' + json.dumps(options.schema.model_json_schema())
            }
            print(f"Extracting from page: {page}, page_index: {page_index}, context_index: {context_index}, args: {args}")
            if options.selector is not None:
                args["selector"] = options.selector
            if options.iframe is not None:
                args["iframe"] = options.iframe
            if options.domSettleTimeoutsMS is not None:
                args["dom_settle_timeouts_ms"] = options.domSettleTimeoutsMS

            response = self.call_mcp_tool("page_use_extract", args)
            print("Response from CallMcpTool - page_use_extract:", response)
            import json as _json
            if isinstance(response, str):
                data = _json.loads(response)
            else:
                data = response
            print("extract data =", data)
            success = data.get("success", False)
            extract_objs = []
            if success:
                extract_results = json.loads(data.get("extract_result", ""))
                for extract_result in extract_results:
                    print("extract_result =", extract_result)
                    extract_objs.append(options.schema.model_validate(extract_result))
            else:
                extract_results = data.get("extract_result", "")
                print("Extract failed due to: ", extract_results)
            return success, extract_objs
        except Exception as e:
            raise BrowserError(f"Failed to get page/context index: {e}")  

    def call_mcp_tool(self, name: str, args: dict):
        """
        Call an MCP tool and handle errors.
        Args:
            name (str): The name of the tool to call.
            args (dict): Arguments to pass to the tool.
        Returns:
            Any: The response from the tool.
        Raises:
            BrowserError: If the tool call fails.
        """
        try:
            args_json = json.dumps(args, ensure_ascii=False)
            request = CallMcpToolRequest(
                authorization=f"Bearer {self.session.get_api_key()}",
                session_id=self.session.get_session_id(),
                name=name,
                args=args_json,
            )
            response = self.session.get_client().call_mcp_tool(request)
            response_map = response.to_map()
            if not response_map:
                raise BrowserError("Invalid response format")
            body = response_map.get("body", {})
            if not body:
                raise BrowserError("Invalid response body")
            return self._parse_response_body(body)
        except Exception as e:
            raise BrowserError(f"Failed to call MCP tool {name}: {e}")

    def _parse_response_body(self, body: Dict[str, Any]) -> Any:
        """
        Parses the response body from the MCP tool.

        Args:
            body (Dict[str, Any]): The response body.

        Returns:
            Any: The parsed content.

        Raises:
            BrowserError: If the response contains errors or is invalid.
        """
        try:
            if body.get("Data", {}).get("isError", False):
                error_content = body.get("Data", {}).get("content", [])
                print("error_content =", error_content)
                error_message = "; ".join(
                    item.get("text", "Unknown error")
                    for item in error_content
                    if isinstance(item, dict)
                )
                raise BrowserError(f"Error in response: {error_message}")

            response_data = body.get("Data", {})
            if not response_data:
                raise BrowserError("No data field in response")

            # Handle 'content' field for other methods
            content = response_data.get("content", [])
            if not content or not isinstance(content, list):
                raise BrowserError("No content found in response")

            content_item = content[0]
            json_text = content_item.get("text")
            return json_text
        except Exception as e:
            raise BrowserError(f"{e}")

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
        try:
            cdp_session = page.context.new_cdp_session(page)
            target_info = cdp_session.send("Target.getTargetInfo")
            page_index = target_info["targetInfo"]["targetId"]
            cdp_session.detach()
            if hasattr(page.context.browser, "contexts"):
                context_index = page.context.browser.contexts.index(page.context)
            else:
                context_index = 0
            return page_index, context_index
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
            return page_index, context_index
        except Exception as e:
            raise BrowserError(f"Failed to get page/context index: {e}")