from lxml import etree
from selenium import webdriver
import time

class DynamicsWebScraper:
	stockSymbol = None
	driver = webdriver.Chrome()

	def __init__(self, stockSymbol):
		self.stockSymbol = stockSymbol
		self.driver.implicitly_wait(5)

	def doneScraping(self):
		self.driver.quit()

	def get(self, url):
		self.driver.get(url)

	def getElementOnCurrentPageUsingXpath(self, xpath, operation=None):
		pageSource = self.driver.page_source
		cleanPageSource = etree.HTML(pageSource)
		return operation(cleanPageSource.xpath(xpath)[0])

	def getElementFromPageUsingXpath(self, pageURL, xpath, operation=None):
		self.driver.get(pageURL)
		pageSource = self.driver.page_source
		cleanPageSource = etree.HTML(pageSource)
		return operation(cleanPageSource.xpath(xpath)[0])

	def performActionOnElement(self, elementXPath, action):
		element = self.driver.find_element_by_xpath(elementXPath)
		action(element)

