#!/usr/bin/env python3
"""
Browser Extension Management Example

This example demonstrates how to use the ExtensionsService to manage browser extensions
and integrate them with browser sessions. It shows the complete workflow of:
1. Uploading browser extensions to the cloud
2. Creating extension options for browser integration
3. Creating browser sessions with extensions
4. Testing extension functionality
5. Managing extension lifecycle
"""

import os
import time
from agentbay import AgentBay
from agentbay.extention import ExtensionsService
from agentbay.session_params import CreateSessionParams, BrowserContext
from agentbay.browser.browser import BrowserOption
from playwright.sync_api import sync_playwright


def extension_management_demo():
    """Demonstrate browser extension management."""
    # Get API key from environment
    api_key = os.environ.get("AGENTBAY_API_KEY")
    if not api_key:
        print("Error: AGENTBAY_API_KEY environment variable not set")
        return False

    # Initialize AgentBay client
    agent_bay = AgentBay(api_key)
    print("AgentBay client initialized")

    # Create a unique context name for extension management
    extension_context_name = f"extension-demo-{int(time.time())}"
    
    try:
        # Initialize Extensions Service with named context
        print(f"Initializing Extensions Service with context: {extension_context_name}")
        extensions_service = ExtensionsService(agent_bay, extension_context_name)
        
        # For this demo, we'll show the code structure without actually uploading files
        # In a real scenario, you would have actual extension ZIP files
        print("Note: This demo shows the code structure. Replace '/path/to/your-extension.zip' with actual extension files.")
        
        # Example 1: Basic extension upload and usage
        print("\n=== Example 1: Basic Extension Usage ===")
        
        # In a real implementation, you would uncomment these lines:
        # extension = extensions_service.create("/path/to/your-extension.zip")
        # print(f"Extension uploaded: {extension.name} (ID: {extension.id})")
        
        # For demo purposes, we'll simulate an extension ID
        simulated_extension_id = "ext_demo_12345"
        print(f"Simulated extension ID: {simulated_extension_id}")
        
        # Create extension option for browser integration
        ext_option = extensions_service.create_extension_option([simulated_extension_id])
        print("Extension option created successfully")
        
        # Create browser session with extension
        browser_context = BrowserContext(
            context_id=f"extension-session-{int(time.time())}",
            auto_upload=True,
            extension_option=ext_option
        )
        
        params = CreateSessionParams(
            labels={"purpose": "extension_demo", "type": "example"},
            browser_context=browser_context
        )
        
        print("Browser session with extension would be created here")
        # In a real implementation:
        # session_result = agent_bay.create(params)
        # session = session_result.session
        # print("Extension session created successfully!")
        
        # Example 2: Working with multiple extensions
        print("\n=== Example 2: Multiple Extensions ===")
        
        # Simulate multiple extensions
        simulated_extension_ids = [
            "ext_demo_12345",
            "ext_demo_67890",
            "ext_demo_abcde"
        ]
        
        # Create session with all extensions
        ext_option_multi = extensions_service.create_extension_option(simulated_extension_ids)
        print(f"Created extension option with {len(simulated_extension_ids)} extensions")
        
        browser_context_multi = BrowserContext(
            context_id=f"multi-extension-session-{int(time.time())}",
            auto_upload=True,
            extension_option=ext_option_multi
        )
        
        params_multi = CreateSessionParams(
            browser_context=browser_context_multi
        )
        
        print("Multi-extension session would be created here")
        
        # Example 3: Extension development workflow
        print("\n=== Example 3: Extension Development Workflow ===")
        
        class ExtensionDevelopmentWorkflow:
            def __init__(self, agent_bay_client, context_name):
                self.agent_bay = agent_bay_client
                self.extensions_service = ExtensionsService(agent_bay_client, context_name)
                self.extension_id = None
            
            def upload_extension(self, extension_path):
                """Upload extension for development testing."""
                print(f"Uploading extension from: {extension_path}")
                # In real implementation:
                # extension = self.extensions_service.create(extension_path)
                # self.extension_id = extension.id
                # print(f"Extension uploaded: {extension.name}")
                
                # For demo, simulate success
                self.extension_id = "ext_dev_12345"
                print(f"Simulated extension uploaded with ID: {self.extension_id}")
                return self.extension_id
            
            def create_test_session(self):
                """Create a browser session for testing."""
                if not self.extension_id:
                    print("No extension uploaded yet")
                    return None
                    
                ext_option = self.extensions_service.create_extension_option([self.extension_id])
                
                session_params = CreateSessionParams(
                    labels={"purpose": "extension_development", "type": "test"},
                    browser_context=BrowserContext(
                        context_id=f"dev-session-{int(time.time())}",
                        auto_upload=True,
                        extension_option=ext_option
                    )
                )
                
                print("Test session would be created here")
                # In real implementation:
                # return self.agent_bay.create(session_params).session
                return {"session_id": f"session_{int(time.time())}"}
            
            def update_and_test(self, new_extension_path):
                """Update extension and create new test session."""
                if not self.extension_id:
                    print("No extension to update")
                    return None
                    
                print(f"Updating extension with: {new_extension_path}")
                # In real implementation:
                # updated_ext = self.extensions_service.update(self.extension_id, new_extension_path)
                # print(f"Extension updated: {updated_ext.name}")
                
                print("Simulated extension update completed")
                
                # Create new test session with updated extension
                return self.create_test_session()
            
            def cleanup(self):
                """Clean up development resources."""
                if self.extension_id:
                    print(f"Deleting extension: {self.extension_id}")
                    # In real implementation:
                    # self.extensions_service.delete(self.extension_id)
                
                print("Cleaning up extension service")
                # In real implementation:
                # self.extensions_service.cleanup()
        
        # Usage of ExtensionDevelopmentWorkflow
        workflow = ExtensionDevelopmentWorkflow(agent_bay, f"dev-context-{int(time.time())}")
        
        # Development cycle
        print("Starting extension development cycle...")
        workflow.upload_extension("/path/to/extension-v1.zip")
        session1 = workflow.create_test_session()
        print(f"Created test session: {session1}")
        
        # Update and test again
        session2 = workflow.update_and_test("/path/to/extension-v2.zip")
        print(f"Created updated test session: {session2}")
        
        # Clean up
        workflow.cleanup()
        print("Development workflow completed")
        
        # Example 4: Automated extension testing
        print("\n=== Example 4: Automated Extension Testing ===")
        
        def run_extension_tests(extension_paths):
            """Run automated tests on multiple extensions."""
            print("Running automated extension tests...")
            
            # In real implementation:
            # extensions_service = ExtensionsService(agent_bay)
            
            try:
                # Upload all test extensions
                extension_ids = []
                for i, path in enumerate(extension_paths):
                    print(f"Uploading extension: {path}")
                    # In real implementation:
                    # ext = extensions_service.create(path)
                    # extension_ids.append(ext.id)
                    
                    # For demo, simulate extension IDs
                    ext_id = f"ext_test_{i}_{int(time.time())}"
                    extension_ids.append(ext_id)
                    print(f"Simulated extension uploaded: {ext_id}")
                
                # Create test session
                ext_option = extensions_service.create_extension_option(extension_ids)
                
                session_params = CreateSessionParams(
                    labels={"purpose": "automated_testing", "type": "extension_test"},
                    browser_context=BrowserContext(
                        context_id=f"test-session-{int(time.time())}",
                        auto_upload=True,
                        extension_option=ext_option
                    )
                )
                
                print("Test session with all extensions would be created here")
                # In real implementation:
                # session_result = agent_bay.create(session_params)
                # session = session_result.session
                
                print(f"Testing {len(extension_ids)} extensions in session")
                return True
                
            except Exception as e:
                print(f"Error during extension testing: {e}")
                return False
            finally:
                print("Cleaning up test resources")
                # In real implementation:
                # extensions_service.cleanup()
        
        # Run automated tests
        test_extension_paths = [
            "/path/to/test-extension-1.zip",
            "/path/to/test-extension-2.zip",
            "/path/to/test-extension-3.zip"
        ]
        
        test_success = run_extension_tests(test_extension_paths)
        if test_success:
            print("Automated extension tests completed successfully!")
        else:
            print("Automated extension tests failed!")
        
        print("\nDemo completed successfully!")
        return True
        
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Clean up - in a real implementation you might want to keep the context
        # for future use, but for demo purposes we'll show how to clean up
        print("\n=== Cleanup ===")
        print("In a real implementation, you would call extensions_service.cleanup() here")
        # extensions_service.cleanup()


if __name__ == "__main__":
    extension_management_demo()