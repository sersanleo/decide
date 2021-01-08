from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from booth.tests import BoothTests

import time

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------TEST DE INTERFAZ DE LOGIN-----------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

class LoginInterfaceTests(StaticLiveServerTestCase):
    def setUp(self):
        self.booth = BoothTests()
        self.booth.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.booth.tearDown()
        self.driver.quit()

    def test_interface_login_success(self):
        self.driver.get(f'{self.live_server_url}/booth/')
        self.driver.find_element_by_id('username').send_keys("voter1")
        self.driver.find_element_by_id('password').send_keys("123",Keys.ENTER)

        #Cuando el login es correcto, se redirige a la página de dashboard
        self.assertEquals(self.driver.current_url,f'{self.live_server_url}/booth/dashboard/')

    def test_interface_login_fail(self):
        #Se loguea con un usuario inexistente
        self.driver.get(f'{self.live_server_url}/booth/')
        self.driver.find_element_by_id('username').send_keys("badvoter1")
        self.driver.find_element_by_id('password').send_keys("badpass1",Keys.ENTER)

        #Cuando el login es incorrecto, se mantiene en la página y aparece una alerta
        alert = self.driver.find_element_by_id('loginFail')
        self.assertEquals(alert.text,'El usuario no está registrado en el sistema.')
        self.assertEquals(self.driver.current_url,f'{self.live_server_url}/booth/dashboard/')

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------TEST DE INTERFAZ DE SUGGESTING------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

class SuggestingInterfaceTests(StaticLiveServerTestCase):
    
    def setUp(self):
        self.booth = BoothTests()
        self.booth.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.booth.tearDown()
        self.driver.quit()

    def test_interface_create_suggestion_fail_date_before_now(self):
        self.driver.get(f'{self.live_server_url}/booth/')
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "username").send_keys("voter1")
        self.driver.find_element(By.ID, "password").send_keys("123")
        self.driver.find_element(By.ID, "password").send_keys(Keys.ENTER)

        self.driver.find_element(By.ID, "sugBtn").click()
        self.driver.find_element_by_id("suggestingTitle").send_keys("test1")
        self.driver.find_element_by_id("suggestingDate").click()
        self.driver.find_element_by_id("suggestingDate").send_keys("04")
        self.driver.find_element_by_id("suggestingDate").send_keys("01")
        self.driver.find_element_by_id("suggestingDate").send_keys("2020")
        self.driver.find_element_by_id("suggestingContent").send_keys("test1")
        self.driver.find_element_by_id("submitSugForm").click()
        #time.sleep(2)
        self.assertEquals(self.driver.current_url,f'{self.live_server_url}/booth/suggesting/')


    def test_interface_create_suggestion_success(self):
        self.driver.get(f'{self.live_server_url}/booth/')
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "username").send_keys("voter1")
        self.driver.find_element(By.ID, "password").send_keys("123")
        self.driver.find_element(By.ID, "password").send_keys(Keys.ENTER)
        
        self.driver.find_element(By.ID, "sugBtn").click()
        self.driver.find_element_by_id("suggestingTitle").send_keys("test1")
        self.driver.find_element_by_id("suggestingDate").click()
        self.driver.find_element_by_id("suggestingDate").send_keys("01")
        self.driver.find_element_by_id("suggestingDate").send_keys("01")
        self.driver.find_element_by_id("suggestingDate").send_keys("2022")
        self.driver.find_element_by_id("suggestingContent").send_keys("test1")
        self.driver.find_element_by_id("submitSugForm").click()
        #time.sleep(2)
        self.assertEquals(self.driver.current_url,f'{self.live_server_url}/booth/dashboard/')

    def test_interface_create_suggestion_fail_empty_suggestingTitle(self):
        self.driver.get(f'{self.live_server_url}/booth/')
        self.driver.find_element(By.ID, "username").send_keys("voter1")
        self.driver.find_element(By.ID, "password").send_keys("123")
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()

        self.driver.find_element(By.ID, "sugBtn").click()
        self.driver.find_element_by_id("suggestingDate").click()
        self.driver.find_element_by_id("suggestingDate").send_keys("04")
        self.driver.find_element_by_id("suggestingDate").send_keys("01")
        self.driver.find_element_by_id("suggestingDate").send_keys("2022")
        self.driver.find_element(By.ID, "suggestingContent").send_keys("test1")
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
        #time.sleep(2)
        self.assertEquals(self.driver.current_url,f'{self.live_server_url}/booth/suggesting/')

    def test_interface_create_suggestion_fail_empty_suggestingDate(self):
        self.driver.get(f'{self.live_server_url}/booth/')
        self.driver.find_element(By.ID, "username").send_keys("voter1")
        self.driver.find_element(By.ID, "password").send_keys("123")
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()

        self.driver.find_element(By.ID, "sugBtn").click()
        self.driver.find_element(By.ID, "suggestingTitle").send_keys("test1")
        self.driver.find_element(By.ID, "suggestingContent").send_keys("test1")
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
        #time.sleep(2)
        self.assertEquals(self.driver.current_url,f'{self.live_server_url}/booth/suggesting/')

    def test_interface_create_suggestion_fail_empty_suggestingContent(self):
        self.driver.get(f'{self.live_server_url}/booth/')
        self.driver.find_element(By.ID, "username").send_keys("voter1")
        self.driver.find_element(By.ID, "password").send_keys("123")
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()

        self.driver.find_element(By.ID, "sugBtn").click()
        self.driver.find_element(By.ID, "suggestingTitle").send_keys("test1")
        self.driver.find_element_by_id("suggestingDate").click()
        self.driver.find_element_by_id("suggestingDate").send_keys("04")
        self.driver.find_element_by_id("suggestingDate").send_keys("01")
        self.driver.find_element_by_id("suggestingDate").send_keys("2022")
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
        #time.sleep(2)
        self.assertEquals(self.driver.current_url,f'{self.live_server_url}/booth/suggesting/')

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------TEST DE INTERFAZ DE BOOTH-----------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

