import json
import asyncio
import traceback
import os
from typing import Optional
from pydantic import Field
from langchain.tools import tool, ToolRuntime

try:
    from agentbay import AgentBay
    from agentbay import ActOptions
    AGENTBAY_AVAILABLE = True
except ImportError:
    AGENTBAY_AVAILABLE = False
    print("AgentBay SDK not available")


# Data class for browser session information
class BrowserSessionData:
    """Data class for browser session information."""
    def __init__(self, session=None, session_id=None):
        self.session = session
        self.session_id = session_id


def get_browser_session(runtime: ToolRuntime[BrowserSessionData, None]) -> Optional[object]:
    """Get browser session from runtime store.
    
    Args:
        runtime: ToolRuntime object containing store with session data
        
    Returns:
        Browser session object or None if not found
    """
    try:
        # Access session from runtime store
        store = runtime.store
        session_entry = store.get(("browser_session",), "default")
        if not session_entry:
            print("No browser session found in store")
            return None
            
        session_data = session_entry.value
        
        # Get session either directly or via session_id
        if hasattr(session_data, 'session') and session_data.session:
            session = session_data.session
        elif hasattr(session_data, 'session_id') and session_data.session_id:
            # If we have a session_id but no session object, try to re-acquire
            if AGENTBAY_AVAILABLE:
                agent_bay = AgentBay()
                session_result = agent_bay.get(session_data.session_id)
                if session_result.success:
                    session = session_result.session
                    # Update the session in store
                    session_data.session = session
                    store.put(("browser_session",), session_data, "default")
                else:
                    print(f"Failed to get session with ID {session_data.session_id}: {session_result.error_message}")
                    return None
            else:
                return None
        else:
            print("No valid session or session_id found in session_data")
            return None
            
        return session
    except Exception as e:
        print(f"Error getting browser session: {e}")
        traceback.print_exc()
        return None


@tool("browser_navigate")
async def browser_navigate(
    url: str = Field(..., description="URL to navigate to"),
    runtime: ToolRuntime[BrowserSessionData, None] = None
) -> str:
    """Navigate to a URL in the browser session"""
    print(f"[browser_navigate] Input: url={url}")
    
    try:
        if not AGENTBAY_AVAILABLE:
            response = {
                "success": False,
                "error": "AgentBay SDK not available"
            }
            print(f"[browser_navigate] Output: {response}")
            return json.dumps(response, ensure_ascii=False)
        
        # Access session from runtime store
        session = get_browser_session(runtime)
        if not session:
            response = {
                "success": False,
                "error": "No browser session available"
            }
            print(f"[browser_navigate] Output: {response}")
            return json.dumps(response, ensure_ascii=False)
        
        # Navigate to the URL using the AgentBay session browser agent
        now_agent = session.browser.agent
        await now_agent.navigate(url)
            
        response = {
            "success": True,
            "message": f"Successfully navigated to {url}",
            "url": url
        }
        # Log output result
        print(f"[browser_navigate] Output: {response}")
        return json.dumps(response, ensure_ascii=False)
    except Exception as e:
        result = {
            "success": False,
            "error": f"Error occurred while navigating to URL: {str(e)}"
        }
        # Log exception
        print(f"[browser_navigate] Exception: {result}")
        traceback.print_exc()
        return json.dumps(result, ensure_ascii=False)


@tool("browser_act")
async def browser_act(
    action: str = Field(..., description="Action to perform on the page"),
    runtime: ToolRuntime[BrowserSessionData, None] = None
) -> str:
    """Perform an action on browser page"""
    print(f"[browser_act] Input: action={action}")
    
    try:
        if not AGENTBAY_AVAILABLE:
            response = {
                "success": False,
                "error": "AgentBay SDK not available"
            }
            print(f"[browser_act] Output: {response}")
            return json.dumps(response, ensure_ascii=False)
        
        # Access session from runtime store
        session = get_browser_session(runtime)
        if not session:
            response = {
                "success": False,
                "error": "No browser session available"
            }
            print(f"[browser_act] Output: {response}")
            return json.dumps(response, ensure_ascii=False)
        
        # Create ActOptions for the action
        act_options = ActOptions(action=action)
        
        result = await session.browser.agent.act(act_options)
            
        # Return result as JSON string
        result_dict = {
            "success": result.success,
            "message": result.message,
            "action": action
        }
        
        result_json_str = json.dumps(result_dict, ensure_ascii=False)
        # Log output result
        print(f"[browser_act] Output: {result_json_str}")
        return result_json_str
    except Exception as e:
        result = {
            "success": False,
            "error": f"Error occurred while performing browser action: {str(e)}"
        }
        # Log exception
        print(f"[browser_act] Exception: {result}")
        traceback.print_exc()
        return json.dumps(result, ensure_ascii=False)


