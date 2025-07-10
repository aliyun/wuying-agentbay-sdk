import json
from typing import Any, Dict

from agentbay.api.models import CallMcpToolRequest
from agentbay.exceptions import AgentBayError
from agentbay.model import OperationResult, extract_request_id


class BaseService:
    """
    Base service class that provides common functionality for all service classes.
    This class implements the common methods for calling MCP tools and parsing
    responses.
    """

    def __init__(self, session):
        """
        Initialize a BaseService object.

        Args:
            session: The Session instance that this service belongs to.
        """
        self.session = session

    def _handle_error(self, e):
        """
        Handle and convert exceptions. This method should be overridden by subclasses
        to provide specific error handling.

        Args:
            e (Exception): The exception to handle.

        Returns:
            Exception: The handled exception.
        """
        return e

    def _call_mcp_tool(self, name: str, args: Dict[str, Any]) -> OperationResult:
        """
        Internal helper to call MCP tool and handle errors.

        Args:
            name (str): The name of the tool to call.
            args (Dict[str, Any]): The arguments to pass to the tool.

        Returns:
            OperationResult: The response from the tool with request ID.
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

            # Extract request ID
            request_id = extract_request_id(response)

            response_map = response.to_map()
            if not response_map:
                return OperationResult(
                    request_id=request_id,
                    success=False,
                    error_message="Invalid response format",
                )

            body = response_map.get("body", {})
            try:
                print("Response body:")
                print(json.dumps(body, ensure_ascii=False, indent=2))
            except Exception:
                print(f"Response: {body}")
            if not body:
                return OperationResult(
                    request_id=request_id,
                    success=False,
                    error_message="Invalid response body",
                )

            result = self._parse_response_body(body)
            return OperationResult(request_id=request_id, success=True, data=result)

        except AgentBayError as e:
            handled_error = self._handle_error(e)
            request_id = "" if "request_id" not in locals() else request_id
            return OperationResult(
                request_id=request_id,
                success=False,
                error_message=str(handled_error),
            )
        except Exception as e:
            handled_error = self._handle_error(e)
            request_id = "" if "request_id" not in locals() else request_id
            return OperationResult(
                request_id=request_id,
                success=False,
                error_message=f"Failed to call MCP tool {name}: {handled_error}",
            )

    def _parse_response_body(
        self, body: Dict[str, Any], parse_json: bool = False
    ) -> Any:
        """
        Parses the response body from the MCP tool.

        Args:
            body (Dict[str, Any]): The response body.
            parse_json (bool, optional): Whether to parse the text as JSON.
            Defaults to False.

        Returns:
            Any: The parsed content. If parse_json is True, returns the parsed
                 JSON object; otherwise returns the raw text.


        Raises:
            AgentBayError: If the response contains errors or is invalid.
        """
        try:
            if body.get("Data", {}).get("isError", False):
                error_content = body.get("Data", {}).get("content", [])
                try:
                    print("error_content =")
                    print(json.dumps(error_content, ensure_ascii=False, indent=2))
                except Exception:
                    print(f"error_content: {error_content}")
                error_message = "; ".join(
                    item.get("text", "Unknown error")
                    for item in error_content
                    if isinstance(item, dict)
                )
                raise AgentBayError(f"Error in response: {error_message}")

            response_data = body.get("Data", {})
            if not response_data:
                raise AgentBayError("No data field in response")

            # Handle 'content' field for other methods
            content = response_data.get("content", [])
            if not content or not isinstance(content, list):
                raise AgentBayError("No content found in response")

            content_item = content[0]
            text_string = content_item.get("text")

            # Allow text field to be empty string
            if text_string is None:
                raise AgentBayError("Text field not found in response")

            return text_string

        except AgentBayError as e:
            # Transform AgentBayError to the expected type
            handled_error = self._handle_error(e)
            raise handled_error
        except Exception as e:
            # Transform AgentBayError to the expected type
            handled_error = self._handle_error(
                AgentBayError(f"Error parsing response body: {e}")
            )
            raise handled_error
