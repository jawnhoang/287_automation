import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
import pyautogui

class TestGemini:

    def setup_method(self, method):
        options = uc.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")

        self.driver = uc.Chrome(options=options, headless=False, version_main=147, use_subprocess=True)
        self.vars = {}

    def teardown_method(self, method):
        input("Press ENTER to close browser...")
        self.driver.quit()

    def type_prompt(self, text):
        wait = WebDriverWait(self.driver, 20)
        # Gemini specific contenteditable div
        editor = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true']"))
        )
        editor.click()
        time.sleep(1)

        # Clear and type
        ActionChains(self.driver)\
            .key_down(Keys.CONTROL)\
            .send_keys("a")\
            .key_up(Keys.CONTROL)\
            .send_keys(Keys.BACKSPACE)\
            .perform()

        editor.send_keys(text)

    def test_gemini(self):
        wait = WebDriverWait(self.driver, 20)

        # 1 | Open Gemini and Wait for Manual Login
        self.driver.get("https://gemini.google.com/app")
        print("\n" + "="*50)
        print("ACTION REQUIRED: Please log in to Gemini manually.")
        print("Once you are at the chat screen, press ENTER here to start...")
        print("="*50 + "\n")
        input() 

        file_path = [
            f"C:\\Users\\jawn\\Desktop\\d3\\d2\\c{i}.jpg" for i in range(1, 22)
        ]
        
        j = 1
        for i in file_path:
            # 1 | Click the 'Plus' / 'Add' button to reveal the file input
            # In Gemini, this is usually a button with an aria-label like "Upload" or "Plus"
            plus_btn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Open upload file menu']"))
            )
            plus_btn.click()

            time.sleep(1) # Brief pause for the menu to open
            try:
                plus_btn = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label*='Upload'], button[aria-label*='Add']"))
                )
                
                # # Real mouse movement simulation
                actions = ActionChains(self.driver)
                actions.move_to_element(plus_btn).click().perform()
            except:
                pass


            time.sleep(1)

            # 2 | Locate the file input (targeting the most common Gemini selector)
            file_input = wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
            )
            
            file_input.send_keys(i)
            time.sleep(1)
            pyautogui.press('esc')

            # 3 | Wait for upload to register (Wait for the thumbnail to appear)
            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "img, .thumbnail, [role='img']"))
            )
            time.sleep(2)

            # 4 | Type prompt
            self.type_prompt(
                "Answer the following: Animate: [Yes/No], "
                "Identify: [what do you see], "
                "Motion: [Moving laterally, Stationary, Manipulating another artifact]"
            )

            # 5 | Submit button
            submit_btn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label*='Send message']"))
            )
            submit_btn.click()

            # 6 | Wait for the AI Response to finish
            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "model-response, .model-response-text"))
            )
            
            time.sleep(10)

            # 7 | Save Screenshot
            output_path = f"C:\\Users\\jawn\\Desktop\\gptauto\\gemini_result_{j}.png"
            self.driver.save_screenshot(output_path)
            print(f"Saved: {output_path}")
            j += 1

            # 8 | Reset: Click "New Chat" or Refresh
            self.driver.get("https://gemini.google.com/app")
            time.sleep(3)