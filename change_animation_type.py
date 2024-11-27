import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestChangeAnimationType():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1936, 1048)
        self.vars = {}
    
    def teardown_method(self, method):
        self.driver.quit()
    
    def test_changeAnimationType(self):
        with open("sites-to-modify.txt", "r", encoding="utf-8") as file:
            links = file.readlines()
        with open("credentials.txt", "r", encoding="utf-8") as file:
            credentials = file.readlines()

        print("Links to process:", links)

        self.driver.get("https://www.tomaszciecko.pl/wp-login.php")
        self.driver.find_element(By.ID, "user_login").click()
        self.driver.find_element(By.ID, "user_login").send_keys(credentials[0])
        self.driver.find_element(By.ID, "user_pass").click()
        self.driver.find_element(By.ID, "user_pass").send_keys(credentials[1])
        self.driver.find_element(By.ID, "rememberme").click()
        self.driver.find_element(By.ID, "wp-submit").click()
        self.driver.implicitly_wait(10)

        for link_text in links:
            link_text = link_text.strip()
            
            if link_text:
                print(f"Processing link: {link_text}")
                
                self.driver.get("https://www.tomaszciecko.pl/wp-admin/edit.php?post_type=page&paged=4")
                
                try:
                    link_element = self.driver.find_element(By.LINK_TEXT, link_text)
                    link_element.click()
                    self.driver.implicitly_wait(30)
                    self.driver.find_element(By.CSS_SELECTOR, "html").click()
                    self.driver.find_element(By.ID, "_post_loading_animation_type").click()

                    dropdown = self.driver.find_element(By.ID, "_post_loading_animation_type")
                    dropdown.find_element(By.XPATH, "//option[. = 'None']").click()
                
                    self.driver.find_element(By.ID, "publish").submit()
                    self.driver.implicitly_wait(10)

                    print(f"Successfully processed: {link_text}")
                except Exception as e:
                    print(f"Error processing {link_text}: {e}")
