from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys
from datetime import datetime
import re


class CookieClickerGameSession:

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("http://orteil.dashnet.org/experiments/cookie/")
        self.cookie_el = self.driver.find_element(by=By.ID, value="cookie")
        self.start_time = datetime.now()
        self.game_running = True
        self.seconds_since_upgrade = 0
        self.last_upgrade = datetime.now()
        self.cookie_balance_int = 0
        self.run_game()

    def run_game(self):
        while self.game_running:
            self.click_cookie()
            self.seconds_since_upgrade = int((datetime.now() - self.last_upgrade).total_seconds())
            if self.seconds_since_upgrade % 5 == 0 and self.seconds_since_upgrade > 0:
                self.buy_best_upgrade()
                self.seconds_since_upgrade = 0
                self.last_upgrade = datetime.now()

    def click_cookie(self):
        self.cookie_el.click()

    def buy_best_upgrade(self):
        store_el = self.driver.find_element(by=By.ID, value="store")
        available_item_els = store_el.find_elements(by=By.TAG_NAME, value="div")
        best_upgrade_dict = dict(el=available_item_els[-1], price=0)
        for item_el in available_item_els[::-1]:
            item_class = item_el.get_attribute("class")
            if not item_class:
                item_title_el = item_el.find_element(by=By.TAG_NAME, value="b")
                item_title_commas_removed = item_title_el.text.replace(",", "")
                item_price_str = re.search(r"[-+]?\d*\.?\d+|[-+]?\d+",
                                           item_title_commas_removed).group(0)
                item_price_int = int(item_price_str)
                if item_price_int > best_upgrade_dict["price"]:
                    best_upgrade_dict = dict(el=item_el, price=item_price_int)
        cookie_balance_el = self.driver.find_element(by=By.ID, value="money")
        self.cookie_balance_int = int(cookie_balance_el.text.replace(",", ""))
        if self.cookie_balance_int > best_upgrade_dict["price"]:
            best_upgrade_dict["el"].click()
