import logging
import os
import re
import shutil
from datetime import datetime


LOGGER = logging.getLogger(__name__)
current_working_directory = os.getcwd()
SCREENSHOTS_DIRECTORY = current_working_directory + "/failure_screenshots"

if os.path.exists(SCREENSHOTS_DIRECTORY):
    shutil.rmtree(SCREENSHOTS_DIRECTORY)

os.mkdir(SCREENSHOTS_DIRECTORY)


def take_failure_snapshot(web_driver, request):
    if (
        hasattr(request.node, "test_result")
        and request.node.test_result == "failed"
    ):
        dt_now = datetime.now()
        ts = dt_now.strftime("%Y%m%dT%H%M%S")
        screenshot_path = re.sub(
            r"[^\w\-_/\. ]",
            "_",
            f"{SCREENSHOTS_DIRECTORY}/{request.node.name}-{ts}.png",
        )
        LOGGER.info(
            f"Test has failed. See more details in screenshot at {screenshot_path}"
        )
        web_driver.save_screenshot(screenshot_path)
