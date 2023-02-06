from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys

from ui_framework import base_config


def configure_base_capabilities(test_name, resolution):
    options = Options()

    preferences = {"safebrowsing.enabled": "false", "network.proxy.port": "80"}
    options.add_argument("--incognito")
    options.add_argument("disable-infobars")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument(f"--window-size={resolution.replace('x', ',')}")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
    # Browser needs to be headless when running in CI
    if base_config.headless:
        options.add_argument("--headless")

    options.add_experimental_option("prefs", preferences)

    capabilities = options.to_capabilities()
    capabilities["name"] = test_name
    capabilities["screenResolution"] = resolution
    capabilities["browserName"] = "chrome"
    capabilities["version"] = "latest"

    return capabilities
