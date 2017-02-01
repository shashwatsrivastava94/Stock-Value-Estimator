from lxml import etree
from selenium import webdriver

class DynamicsWebScraper:
	stockSymbol = None
	driver = webdriver.Chrome()

	def __init__(self, stockSymbol):
		self.stockSymbol = stockSymbol
		self.driver.implicitly_wait(5)

	def doneScraping(self):
		self.driver.quit()

	def getElementFromPageUsingXpath(self, pageURL, xpath, operation=None):
		self.driver.get(pageURL)
		pageSource = self.driver.page_source
		cleanPageSource = etree.HTML(pageSource)
		return operation(cleanPageSource.xpath(xpath)[0])
