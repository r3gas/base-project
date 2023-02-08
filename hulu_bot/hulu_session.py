from selenium.webdriver import DesiredCapabilities

from page_models import page_hulu
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

"""
Use a combination of selenium and beautifulsoup to log into your hulu account and 
"""
HOME_URL = "https://auth.hulu.com/web/login"

class HuluSession:
    def __init__(self):

        options = uc.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        options.add_argument("--lang=en-GB")
        print("Getting ChromeDriver ...")
        """
        Use undetected-chromedirver
        """
        self.driver = uc.Chrome(options=options)
        self.hulu_page = page_hulu.HuluPage(self.driver)

    def login(self, username, password, profile_name):
        self.driver.get(HOME_URL)
        self.hulu_page.wait_for_element_to_be_visible(self.hulu_page.login_message)
        self.hulu_page.clear_and_send_keys(username, self.hulu_page.username_input)
        self.hulu_page.clear_and_send_keys(password, self.hulu_page.password_input)
        self.hulu_page.click(self.hulu_page.login_button)
        self.hulu_page.wait_for_element_to_be_invisible(self.hulu_page.login_message)
        self.hulu_page.click(self.hulu_page.get_watching_profile(profile_name))

    """
    Pass in which tab you want to go to in the session prior to scraping titles
    All tabs are stored in the hulu page model under the Tabs section
    """
    def navigate_to_movie_tab(self):
        self.hulu_page.wait_for_element_to_be_visible(self.hulu_page.global_nav)
        self.hulu_page.click(self.hulu_page.home_tab)
        self.hulu_page.click(self.hulu_page.movies_tab)
        self.hulu_page.wait_for_element_to_be_visible(self.hulu_page.for_you)
        self.hulu_page.wait_for_element_to_be_visible(self.hulu_page.popular)

    """
    Use Beautiful Soup to collect the titles
    Check titles.txt to see if title already exists
    If not, write title to file
    """
    def get_movie_tab_titles(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        titles = []
        for div in soup.find_all('div', class_='StandardEmphasisHorizontalTileThumbnail__content'):
            title = div.find('img')['alt'].split('for ')[1]
            titles.append(title)

        with open('titles.txt', 'w') as file:
            for title in titles:
                file.write(title + '\n')

    def close(self):
        self.driver.close()