@tool("browser_screenshot")
async def browser_screenshot(
    file_path: str = Field(..., description="File path to save the screenshot"),
    runtime: ToolRuntime[BrowserSessionData, None] = None
) -> str:
    """Take a screenshot of the current browser page"""
    print(f"[browser_screenshot] Input: file_path={file_path}")
    
    try:
        if not AGENTBAY_AVAILABLE:
            response = {
                "success": False,
                "error": "AgentBay SDK not available"
            }
            print(f"[browser_screenshot] Output: {response}")
            return json.dumps(response, ensure_ascii=False)
        
        # Access session from runtime store
        session = get_browser_session(runtime)
        if not session:
            response = {
                "success": False,
                "error": "No browser session available"
            }
            print(f"[browser_screenshot] Output: {response}")
            return json.dumps(response, ensure_ascii=False)
            
        # Capture screenshot using browser agent
        screenshot_result = await session.browser.agent.screenshot()
            
        if screenshot_result:
            import base64
            import os
            # Decode base64 string to bytes
            screenshot_data = base64.b64decode(screenshot_result.split(',')[1] if ',' in screenshot_result else screenshot_result)
            
            # Create directory if it doesn't exist
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
                print(f"[browser_screenshot] Created directory: {directory}")
            
            # Save to file
            with open(file_path, "wb") as f:
                f.write(screenshot_data)
            
            # Return result as JSON string
            result_dict = {
                "success": True,
                "message": "Screenshot captured successfully",
                "file_path": file_path
            }
            
            result_json_str = json.dumps(result_dict, ensure_ascii=False)
            # Log output result
            print(f"[browser_screenshot] Output: {result_json_str}")
            return result_json_str
        else:
            result_dict = {
                "success": False,
                "error": "Failed to capture screenshot"
            }
            result_json_str = json.dumps(result_dict, ensure_ascii=False)
            # Log output result
            print(f"[browser_screenshot] Output: {result_json_str}")
            return result_json_str
    except Exception as e:
        result = {
            "success": False,
            "error": f"Error occurred while capturing screenshot: {str(e)}"
        }
        # Log exception
        print(f"[browser_screenshot] Exception: {result}")
        traceback.print_exc()
        return json.dumps(result, ensure_ascii=False)


@tool("browser_wait")
async def browser_wait(
    milliseconds: int = Field(..., description="Time to wait in milliseconds"),
    runtime: ToolRuntime[BrowserSessionData, None] = None
) -> str:
    """Wait for a specified amount of time in milliseconds. Useful for waiting for remote operations to complete."""
    # Log input parameters
    print(f"[browser_wait] Input: milliseconds={milliseconds}")
    
    try:
        # Convert milliseconds to seconds for time.sleep()
        seconds = milliseconds / 1000.0
        
        # Wait for the specified time
        await asyncio.sleep(seconds)
        
        response = {
            "success": True,
            "message": f"Successfully waited for {milliseconds} milliseconds ({seconds} seconds)"
        }
        
        # Log output result
        print(f"[browser_wait] Output: {response}")
        return json.dumps(response, ensure_ascii=False)
    except Exception as e:
        result = {
            "success": False,
            "error": f"Error occurred while waiting: {str(e)}"
        }
        # Log exception
        print(f"[browser_wait] Exception: {result}")
        traceback.print_exc()
        return json.dumps(result, ensure_ascii=False)
