import json
from typing import Optional, Dict, Any

from agentbay.api.models import CallMcpToolRequest
from agentbay.exceptions import OssError


class Oss:
    """
    Handles Object Storage Service operations in the AgentBay cloud environment.
    """

    def __init__(self, session):
        """
        Initialize an Oss object.

        Args:
            session: The Session instance that this Oss belongs to.
        """
        self.session = session

    def _call_mcp_tool(self, name: str, args: Dict[str, Any]) -> Any:
        """
        Internal helper to call MCP tool and handle errors.

        Args:
            name (str): The name of the tool to call.
            args (Dict[str, Any]): The arguments to pass to the tool.

        Returns:
            Any: The response from the tool.

        Raises:
            OssError: If the tool call fails.
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
                raise OssError("Invalid response format")
            body = response_map.get("body", {})
            print("response_map =", response_map)
            if not body:
                raise OssError("Invalid response body")
            return self._parse_response_body(body)
        except (KeyError, TypeError, ValueError) as e:
            raise OssError(f"Failed to parse MCP tool response: {e}")
        except Exception as e:
            raise OssError(f"Failed to call MCP tool {name}: {e}")

    def _parse_response_body(self, body: Dict[str, Any]) -> Any:
        """
        Parses the response body from the MCP tool.

        Args:
            body (Dict[str, Any]): The response body.

        Returns:
            Any: The parsed content.

        Raises:
            OssError: If the response contains errors or is invalid.
        """
        try:
            if body.get("Data", {}).get("isError", True):
                error_content = body.get("Data", {}).get("content", [])
                print("error_content =", error_content) 
                error_message = "; ".join(
                    item.get("text", "Unknown error")
                    for item in error_content
                    if isinstance(item, dict)
                )
                raise OssError(f"Error in response: {error_message}")
            response_data = body.get("Data", {})
            if not response_data:
                raise OssError("No data field in response")
            content = response_data.get("content", [])
            if not content or not isinstance(content, list):
                raise OssError("No content found in response")
            content_item = content[0]
            json_text = content_item.get("text")
            return json_text
        except Exception as e:
            raise OssError(f"{e}")

    def env_init(self, access_key_id: str, access_key_secret: str, securityToken: Optional[str] =
                        None, endpoint: Optional[str] = None, region: Optional[str] = None) -> str:
        """
        Create an OSS client with the provided credentials.

        Args:
            access_key_id: The Access Key ID for OSS authentication.
            access_key_secret: The Access Key Secret for OSS authentication.
            endpoint: The OSS service endpoint. If not specified, the default is used.
            region: The OSS region. If not specified, the default is used.

        Returns:
            str: The result of the client creation operation.

        Raises:
            OssError: If the client creation fails.
        """
        try:
            args = {
                "access_key_id": access_key_id,
                "access_key_secret": access_key_secret,
                "security_token":    securityToken,
            }

            # Add optional parameters if provided
            if endpoint:
                args["endpoint"] = endpoint
            if region:
                args["region"] = region

            response = self._call_mcp_tool("oss_env_init", args)
            print("response =", response)

            if not isinstance(response, str):
                raise OssError("result field not found or not a string")

            return response
        except OssError:
            raise
        except Exception as e:
            raise OssError(f"Failed to create OSS client: {e}")

    def upload(self, bucket: str, object: str, path: str) -> str:
        """
        Upload a local file or directory to OSS.

        Args:
            bucket: OSS bucket name.
            object: Object key in OSS.
            path: Local file or directory path to upload.

        Returns:
            str: The result of the upload operation.

        Raises:
            OssError: If the upload fails.
        """
        try:
            args = {
                "bucket": bucket,
                "object": object,
                "path": path
            }

            response = self._call_mcp_tool("oss_upload", args)
            print("response =", response)

            if not isinstance(response, str):
                raise OssError("result field not found or not a string")

            return response
        except OssError:
            raise
        except Exception as e:
            raise OssError(f"Failed to upload to OSS: {e}")

    def upload_anonymous(self, url: str, path: str) -> str:
        """
        Upload a local file or directory to a URL anonymously.

        Args:
            url: The HTTP/HTTPS URL to upload the file to.
            path: Local file or directory path to upload.

        Returns:
            str: The result of the upload operation.

        Raises:
            OssError: If the upload fails.
        """
        try:
            args = {
                "url": url,
                "path": path
            }

            response = self._call_mcp_tool("oss_upload_annon", args)
            print("response =", response)

            if not isinstance(response, str):
                raise OssError("result field not found or not a string")

            return response
        except OssError:
            raise
        except Exception as e:
            raise OssError(f"Failed to upload anonymously: {e}")

    def download(self, bucket: str, object: str, path: str) -> str:
        """
        Download an object from OSS to a local file.

        Args:
            bucket: OSS bucket name.
            object: Object key in OSS.
            path: Local path to save the downloaded file.

        Returns:
            str: The result of the download operation.

        Raises:
            OssError: If the download fails.
        """
        try:
            args = {
                "bucket": bucket,
                "object": object,
                "path": path
            }

            response = self._call_mcp_tool("oss_download", args)
            print("response =", response)

            if not isinstance(response, str):
                raise OssError("result field not found or not a string")

            return response
        except OssError:
            raise
        except Exception as e:
            raise OssError(f"Failed to download from OSS: {e}")

    def download_anonymous(self, url: str, path: str) -> str:
        """
        Download a file from a URL anonymously to a local file.

        Args:
            url: The HTTP/HTTPS URL to download the file from.
            path: The full local file path to save the downloaded file.

        Returns:
            str: The result of the download operation.

        Raises:
            OssError: If the download fails.
        """
        try:
            args = {
                "url": url,
                "path": path
            }

            response = self._call_mcp_tool("oss_download_annon", args)
            print("response =", response)

            if not isinstance(response, str):
                raise OssError("result field not found or not a string")

            return response
        except OssError:
            raise
        except Exception as e:
            raise OssError(f"Failed to download anonymously: {e}")
