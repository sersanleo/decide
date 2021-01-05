import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

  
def test_viewVisualizerGlobalLink():
	driver = webdriver.Chrome(executable_path="./chromedriver_ubuntu")
	driver.get("http://localhost:8000/visualizer/")
	driver.set_window_size(1386, 692)
	elements = driver.find_element(By.XPATH, "//a[contains(@href, \'/visualizer/global\')]").click()
	assert len(elements) > 0
	driver.find_element(By.LINK_TEXT, "Visualizar estadisticas globales").click()
	driver.close()


def test_visualizerGlobalTable1():
	driver = webdriver.Chrome(executable_path="./chromedriver_ubuntu")
	driver.get("http://localhost:8000/visualizer/")
	driver.set_window_size(1386, 692)
	driver.find_element(By.XPATH, "//a[contains(@href, \'/visualizer/global\')]").click()
	elements = driver.find_elements(By.CSS_SELECTOR, ".table:nth-child(4) th:nth-child(1)")
	assert len(elements) > 0
	elements = driver.find_elements(By.CSS_SELECTOR, ".table:nth-child(4) th:nth-child(2)")
	assert len(elements) > 0
	driver.find_element(By.CSS_SELECTOR, ".table:nth-child(4) th:nth-child(4)").click()
	driver.find_element(By.CSS_SELECTOR, ".table:nth-child(4) th:nth-child(3)").click()
	elements = driver.find_elements(By.CSS_SELECTOR, ".table:nth-child(4) th:nth-child(3)")
	assert len(elements) > 0
	elements = driver.find_elements(By.CSS_SELECTOR, ".table:nth-child(4) th:nth-child(4)")
	assert len(elements) > 0
	elements = driver.find_elements(By.CSS_SELECTOR, "th:nth-child(5)")
	assert len(elements) > 0
	elements = driver.find_elements(By.CSS_SELECTOR, "th:nth-child(6)")
	assert len(elements) > 0
	elements = driver.find_elements(By.CSS_SELECTOR, "th:nth-child(7)")
	assert len(elements) > 0
	driver.close()


def test_visualizerGlobalTable2():
	driver = webdriver.Chrome(executable_path="./chromedriver_ubuntu")
	driver.get("http://localhost:8000/visualizer/")
	driver.set_window_size(1386, 692)
	driver.find_element(By.XPATH, "//a[contains(@href, \'/visualizer/global\')]").click()
	elements = driver.find_elements(By.CSS_SELECTOR, ".table:nth-child(5) th:nth-child(1)")
	assert len(elements) > 0
	elements = driver.find_elements(By.CSS_SELECTOR, ".table:nth-child(5) th:nth-child(2)")
	assert len(elements) > 0
	elements = driver.find_elements(By.CSS_SELECTOR, ".table:nth-child(5) th:nth-child(3)")
	assert len(elements) > 0
	elements = driver.find_elements(By.CSS_SELECTOR, ".table:nth-child(5) th:nth-child(4)")
	assert len(elements) > 0
	driver.close()

def test_visualizerGlobalTable3():
	driver = webdriver.Chrome(executable_path="./chromedriver_ubuntu")
	driver.get("http://localhost:8000/visualizer/")
	driver.set_window_size(1386, 692)
	driver.find_element(By.XPATH, "//a[contains(@href, \'/visualizer/global\')]").click()
	elements = driver.find_elements(By.CSS_SELECTOR, ".table:nth-child(6) th:nth-child(1)")
	assert len(elements) > 0
	elements = driver.find_elements(By.CSS_SELECTOR, ".table:nth-child(6) th:nth-child(2)")
	assert len(elements) > 0
	elements = driver.find_elements(By.CSS_SELECTOR, ".table:nth-child(6) th:nth-child(3)")
	assert len(elements) > 0
	elements = driver.find_elements(By.CSS_SELECTOR, ".table:nth-child(6) th:nth-child(4)")
	assert len(elements) > 0
	driver.close()


	
def test_visualizerGlobalPercent():
	driver = webdriver.Chrome(executable_path="./chromedriver_ubuntu")
	driver.get("http://localhost:8000/visualizer/")
	driver.set_window_size(1386, 692)
	driver.find_element(By.XPATH, "//a[contains(@href, \'/visualizer/global\')]").click()
	elements = driver.find_elements(By.XPATH, "//div[@id=\'app-visualizer\']/div/div/table/tbody/tr/td[7]")
	verification = (elements.text).contains('%')
	assert verification
	elements = driver.find_elements(By.XPATH, "//div[@id=\'app-visualizer\']/div/div/table[3]/tbody/tr/td")
	verification = (elements.text).contains('%')
	assert verification
	elements = driver.find_elements(By.XPATH, "//div[@id=\'app-visualizer\']/div/div/table[3]/tbody/tr/td[2]")
	verification = (elements.text).contains('%')
	assert verification
	elements = driver.find_elements(By.XPATH, "//div[@id=\'app-visualizer\']/div/div/table[3]/tbody/tr/td[3]")
	verification = (elements.text).contains('%')
	assert verification
	elements = driver.find_elements(By.XPATH, "//div[@id=\'app-visualizer\']/div/div/table[3]/tbody/tr/td[4]")
	verification = (elements.text).contains('%')
	assert verification
	elements = driver.find_elements(By.XPATH, "//div[@id=\'app-visualizer\']/div/div/table/tbody/tr/td[6]")
	verification = (elements.text).contains('%')
	assert verification
	driver.close()
