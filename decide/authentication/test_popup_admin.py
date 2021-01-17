from authentication.models import UserProfile
from django.contrib import auth
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from base.tests import BaseTestCase
from rest_framework.test import APIClient, APITestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from base import mods

from voting.models import Voting

class AppDynamicsJob(StaticLiveServerTestCase):
    def setUp(self):
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        super().setUp()

    def test_app_dynamics_job(self):
        driver = self.driver
        driver.get(f'{self.live_server_url}/admin/')
        driver.set_window_size(1386, 692)
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("admin")
        driver.find_element_by_id("id_password").click()
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("qwerty")
        driver.find_element_by_xpath("//input[@value='Log in']").click()
        driver.find_element_by_id("btn-abrir-popup").click()
        driver.close()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()