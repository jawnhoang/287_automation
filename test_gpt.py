import pytest
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

class TestGpt:

    def setup_method(self, method):
        options = Options()
        options = uc.ChromeOptions()
        

        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = uc.Chrome(options=options, headless=False, version_main=147)
        self.vars = {}

    def teardown_method(self, method):
        input("Press ENTER to close browser...")
        self.driver.quit()

    def type_prompt(self, text):
        wait = WebDriverWait(self.driver, 20)

        editor = wait.until(
            EC.presence_of_element_located((By.ID, "prompt-textarea"))
        )

        # force focus
        editor.click()
        time.sleep(2)

        # clear content safely
        ActionChains(self.driver)\
            .key_down(Keys.CONTROL)\
            .send_keys("a")\
            .key_up(Keys.CONTROL)\
            .send_keys(Keys.BACKSPACE)\
            .perform()

        # type into active ProseMirror selection
        active = self.driver.switch_to.active_element
        active.send_keys(text)

    def test_gpt(self):

        wait = WebDriverWait(self.driver, 20)

        # 1 | open ChatGPT
        self.driver.get("https://chatgpt.com/")

        time.sleep(5)

        file_path = ["C:\\Users\\jawn\\Desktop\\d3\\d2\\c1.jpg","C:\\Users\\jawn\\Desktop\\d3\\d2\\c2.jpg",
                     "C:\\Users\\jawn\\Desktop\\d3\\d2\\c3.jpg","C:\\Users\\jawn\\Desktop\\d3\\d2\\c4.jpg",
                     "C:\\Users\\jawn\\Desktop\\d3\\d2\\c5.jpg", "C:\\Users\\jawn\\Desktop\\d3\\d2\\c6.jpg",
                     "C:\\Users\\jawn\\Desktop\\d3\\d2\\c7.jpg", "C:\\Users\\jawn\\Desktop\\d3\\d2\\c8.jpg",
                     "C:\\Users\\jawn\\Desktop\\d3\\d2\\c9.jpg", "C:\\Users\\jawn\\Desktop\\d3\\d2\\c10.jpg",
                     "C:\\Users\\jawn\\Desktop\\d3\\d2\\c11.jpg", "C:\\Users\\jawn\\Desktop\\d3\\d2\\c12.jpg",
                     "C:\\Users\\jawn\\Desktop\\d3\\d2\\c13.jpg", "C:\\Users\\jawn\\Desktop\\d3\\d2\\c14.jpg",
                     "C:\\Users\\jawn\\Desktop\\d3\\d2\\c15.jpg", "C:\\Users\\jawn\\Desktop\\d3\\d2\\c16.jpg",
                     "C:\\Users\\jawn\\Desktop\\d3\\d2\\c17.jpg", "C:\\Users\\jawn\\Desktop\\d3\\d2\\c18.jpg",
                     "C:\\Users\\jawn\\Desktop\\d3\\d2\\c19.jpg", "C:\\Users\\jawn\\Desktop\\d3\\d2\\c20.jpg",
                     "C:\\Users\\jawn\\Desktop\\d3\\d2\\c21.jpg"]
        j = 1
        cnt = 0
        for i in file_path:


            # 2 | locate plus button
            plus_btn = wait.until(
                EC.presence_of_element_located((By.ID, "composer-plus-btn"))
            )

            ActionChains(self.driver).move_to_element(plus_btn).perform()

            # 4 | open upload menu
            plus_btn.click()

            file_input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
            )
            file_input.send_keys(i)

            # wait for UI to process upload
            time.sleep(1)
            
            # 7 | final instruction prompt
            self.type_prompt("Hello, ")
            self.type_prompt(
                "Answer the following: Animate: [Yes/No], Identify: [what do you see], " \
                "Motion: [Moving laterally, Stationary, Manipulating another artifact]"
            )

            time.sleep(1)

            # 8 | submit
            submit_btn = wait.until(
                EC.element_to_be_clickable((By.ID, "composer-submit-button"))
            )
            submit_btn.click()

            wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-message-author-role='assistant']"))
                )
            
            self.driver.execute_script("""
                document.querySelector('main')?.scrollTo(0, 0);
            """)

            time.sleep(10)

            self.driver.save_screenshot(f"C:\\Users\\jawn\\Desktop\\gptauto\\result_{j}.png")
            j+=1

            time.sleep(5)
            self.driver.delete_all_cookies()
            self.driver.get("https://chatgpt.com/")