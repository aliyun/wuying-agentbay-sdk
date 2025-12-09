import unittest
import pytest
from unittest.mock import MagicMock, Mock, MagicMock

from agentbay import Code
from agentbay import (
    EnhancedCodeExecutionResult,
    CodeExecutionResult as ExecutionResult,
    ExecutionLogs,
    ExecutionError,
)


class TestEnhancedCodeExecution(unittest.TestCase):
    """Unit tests for Enhanced Code Execution functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_session = MagicMock()
        self.session = self.mock_session
        self.mock_session._get_api_key.return_value = "test-api-key"
        self.mock_session._get_session_id.return_value = "test-session-id"
        self.mock_session._is_vpc_enabled.return_value = False
        
        self.mock_client = MagicMock()
        self.mock_session._get_client.return_value = self.mock_client
        
        self.code = Code(self.mock_session)

    def test_execution_result_formats(self):
        """Test ExecutionResult.formats() method."""
        # Test with text only
        result = ExecutionResult(text="Hello World")
        self.assertEqual(result.formats(), ["text"])
        
        # Test with multiple formats
        result = ExecutionResult(
            text="Hello",
            html="<h1>Hello</h1>",
            png="base64data",
            is_main_result=True
        )
        formats = result.formats()
        self.assertIn("text", formats)
        self.assertIn("html", formats)
        self.assertIn("png", formats)
        self.assertNotIn("is_main_result", formats)
        
        # Test with no formats
        result = ExecutionResult()
        self.assertEqual(result.formats(), [])

    def test_enhanced_result_backward_compatibility(self):
        """Test backward compatibility through result property."""
        # Test main result priority
        results = [
            ExecutionResult(text="secondary", is_main_result=False),
            ExecutionResult(text="primary", is_main_result=True)
        ]
        enhanced_result = EnhancedCodeExecutionResult(
            success=True,
            results=results
        )
        self.assertEqual(enhanced_result.result, "primary")
        
        # Test fallback to first result
        results = [
            ExecutionResult(text="first"),
            ExecutionResult(text="second")
        ]
        enhanced_result = EnhancedCodeExecutionResult(
            success=True,
            results=results
        )
        self.assertEqual(enhanced_result.result, "first")
        
        # Test fallback to logs
        logs = ExecutionLogs(stdout=["output1", "output2"])
        enhanced_result = EnhancedCodeExecutionResult(
            success=True,
            logs=logs
        )
        self.assertEqual(enhanced_result.result, "output1output2")
        
        # Test empty result
        enhanced_result = EnhancedCodeExecutionResult(success=True)
        self.assertEqual(enhanced_result.result, "")

    @pytest.mark.sync
    def test_rich_response_parsing(self):
        """Test parsing of rich response format."""
        response_body = {
            "Success": True,
            "Data": {
                "logs": {
                    "stdout": ["Hello World\n"],
                    "stderr": ["Warning: test\n"]
                },
                "results": [
                    {
                        "text": "42",
                        "is_main_result": True
                    },
                    {
                        "html": "<div>Chart</div>",
                        "png": "base64imagedata",
                        "is_main_result": False
                    }
                ],
                "execution_count": 5,
                "execution_time": 1.5
            },
            "RequestId": "test-request-id"
        }
        
        mock_response = MagicMock()
        mock_response.to_map.return_value = {"body": response_body}
        self.mock_client.call_mcp_tool.return_value = mock_response

        result = self.code.run_code("print('Hello World'); 42", "python")

        self.assertIsInstance(result, EnhancedCodeExecutionResult)
        self.assertTrue(result.success)
        self.assertEqual(result.execution_count, 5)
        self.assertEqual(result.execution_time, 1.5)
        
        # Check logs
        self.assertEqual(result.logs.stdout, ["Hello World\n"])
        self.assertEqual(result.logs.stderr, ["Warning: test\n"])
        
        # Check results
        self.assertEqual(len(result.results), 2)
        self.assertEqual(result.results[0].text, "42")
        self.assertTrue(result.results[0].is_main_result)
        self.assertEqual(result.results[1].html, "<div>Chart</div>")
        self.assertEqual(result.results[1].png, "base64imagedata")
        self.assertFalse(result.results[1].is_main_result)
        
        # Check backward compatibility
        self.assertEqual(result.result, "42")

    @pytest.mark.sync
    def test_matplotlib_chart_response(self):
        """Test response with matplotlib chart data."""
        response_body = {
            "Success": True,
            "Data": {
                "logs": {
                    "stdout": [""],
                    "stderr": []
                },
                "results": [
                    {
                        "png": "iVBORw0KGgoAAAANSUhEUgAAAX4AAAEGCAYAAABiq",
                        "chart": {
                            "type": "matplotlib",
                            "title": "Sample Chart"
                        },
                        "is_main_result": True
                    }
                ],
                "execution_time": 2.1
            },
            "RequestId": "chart-request-id"
        }
        
        mock_response = MagicMock()
        mock_response.to_map.return_value = {"body": response_body}
        self.mock_client.call_mcp_tool.return_value = mock_response

        code = """
