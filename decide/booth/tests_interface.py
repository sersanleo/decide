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

        self.assertEquals(self.driver.current_url,f'{self.live_server_url}/booth/suggesting/')

class AccesibilityInterfaceTests(StaticLiveServerTestCase):
# Esta clase de test requiere que la opción headless esté a False para su correcto funcionamiento
    def setUp(self):
        self.booth = BoothTests()
        self.booth.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(options=options)

        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.booth.tearDown()
        self.driver.quit()

    def test_accesibility_dalt_deutera_protan_success(self):
        self.driver.get(f'{self.live_server_url}/booth/')
        self.driver.find_element(By.XPATH, "//*[@role='button']").click()
        vis_types = self.driver.find_elements(By.XPATH, "//*[@role='menuitem']")
        vis_types[0].click()
        self.driver.find_element(By.ID, "username").send_keys("voter1")
        self.driver.find_element(By.ID, "password").send_keys("123")
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Single question voting").click()
        time.sleep(1)
        form_radios_uniq = self.driver.find_elements_by_tag_name("label")
        self.assertEquals(form_radios_uniq[0].value_of_css_property('background-color'),'rgba(82, 172, 255, 1)')

    def test_accesibility_dalt_tritan_succes(self):
        self.driver.get(f'{self.live_server_url}/booth/')
        self.driver.find_element(By.XPATH, "//*[@role='button']").click()
        vis_types = self.driver.find_elements(By.XPATH, "//*[@role='menuitem']")
        vis_types[1].click()
        self.driver.find_element(By.ID, "username").send_keys("voter1")
        self.driver.find_element(By.ID, "password").send_keys("123")
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Single question voting").click()
        time.sleep(1)
        form_radios_uniq = self.driver.find_elements_by_tag_name("label")
        self.assertEquals(form_radios_uniq[0].value_of_css_property('background-color'),'rgba(255, 102, 102, 1)')

    def test_accesibility_dalt_normal_succes(self):
        self.driver.get(f'{self.live_server_url}/booth/')
        self.driver.find_element(By.XPATH, "//*[@role='button']").click()
        vis_types = self.driver.find_elements(By.XPATH, "//*[@role='menuitem']")
        vis_types[2].click()
        self.driver.find_element(By.ID, "username").send_keys("voter1")
        self.driver.find_element(By.ID, "password").send_keys("123")
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Single question voting").click()
        time.sleep(1)
        form_radios_uniq = self.driver.find_elements_by_tag_name("label")
        self.assertEquals(form_radios_uniq[0].value_of_css_property('background-color'),'rgba(108, 117, 125, 1)')