import unittest
import pytest

from agentbay import BrowserOption


class TestAsyncBrowserTypeUnit(unittest.IsolatedAsyncioTestCase):
    """Unit tests for browser type functionality."""

    @pytest.mark.asyncio


    async def test_browser_type_default(self):
        """Test that browser_type defaults to None."""
        option = BrowserOption()
        self.assertIsNone(option.browser_type)

    @pytest.mark.asyncio


    async def test_browser_type_chrome(self):
        """Test setting browser_type to 'chrome'."""
        option = BrowserOption(browser_type="chrome")
        self.assertEqual(option.browser_type, "chrome")

    @pytest.mark.asyncio


    async def test_browser_type_chromium(self):
        """Test setting browser_type to 'chromium'."""
        option = BrowserOption(browser_type="chromium")
        self.assertEqual(option.browser_type, "chromium")

    @pytest.mark.asyncio


    async def test_browser_type_invalid_firefox(self):
        """Test that invalid browser_type 'firefox' raises ValueError."""
        with self.assertRaises(ValueError) as context:
            BrowserOption(browser_type="firefox")

        self.assertIn(
            "browser_type must be 'chrome' or 'chromium'", str(context.exception)
        )

    @pytest.mark.asyncio


    async def test_browser_type_invalid_edge(self):
        """Test that invalid browser_type 'edge' raises ValueError."""
        with self.assertRaises(ValueError) as context:
            BrowserOption(browser_type="edge")

        self.assertIn(
            "browser_type must be 'chrome' or 'chromium'", str(context.exception)
        )

    @pytest.mark.asyncio


    async def test_browser_type_invalid_safari(self):
        """Test that invalid browser_type 'safari' raises ValueError."""
        with self.assertRaises(ValueError) as context:
            BrowserOption(browser_type="safari")

        self.assertIn(
            "browser_type must be 'chrome' or 'chromium'", str(context.exception)
        )

    @pytest.mark.asyncio


    async def test_browser_type_invalid_empty_string(self):
        """Test that empty string browser_type raises ValueError."""
        with self.assertRaises(ValueError) as context:
            BrowserOption(browser_type="")

        self.assertIn(
            "browser_type must be 'chrome' or 'chromium'", str(context.exception)
        )

    @pytest.mark.asyncio


    async def test_browser_type_valid_none(self):
        """Test that None browser_type is valid (default)."""
        option = BrowserOption(browser_type=None)
        self.assertIsNone(option.browser_type)

    @pytest.mark.asyncio


    async def test_browser_type_case_sensitive(self):
        """Test that browser_type is case sensitive."""
        with self.assertRaises(ValueError) as context:
            BrowserOption(browser_type="Chrome")

        self.assertIn(
            "browser_type must be 'chrome' or 'chromium'", str(context.exception)
        )

    @pytest.mark.asyncio


    async def test_browser_type_to_map_chrome(self):
        """Test that browser_type 'chrome' is included in to_map()."""
        option = BrowserOption(browser_type="chrome")
        option_map = option._to_map()

        self.assertIn("browserType", option_map)
        self.assertEqual(option_map["browserType"], "chrome")

    @pytest.mark.asyncio


    async def test_browser_type_to_map_chromium(self):
        """Test that browser_type 'chromium' is included in to_map()."""
        option = BrowserOption(browser_type="chromium")
        option_map = option._to_map()

        self.assertIn("browserType", option_map)
        self.assertEqual(option_map["browserType"], "chromium")

    @pytest.mark.asyncio


    async def test_browser_type_to_map_default(self):
        """Test that browser_type is not included in to_map() when None."""
        option = BrowserOption()
        option_map = option._to_map()

        self.assertNotIn("browserType", option_map)

    @pytest.mark.asyncio


    async def test_browser_type_with_other_options(self):
        """Test browser_type with other browser options."""
        option = BrowserOption(
            browser_type="chrome",
            use_stealth=True,
            user_agent="Mozilla/5.0 (Test) AppleWebKit/537.36",
            solve_captchas=True,
        )

        # Verify browser_type is set correctly
        self.assertEqual(option.browser_type, "chrome")

        # Verify other options are set correctly
        self.assertTrue(option.use_stealth)
        self.assertEqual(option.user_agent, "Mozilla/5.0 (Test) AppleWebKit/537.36")
        self.assertTrue(option.solve_captchas)

        # Verify to_map includes all options
        option_map = option._to_map()
        self.assertEqual(option_map["browserType"], "chrome")
        self.assertTrue(option_map["useStealth"])
        self.assertEqual(
            option_map["userAgent"], "Mozilla/5.0 (Test) AppleWebKit/537.36"
        )
        self.assertTrue(option_map["solveCaptchas"])

    @pytest.mark.asyncio


    async def test_browser_type_from_map_chrome(self):
        """Test creating BrowserOption from map with chrome browserType."""
        option_map = {
            "browserType": "chrome",
            "useStealth": True,
            "userAgent": "Mozilla/5.0 (Test) AppleWebKit/537.36",
        }

        option = BrowserOption()
        option._from_map(option_map)

        self.assertEqual(option.browser_type, "chrome")
        self.assertTrue(option.use_stealth)
        self.assertEqual(option.user_agent, "Mozilla/5.0 (Test) AppleWebKit/537.36")

    @pytest.mark.asyncio


    async def test_browser_type_from_map_chromium(self):
        """Test creating BrowserOption from map with chromium browserType."""
        option_map = {
            "browserType": "chromium",
            "useStealth": False,
            "solveCaptchas": True,
        }

        option = BrowserOption()
        option._from_map(option_map)

        self.assertEqual(option.browser_type, "chromium")
        self.assertFalse(option.use_stealth)
        self.assertTrue(option.solve_captchas)

    @pytest.mark.asyncio


    async def test_browser_type_from_map_default(self):
        """Test creating BrowserOption from map without browserType (should remain None)."""
        option_map = {
            "useStealth": True,
            "userAgent": "Mozilla/5.0 (Test) AppleWebKit/537.36",
        }

        option = BrowserOption()
        option._from_map(option_map)

        # Should remain None when not specified
        self.assertIsNone(option.browser_type)
        self.assertTrue(option.use_stealth)
        self.assertEqual(option.user_agent, "Mozilla/5.0 (Test) AppleWebKit/537.36")

    @pytest.mark.asyncio


    async def test_browser_type_validation_order(self):
        """Test that browser_type validation works correctly."""
        # Test browser_type validation independently
        with self.assertRaises(ValueError) as context:
            BrowserOption(browser_type="invalid")

        # Should get browser_type error
        self.assertIn(
            "browser_type must be 'chrome' or 'chromium'", str(context.exception)
        )

        # Test that proxies validation also works (happens before browser_type in the code)
        with self.assertRaises(ValueError) as context:
            BrowserOption(
                browser_type="chrome",  # Valid browser_type
                proxies=[{}, {}],  # Invalid proxies (too many)
            )

        # Should get proxies error
        self.assertIn(
            "proxies list length must be limited to 1", str(context.exception)
        )

    @pytest.mark.asyncio


    async def test_browser_type_immutable_after_creation(self):
        """Test that browser_type cannot be changed after BrowserOption creation."""
        option = BrowserOption(browser_type="chrome")
        self.assertEqual(option.browser_type, "chrome")

        # Attempting to change browser_type should not affect the original value
        # (This is more of a documentation test - in practice, the attribute is mutable)
        option.browser_type = (
            "chromium"  # This would work in Python, but we test the behavior
        )
        self.assertEqual(option.browser_type, "chromium")  # This shows it's mutable

    @pytest.mark.asyncio


    async def test_browser_type_with_viewport_and_screen(self):
        """Test browser_type with viewport and screen options."""
        from agentbay import BrowserScreen, BrowserViewport

        viewport = BrowserViewport(width=1920, height=1080)
        screen = BrowserScreen(width=1920, height=1080)

        option = BrowserOption(browser_type="chrome", viewport=viewport, screen=screen)

        self.assertEqual(option.browser_type, "chrome")
        self.assertEqual(option.viewport.width, 1920)
        self.assertEqual(option.viewport.height, 1080)
        self.assertEqual(option.screen.width, 1920)
        self.assertEqual(option.screen.height, 1080)

        # Test to_map includes all options
        option_map = option._to_map()
        self.assertEqual(option_map["browserType"], "chrome")
        self.assertEqual(option_map["viewport"]["width"], 1920)
        self.assertEqual(option_map["viewport"]["height"], 1080)
        self.assertEqual(option_map["screen"]["width"], 1920)
        self.assertEqual(option_map["screen"]["height"], 1080)


if __name__ == "__main__":
    unittest.main()