class BoothInterfaceTests(StaticLiveServerTestCase):

    def setUp(self):
        self.booth = BoothTests()
        self.booth.setUp()

        options = webdriver.ChromeOptions()
        options.headless = False
        self.driver = webdriver.Chrome(options=options)

        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.booth.tearDown()
        self.driver.quit()

    # def test_interface_vote_question_unique_no_vote_failure(self):
    #     self.driver.get(f'{self.live_server_url}/booth/')
    #     self.driver.find_element(By.ID, "username").send_keys("voter1")
    #     self.driver.find_element(By.ID, "password").send_keys("123")
    #     self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
    #     self.driver.find_element(By.LINK_TEXT, "Single question voting").click()
    #     self.driver.find_element(By.LINK_TEXT, "Enviar").click()
    #     alert = self.driver.find_elements_by_id('alertVoteMessage')
    #     self.assertTrue(len(alert)<1)
    
    # def test_interface_vote_question_multi_no_vote_failure(self):
    #     self.driver.get(f'{self.live_server_url}/booth/')
    #     self.driver.find_element(By.ID, "username").send_keys("voter1")
    #     self.driver.find_element(By.ID, "password").send_keys("123")
    #     self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
    #     self.driver.find_element(By.LINK_TEXT, "Single question voting").click()
    #     self.driver.find_element(By.LINK_TEXT, "Enviar").click()
    #     alert = self.driver.find_elements_by_id('alertVoteMessage')
    #     self.assertTrue(len(alert)<1)

    
    # def test_interface_vote_question_rank_no_vote_failure(self):
    #     self.driver.get(f'{self.live_server_url}/booth/')
    #     self.driver.find_element(By.ID, "username").send_keys("voter1")
    #     self.driver.find_element(By.ID, "password").send_keys("123")
    #     self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
    #     self.driver.find_element(By.LINK_TEXT, "Single question voting").click()
    #     button = self.driver.find_elements_by_id('rankSendButton')
    #     self.assertTrue(len(button)<1)

    def test_interface_vote_success(self):
        self.driver.get(f'{self.live_server_url}/booth/')
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "username").send_keys("voter1")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("123")
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Single question voting").click()
        time.sleep(1)
        # form_radios_uniq = self.driver.find_elements_by_tag_name("label")
        # form_radios_uniq[0].click()
        self.driver.find_element(By.CSS_SELECTOR, "#\BVID17 .btn").click()
        self.driver.find_element(By.ID, "envButton").click()
        time.sleep(2)
        alert = self.driver.find_element(By.ID, "alertVoteMessage")
        self.assertEquals(alert.text,'Conglatulations. Your vote has been sent')
        self.driver.find_element(By.LINK_TEXT, "Siguiente pregunta >>").click()
        time.sleep(2)

        form_radios_mult = self.driver.find_elements_by_tag_name("label")
        for i in form_radios_mult:
            i.click()
        self.driver.find_element(By.LINK_TEXT, "Enviar").click()
        alert = self.driver.find_element(By.ID, "alertVoteMessage")
        self.assertEquals(alert.text,'Conglatulations. Your vote has been sent')
        self.driver.find_element(By.LINK_TEXT, "Siguiente pregunta >>").click()
        time.sleep(2)

        form_radios_rank = self.driver.find_elements_by_tag_name("label")
        for i in form_radios_rank:
            i.click()
        self.driver.find_element(By.ID, "rankSendButton").click()
        self.driver.find_element(By.ID, "alertVoteMessage").click()
        self.driver.find_element(By.LINK_TEXT, "Finalizar votación").click()
        self.assertEquals(self.driver.current_url,f'{self.live_server_url}/booth/dashboard/')
        time.sleep(2)
