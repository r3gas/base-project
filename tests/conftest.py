
import logging
import pytest
from selenium import webdriver
from ui_framework import configure_chrome
from ui_framework import base_config

LOGGER = logging.getLogger(__name__)

SCREEN_HEIGHT = 1080
SCREEN_WIDTH = 1920
RESOLUTION = str(SCREEN_WIDTH) + "x" + str(SCREEN_HEIGHT)


# Teardown fixture to quit browser session
def teardown_driver(driver):
    driver.quit()


# Creator of web_driver fixtures
# Currently only configured for chrome
@pytest.fixture(scope="function")
def web_driver_factory(request):
    class Driver(object):
        @staticmethod
        def web_driver():
            test_name = request.node.name

            if base_config.browser.lower() == "chrome":
                capabilities = configure_chrome.configure_base_capabilities(
                    test_name, RESOLUTION
                )
                driver = webdriver.Chrome(desired_capabilities=capabilities)
            else:
                raise Exception("WebDriver Environment not supported")
            driver.set_window_size(SCREEN_WIDTH, SCREEN_HEIGHT)

            def teardown():
                teardown_driver(driver)

            request.addfinalizer(teardown)
            return driver

    return Driver()


# Fixture to use web_driver_factory and create single web_driver
@pytest.fixture(scope="function")
def web_driver(web_driver_factory):
    yield web_driver_factory.web_driver()


# Adds pass / fail status to test object, used in teardown finalizers
@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "test_result", rep.outcome)
    return rep
