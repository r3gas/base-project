import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from ui_framework.base_selenium_page import SeleniumBasePage


class HuluPage(SeleniumBasePage):

    """
    Login Flow
    """
    login_message = (By.CSS_SELECTOR, "[data-automationid='login-message']")
    username_input = (By.CSS_SELECTOR, "[data-automationid='email-field']")
    password_input = (By.CSS_SELECTOR, "[data-automationid='password-field']")
    login_button = (By.CSS_SELECTOR, "[data-automationid='login-button']")

    def get_watching_profile(self, profile_name):
        profile = (By.CSS_SELECTOR, f"[aria-label='Switch profile to {profile_name}']")
        return profile

    """
    Search
    """
    search_button = (By.CSS_SELECTOR, "[data-automationid='globalnav-search']")

    """
    Tabs
    """
    home_tab = (By.CSS_SELECTOR, "[data-automationid='globalnav-home']")
    global_nav = (By.CSS_SELECTOR, "[data-testid='global-navigation']")
    my_stuff_tab = (By.CSS_SELECTOR, "[data-automationid='globalnav-my-stuff']")
    movies_tab = (By.CSS_SELECTOR, "[data-automationid='globalnav-movies']")

    """
    For you sections
    """
    for_you = (By.ID, "for-you")
    popular = (By.ID, "popular")
    tv_for_you_section = (By.ID, "tv-for-you")
