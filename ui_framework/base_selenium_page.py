import datetime
import logging
import platform
import re
import time

from pytz import timezone
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.remote_connection import LOGGER as seleniumLogger
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

seleniumLogger.setLevel(logging.WARNING)


class SeleniumBasePage(object):
    ACCEPTABLE_LOADING_TIME = 60  # seconds

    def __init__(self, driver):
        self.driver = driver

    def verify_count_of_element(self, locator, expected_count, timeout=30):
        number_of_elements = len(self.find_elements_by(*locator))
        start_time = time.time()
        while time.time() - start_time < timeout:
            if number_of_elements == expected_count:
                return
            else:
                time.sleep(0.1)
        raise TimeoutError(
            f"{number_of_elements} did not match {expected_count}"
        )

    def verify_minimum_count_of_element(
        self, locator, expected_count, timeout=30
    ):
        number_of_elements = len(self.find_elements_by(*locator))
        start_time = time.time()
        while time.time() - start_time < timeout:
            if number_of_elements >= expected_count:
                return
            else:
                time.sleep(0.1)
        raise TimeoutError(
            f"{number_of_elements} were less than {expected_count}"
        )

    def verify_attribute_contains(
        self,
        attribute,
        expected_string,
        element_locator,
        timeout=ACCEPTABLE_LOADING_TIME,
    ):
        start_time = time.time()

        while time.time() - start_time < timeout:
            attribute_value = self.get_attribute_of_element(
                attribute, element_locator
            )

            if expected_string in attribute_value:
                return
            else:
                time.sleep(0.1)

        raise TimeoutException(
            "Attribute value "
            + attribute_value
            + " did not contain "
            + expected_string
        )

    def verify_css_value_contains(
        self,
        css_value,
        expected_string,
        element_locator,
        timeout=ACCEPTABLE_LOADING_TIME,
    ):
        start_time = time.time()

        while time.time() - start_time < timeout:
            css_value_value = self.get_css_value_of_element(
                css_value, element_locator
            )

            if expected_string in css_value_value:
                return
            else:
                time.sleep(0.1)

        raise TimeoutException(
            "CSS value "
            + css_value_value
            + " did not contain "
            + expected_string
        )

    def wait_for_element_to_be_invisible(
        self, element_locator, timeout=ACCEPTABLE_LOADING_TIME
    ):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(element_locator)
            )
        except Exception:
            raise Exception(f"Element was still visible after {timeout}.")

    def clear(self, element_locator, timeout=10):
        self.wait_for_element_to_be_clickable(element_locator, timeout)
        element = self.find_element_by(*element_locator)
        element.clear()

    def verify_value(self, expected_value, element_locator, timeout=10):
        start_time = time.time()

        while time.time() - start_time < timeout:
            actual_value = self.get_attribute_of_element(
                "value", element_locator
            )

            if actual_value == expected_value:
                return
            else:
                time.sleep(0.1)

        raise TimeoutError(
            "Actual value: "
            + actual_value
            + " did not equal expected value: "
            + expected_value
            + " after waiting"
        )

    def verify_value_contains(
        self, expected_value, element_locator, timeout=10
    ):
        start_time = time.time()

        actual_value = self.get_attribute_of_element("value", element_locator)
        while time.time() - start_time < timeout:
            if expected_value in actual_value:
                return
            else:
                actual_value = self.get_attribute_of_element(
                    "value", element_locator
                )
                time.sleep(0.1)

        raise TimeoutError(
            f"Expected value: {expected_value} is not a substring of: "
            f"{actual_value} after waiting {timeout} seconds."
        )

    def verify_text_contains(self, expected_text, element_locator, timeout=40):
        self.wait_for_element_to_be_present(element_locator)
        start_time = time.time()

        while time.time() - start_time < timeout:
            actual_text = self.get_text(element_locator)

            if expected_text in actual_text:
                return
            else:
                time.sleep(0.1)
        raise TimeoutError(
            f"Actual text: {actual_text} did not contain "
            f"expected text: {expected_text} after waiting {timeout} seconds."
        )

    def verify_value_contains_pattern(
        self, pattern, element_locator, timeout=15
    ):
        pattern = re.compile(pattern)
        start_time = time.time()

        actual_value = self.get_attribute_of_element("value", element_locator)
        while time.time() - start_time < timeout:
            if pattern.findall(actual_value):
                return
            else:
                actual_value = self.get_attribute_of_element(
                    "value", element_locator
                )
                time.sleep(0.1)
        raise TimeoutError(
            f"Actual value: {actual_value} did not match regex pattern {pattern}"
        )

    def verify_value_matches_pattern(
        self, pattern, element_locator, timeout=15
    ):
        pattern = re.compile(pattern)
        start_time = time.time()

        while time.time() - start_time < timeout:
            actual_value = self.get_attribute_of_element(
                "value", element_locator
            )
            result = pattern.match(actual_value)

            if result and result.group() == actual_value:
                return
            else:
                time.sleep(0.1)
        raise TimeoutError(
            f"Actual value: {actual_value} did not match regex pattern {pattern}"
        )

    def verify_text_does_not_contain(
        self, string, element_locator, timeout=ACCEPTABLE_LOADING_TIME
    ):
        start_time = time.time()

        while time.time() - start_time < timeout:
            actual_text = self.get_text(element_locator)

            if string not in actual_text:
                return
            else:
                time.sleep(0.1)

        raise TimeoutError(
            f"Actual text: {actual_text} "
            f"contained unexpected text: {string} after waiting {timeout} seconds"
        )

    def verify_text_does_not_contain_regex(
        self, matcher, element_locator, timeout=ACCEPTABLE_LOADING_TIME
    ):
        start_time = time.time()
        pattern = re.compile(matcher)

        while time.time() - start_time < timeout:
            actual_text = self.get_text(element_locator)

            if pattern.match(actual_text):
                time.sleep(0.1)
            else:
                return

        raise TimeoutError(
            f"Actual text: {actual_text} "
            f"contained unexpected text pattern: {pattern} after waiting {timeout} seconds"
        )

    def verify_text(self, expected_text, element_locator, timeout=20):
        start_time = time.time()

        while time.time() - start_time < timeout:
            actual_text = self.get_text(element_locator)

            if actual_text == expected_text:
                return
            else:
                time.sleep(0.1)

        raise TimeoutError(
            "Actual text: "
            + actual_text
            + " did not equal expected text: "
            + expected_text
            + " after waiting"
        )

    def get_text(self, element_locator, wait=10):
        text_load_timeout = wait
        start_time = time.time()

        while time.time() - start_time < text_load_timeout:
            try:
                element = self.wait_for_element_to_be_visible(element_locator)
                text = element.text
            except StaleElementReferenceException:
                text = None
                time.sleep(0.1)

            if text:
                return text
            else:
                time.sleep(0.1)

        raise TimeoutError(
            f"Unable to get text for element after {wait} seconds"
        )

    def get_attribute_of_element(self, attribute, element_locator, wait=30):
        self.wait_for_element_to_be_present(element_locator, wait)

        attribute_load_timeout = wait
        start_time = time.time()

        while time.time() - start_time < attribute_load_timeout:
            element = self.find_element_by(*element_locator)
            attribute_value = element.get_attribute(attribute)

            if attribute_value:
                return attribute_value
            else:
                time.sleep(0.5)

        raise TimeoutError(
            "Unable to find value for attribute: " + attribute + "for element"
        )

    def get_css_value_of_element(self, css_value, element_locator, wait=30):
        self.wait_for_element_to_be_present(element_locator, wait)

        css_value_load_timeout = wait
        start_time = time.time()

        while time.time() - start_time < css_value_load_timeout:
            element = self.find_element_by(*element_locator)
            css_value_value = element.value_of_css_property(css_value)

            if css_value_value:
                return css_value_value
            else:
                time.sleep(0.5)

        raise TimeoutError(
            "Unable to find value for attribute: " + css_value + " for element"
        )

    def verify_element_has_attribute(
        self, element_locator, attribute, timeout=10
    ):
        self.wait_for_element_to_be_present(element_locator, timeout)

        start_time = time.time()

        while time.time() - start_time < timeout:
            element = self.find_element_by(*element_locator)
            attribute_value = element.get_attribute(attribute)

            if attribute_value:
                return
            else:
                time.sleep(0.1)

        raise TimeoutError(
            "Unable to find attribute: " + attribute + " for element"
        )

    def wait_for_element_to_be_present(
        self, element_locator, wait=ACCEPTABLE_LOADING_TIME
    ):
        try:
            WebDriverWait(self.driver, wait).until(
                EC.presence_of_element_located(element_locator)
            )
        except TimeoutException:
            raise Exception(
                f"Element with locator: {element_locator} was not in the DOM after {wait} seconds. "
            )

    def wait_for_element_to_be_visible(
        self, element_locator, wait=ACCEPTABLE_LOADING_TIME
    ):
        self.wait_for_element_to_be_present(element_locator, wait=wait)

        try:
            return WebDriverWait(self.driver, wait).until(
                EC.visibility_of_element_located(element_locator)
            )
        except Exception:
            raise Exception(
                "Element was present but not visible. Make sure that element is not hidden. "
            )

    def send_keys(self, keys, element_locator):
        element = self.wait_for_element_to_be_visible(element_locator)
        element.send_keys(keys)

    def clear_and_send_keys(self, keys, element_locator):
        self.clear(element_locator)
        self.send_keys(keys, element_locator)

    def click(self, element_locator, timeout=ACCEPTABLE_LOADING_TIME):
        start_time = time.time()

        while time.time() - start_time < timeout:
            element = self.wait_for_element_to_be_clickable(
                element_locator, timeout
            )
            try:
                element.click()
                return
            except ElementClickInterceptedException:
                time.sleep(0.1)
            except StaleElementReferenceException:
                time.sleep(0.1)

        raise Exception(
            f"Unable to click element with locator {element_locator} after polling for {timeout} seconds"
        )

    def choose_value_in_select(self, element_locator, value_to_select):
        self.wait_for_element_to_be_clickable(element_locator)
        element = self.find_element_by(*element_locator)
        select_element = Select(element)
        select_element.select_by_value(value_to_select)

    def modal_click(self, element_locator, pause_time=None):
        self.wait_for_element_to_be_clickable(element_locator)
        element = self.find_element_by(*element_locator)
        actions = ActionChains(self.driver)
        if pause_time is not None:
            actions.click(element).pause(pause_time).perform()
        else:
            actions.click(element).perform()

    def move_mouse_to_location(self, element_locator):
        self.wait_for_element_to_be_visible(element_locator)
        element = self.find_element_by(*element_locator)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

    def modal_send_keys(self, keys, element_locator):
        self.wait_for_element_to_be_visible(element_locator)
        element = self.find_element_by(*element_locator)
        actions = ActionChains(self.driver)
        actions.click(element).send_keys(keys).send_keys(Keys.ENTER).perform()

    def navigate(self, url=None):
        if url:
            self.driver.get(url)
        else:
            self.driver.get(self.url)

    def find_element_by(self, *loc, timeout=10):
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                return self.driver.find_element(*loc)
            except StaleElementReferenceException:
                time.sleep(0.1)

        raise Exception(
            f"Unable to find element with locator f{loc} after waiting {timeout} seconds"
        )

    def find_element_without_polling(self, *loc):
        return self.driver.find_element(*loc)

    def find_elements_by(self, *loc):
        return self.driver.find_elements(*loc)

    def wait_for_element_to_be_clickable(
        self, element_locator, wait=ACCEPTABLE_LOADING_TIME
    ):
        self.wait_for_element_to_be_visible(element_locator, wait)

        start_time = time.time()

        while time.time() - start_time < wait:
            try:
                return WebDriverWait(self.driver, wait).until(
                    EC.element_to_be_clickable(element_locator)
                )
            except TimeoutException:
                raise Exception(
                    f"Element {element_locator} was visible but not clickable after {wait} seconds"
                    f"Verify that element has been scrolled into view"
                )
            except StaleElementReferenceException:
                time.sleep(0.1)
        raise StaleElementReferenceException(
            f"Element remained stale after {wait} seconds"
        )

    def switch_to_frame(self, frame_locator):
        self.wait_for_element_to_be_visible(frame_locator)
        frame = self.driver.find_element(*frame_locator)
        self.driver.switch_to.frame(frame)

    def return_from_iframe(self):
        self.driver.switch_to.default_content()

    def get_current_url(self):
        new_url = self.driver.current_url
        return new_url

    def get_current_number_of_tabs(self):
        return len(self.driver.window_handles)

    def wait_for_number_of_tabs(self, expected_number_of_tabs):
        start_time = time.time()

        while time.time() - start_time < self.ACCEPTABLE_LOADING_TIME:
            current_number_of_tabs = self.get_current_number_of_tabs()

            if current_number_of_tabs is expected_number_of_tabs:
                return
            else:
                time.sleep(0.1)

        raise TimeoutError(
            "Actual number of tabs "
            + str(current_number_of_tabs)
            + " did not equal expected number of tabs "
            + expected_number_of_tabs
        )

    def click_and_change_tabs(self, locator):
        number_of_tabs_before_click = self.get_current_number_of_tabs()
        self.click(locator)
        self.switch_to_new_tab(number_of_tabs_before_click)

    def switch_to_new_tab(self, tab_index):
        self.wait_for_number_of_tabs(tab_index + 1)
        self.driver.switch_to.window(self.driver.window_handles[tab_index])

    def switch_to_newest_tab(self):
        current_number_of_tabs = self.get_current_number_of_tabs()
        self.driver.switch_to.window(
            self.driver.window_handles[current_number_of_tabs - 1]
        )

    def switch_to_existing_tab(self, tab_index):
        self.driver.switch_to.window(self.driver.window_handles[tab_index])

    def close_current_window_and_switch_to_previous_window(
        self, desired_tab_index
    ):
        self.driver.close()
        self.driver.switch_to.window(
            self.driver.window_handles[desired_tab_index]
        )

    def scroll_into_center_view(self, locator):
        self.wait_for_element_to_be_visible(locator)
        element = self.find_element_by(*locator)

        start_time = time.time()

        while time.time() - start_time < 10:
            try:
                self.driver.execute_script(
                    'arguments[0].scrollIntoView({behavior: "auto", block: "center", inline: "nearest"});',
                    element,
                )
                return
            except StaleElementReferenceException:
                time.sleep(0.1)

        raise Exception(
            f"Unable to scoll element with locator {locator} into center view after 10 seconds"
        )

    def scroll_into_view(self, *loc, align_to_top=True):
        self.wait_for_element_to_be_visible(loc)
        element = self.find_element_by(*loc)
        if align_to_top:
            self.driver.execute_script(
                "arguments[0].scrollIntoView();", element
            )
        else:
            self.driver.execute_script(
                "arguments[0].scrollIntoView(false);", element
            )

    def scroll_to_top(self):
        self.driver.execute_script("window.scrollTo(0, 0)")

    def scroll_to_bottom(self):
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )

    def clear_by_backspace(self, locator, number_of_backspaces):
        self.send_keys(Keys.BACK_SPACE * number_of_backspaces, locator)

    def send_space_bar_key(self, locator):
        self.send_keys(Keys.SPACE, locator)

    def get_browser_time(self):
        time_zone = self.driver.execute_script(
            "return Intl.DateTimeFormat().resolvedOptions().timeZone"
        )
        return datetime.datetime.now(timezone(time_zone))

    def select_all_and_delete(self, element_locator, timeout=10):
        actions = ActionChains(self.driver)
        if platform.system() == "Darwin":
            actions.key_down(Keys.COMMAND).perform()
            actions.send_keys("a").perform()
            actions.key_up(Keys.COMMAND).perform()
            actions.send_keys(Keys.DELETE).perform()
        else:
            actions.key_down(Keys.CONTROL).perform()
            actions.send_keys("a").perform()
            actions.key_up(Keys.CONTROL).perform()
            actions.send_keys(Keys.DELETE).perform()

    def double_click_with_offset(
        self, starting_locator, x_offset=0, y_offset=0
    ):
        actions = ActionChains(self.driver)
        element = self.find_element_by(*starting_locator)
        actions.move_to_element_with_offset(
            element, x_offset, y_offset
        ).perform()
        actions.double_click().perform()

    def right_click(self, locator=None):
        actions = ActionChains(self.driver)
        if locator:
            element = self.find_element_by(*locator)
            actions.context_click(element).perform()
        else:
            actions.context_click().perform()

    def send_delete_key(self):
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.DELETE).perform()

