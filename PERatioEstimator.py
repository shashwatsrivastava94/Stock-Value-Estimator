from lxml import etree
from selenium import webdriver
import time

def getMedianHistoricalPE(driver, stockSymbol):
	driver.get("http://financials.morningstar.com/valuation/price-ratio.html?t=%s" % stockSymbol)
	pageSource = driver.page_source
	cleanPageSource = etree.HTML(pageSource)
	return float(cleanPageSource.xpath('//*[@id="currentValuationTable"]/tbody/tr[2]/td[4]/text()')[0])

def getEarningsPerShare(driver, stockSymbol):
	driver.get('http://financials.morningstar.com/ratios/r.html?t=%s&region=usa&culture=en-US' % stockSymbol)
	pageSource = driver.page_source
	cleanPageSource = etree.HTML(pageSource)
	return float(cleanPageSource.xpath('//*[@id="financials"]/table/tbody/tr[12]/td[11]/text()')[0])

def getExpectedGrowthRate(driver, stockSymbol):
	driver.get('http://finance.yahoo.com/quote/%s/analysts?ltr=1' % stockSymbol)
	pageSource = driver.page_source
	cleanPageSource = etree.HTML(pageSource)
	growthRate = str(cleanPageSource.xpath('//*[@id="main-0-Quote-Proxy"]/section/div[2]/section/div/section/table[6]/tbody/tr[5]/td[2]/text()')[0])
	return float(growthRate.replace("%", ""))

def startPERatioEstimator(stockSymbol):
	## Setup
	print "----------Estimating value of " + stockSymbol + " using PE Ratio Method----------"
	driver = webdriver.Chrome()
	htmlParser = etree.HTMLParser()
	marginOfSafety = 0.25
	discountRate = 1.1
	numOfYearsInFuture = 5

	# Run each of the estimators
	medianHistoricalPE = getMedianHistoricalPE(driver, stockSymbol)
	print "Median historical PE is %d" % medianHistoricalPE
	earningsPerShareTTM = getEarningsPerShare(driver, stockSymbol)
	print "Earnings per share ttm is %s" % earningsPerShareTTM
	expectedGrowthRate = getExpectedGrowthRate(driver, stockSymbol)
	print "Expected growth rate is %s" % expectedGrowthRate

	estimatedGrowthRate = 1 + ((expectedGrowthRate * (1 - marginOfSafety)) / 100)
	print "Conservative growth rate is %s" % estimatedGrowthRate

	fiveYearPriceTarget = earningsPerShareTTM * (estimatedGrowthRate ** numOfYearsInFuture) * medianHistoricalPE
	print "Value in five years is %s" % fiveYearPriceTarget

	currentPriceValue = fiveYearPriceTarget / (discountRate ** numOfYearsInFuture)

	print "Estimated value of %s right now is %d" % (stockSymbol, currentPriceValue)

	# teardown
	driver.quit()
