from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys
from datetime import datetime


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
        self.run_game()

    def run_game(self):
        while self.game_running:
            self.click_cookie()
            self.seconds_since_upgrade = int((datetime.now() - self.last_upgrade).total_seconds())
            if self.seconds_since_upgrade % 5 == 0 and self.seconds_since_upgrade > 0:
                print("5 seconds passed...")
                self.seconds_since_upgrade = 0
                self.last_upgrade = datetime.now()

    def click_cookie(self):
        self.cookie_el.click()
