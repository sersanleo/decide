from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from base.tests import BaseTestCase

class SignUpTestCase(StaticLiveServerTestCase):

    def setUp(self):
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.FirefoxOptions()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)

        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()

    def test_correct_sing_up(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.find_element(By.ID, "signIn").click()
        self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > #username").click()
        self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > #username").send_keys("prueba5")
        self.driver.find_element(By.ID, "email").click()
        self.driver.find_element(By.ID, "email").send_keys("prueba@gmail.com")
        self.driver.find_element(By.CSS_SELECTOR, "#\\__BVID__18 .custom-control:nth-child(1) > .custom-control-label").click()
        self.driver.find_element(By.CSS_SELECTOR, "#\\__BVID__21 .custom-control:nth-child(2) > .custom-control-label").click()
        self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > #password").click()
        self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > #password").send_keys("prueba1234")
        self.driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(7)").click()
        self.driver.find_element(By.ID, "btn-abrir-popup").click()
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "username").send_keys("prueba5")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("prueba1234")
        self.driver.find_element(By.CSS_SELECTOR, ".mt-3").click()
        assert self.driver.find_element(By.ID, "welcomeID").text == "Welcome"
        assert self.driver.find_element(By.CSS_SELECTOR, "strong:nth-child(2)").text == "prueba5!"

    def test_wrong_sing_up(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.find_element(By.ID, "signIn").click()
        self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > #username").click()
        self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > #username").send_keys("prueba5")
        self.driver.find_element(By.ID, "email").click()
        self.driver.find_element(By.ID, "email").send_keys("prueba@gmail.com")
        self.driver.find_element(By.CSS_SELECTOR, "#\\__BVID__18 .custom-control:nth-child(1) > .custom-control-label").click()
        self.driver.find_element(By.CSS_SELECTOR, "#\\__BVID__21 .custom-control:nth-child(2) > .custom-control-label").click()
        self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > #password").click()
        self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > #password").send_keys("prueba1234")
        self.driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(7)").click()
        self.driver.find_element(By.ID, "btn-abrir-popup").click()
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "username").send_keys("prueba5")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("prueba1234")
        self.driver.find_element(By.CSS_SELECTOR, ".mt-3").click()
        text = self.driver.find_element(By.CSS_SELECTOR, "strong:nth-child(2)").text
        assert text != "decide!"


    