import matplotlib.pyplot as plt
plt.plot([1,2,3], [1,4,9])
plt.title('Sample Chart')
plt.show()
"""
        result = self.code.run_code(code, "python")

        self.assertTrue(result.success)
        self.assertEqual(len(result.results), 1)
        
        chart_result = result.results[0]
        self.assertIsNotNone(chart_result.png)
        self.assertIsNotNone(chart_result.chart)
        self.assertEqual(chart_result.chart["type"], "matplotlib")
        self.assertEqual(chart_result.chart["title"], "Sample Chart")
        self.assertTrue(chart_result.is_main_result)

    @pytest.mark.sync
    def test_pandas_dataframe_response(self):
        """Test response with pandas DataFrame HTML output."""
        response_body = {
            "Success": True,
            "Data": {
                "logs": {
                    "stdout": [""],
                    "stderr": []
                },
                "results": [
                    {
                        "html": "<table><tr><th>A</th><th>B</th></tr><tr><td>1</td><td>4</td></tr></table>",
                        "text": "   A  B\n0  1  4\n1  2  5\n2  3  6",
                        "is_main_result": True
                    }
                ]
            },
            "RequestId": "dataframe-request-id"
        }
        
        mock_response = MagicMock()
        mock_response.to_map.return_value = {"body": response_body}
        self.mock_client.call_mcp_tool.return_value = mock_response

        code = """
import pandas as pd
df = pd.DataFrame({'A': [1,2,3], 'B': [4,5,6]})
df.to_html()
"""
        result = self.code.run_code(code, "python")

        self.assertTrue(result.success)
        self.assertEqual(len(result.results), 1)
        
        df_result = result.results[0]
        self.assertIn("<table>", df_result.html)
        self.assertIn("A  B", df_result.text)
        self.assertTrue(df_result.is_main_result)

    @pytest.mark.sync
    def test_multiple_display_outputs(self):
        """Test code with multiple display outputs."""
        response_body = {
            "Success": True,
            "Data": {
                "logs": {
                    "stdout": ["This is standard output\n"],
                    "stderr": []
                },
                "results": [
                    {
                        "html": "<h1>Important Result</h1>",
                        "is_main_result": False
                    },
                    {
                        "text": "42",
                        "is_main_result": True
                    }
                ]
            },
            "RequestId": "multi-output-request-id"
        }
        
        mock_response = MagicMock()
        mock_response.to_map.return_value = {"body": response_body}
        self.mock_client.call_mcp_tool.return_value = mock_response

        code = """
from IPython.display import display, HTML
display(HTML('<h1>Important Result</h1>'))
print('This is standard output')
42
"""
        result = self.code.run_code(code, "python")

        self.assertTrue(result.success)
        self.assertEqual(len(result.results), 2)
        self.assertEqual(result.logs.stdout, ["This is standard output\n"])
        
        # Check HTML display output
        self.assertEqual(result.results[0].html, "<h1>Important Result</h1>")
        self.assertFalse(result.results[0].is_main_result)
        
        # Check main result (last expression)
        self.assertEqual(result.results[1].text, "42")
        self.assertTrue(result.results[1].is_main_result)
        
        # Backward compatibility should return main result
        self.assertEqual(result.result, "42")

    @pytest.mark.sync
    def test_error_response_with_details(self):
        """Test error response with detailed error information."""
        response_body = {
            "Success": True,
            "Data": {
                "logs": {
                    "stdout": [],
                    "stderr": ["Traceback (most recent call last):\n"]
                },
                "error": {
                    "name": "NameError",
                    "value": "name 'undefined_var' is not defined",
                    "traceback": "Traceback (most recent call last):\n  File \"<stdin>\", line 1, in <module>\nNameError: name 'undefined_var' is not defined"
                },
                "isError": True
            },
            "RequestId": "error-request-id"
        }
        
        mock_response = MagicMock()
        mock_response.to_map.return_value = {"body": response_body}
        self.mock_client.call_mcp_tool.return_value = mock_response

        result = self.code.run_code("print(undefined_var)", "python")

        self.assertFalse(result.success)
        self.assertIsNotNone(result.error)
        self.assertEqual(result.error.name, "NameError")
        self.assertEqual(result.error.value, "name 'undefined_var' is not defined")
        self.assertIn("Traceback", result.error.traceback)

    @pytest.mark.sync
    def test_json_output_response(self):
        """Test response with JSON output."""
        response_body = {
            "Success": True,
            "Data": {
                "logs": {
                    "stdout": [],
                    "stderr": []
                },
                "results": [
                    {
                        "json": {"name": "John", "age": 30, "city": "New York"},
                        "text": '{"name": "John", "age": 30, "city": "New York"}',
                        "is_main_result": True
                    }
                ]
            },
            "RequestId": "json-request-id"
        }
        
        mock_response = MagicMock()
        mock_response.to_map.return_value = {"body": response_body}
        self.mock_client.call_mcp_tool.return_value = mock_response

        code = """
import json
data = {"name": "John", "age": 30, "city": "New York"}
json.dumps(data)
"""
        result = self.code.run_code(code, "python")

        self.assertTrue(result.success)
        self.assertEqual(len(result.results), 1)
        
        json_result = result.results[0]
        self.assertIsNotNone(json_result.json)
        self.assertEqual(json_result.json["name"], "John")
        self.assertEqual(json_result.json["age"], 30)
        self.assertTrue(json_result.is_main_result)

    @pytest.mark.sync
    def test_latex_output_response(self):
        """Test response with LaTeX output."""
        response_body = {
            "Success": True,
            "Data": {
                "logs": {
                    "stdout": [],
                    "stderr": []
                },
                "results": [
                    {
                        "latex": r"$$\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}$$",
                        "is_main_result": True
                    }
                ]
            },
            "RequestId": "latex-request-id"
        }
        
        mock_response = MagicMock()
        mock_response.to_map.return_value = {"body": response_body}
        self.mock_client.call_mcp_tool.return_value = mock_response

        code = r"""
from IPython.display import Latex
Latex(r'$$\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}$$')
"""
        result = self.code.run_code(code, "python")

        self.assertTrue(result.success)
        self.assertEqual(len(result.results), 1)
        
        latex_result = result.results[0]
        self.assertIsNotNone(latex_result.latex)
        self.assertIn(r"\int", latex_result.latex)
        self.assertTrue(latex_result.is_main_result)


if __name__ == "__main__":
    unittest.main()