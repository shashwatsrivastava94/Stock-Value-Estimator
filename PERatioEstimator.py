from dynamicWebScraper import DynamicsWebScraper
import time

def startPERatioEstimator(stockSymbol):
	## Setup
	print "----------Estimating value of " + stockSymbol + " using PE Ratio Method----------"
	marginOfSafety = 0.25
	discountRate = 1.1
	numOfYearsInFuture = 5
	scraper = DynamicsWebScraper(stockSymbol)

	# Run each of the estimators
	medianHistoricalPE = scraper.getElementFromPageUsingXpath("http://financials.morningstar.com/valuation/price-ratio.html?t=" + stockSymbol,
	 '//*[@id="currentValuationTable"]/tbody/tr[2]/td[4]/text()', lambda x: float(x))
	print "Median historical PE is %d" % medianHistoricalPE

	earningsPerShareTTM = scraper.getElementFromPageUsingXpath("http://financials.morningstar.com/ratios/r.html?t=" + stockSymbol + "&region=usa&culture=en-US",
		'//*[@id="financials"]/table/tbody/tr[12]/td[11]/text()', lambda x: float(x))
	print "Earnings per share ttm is %s" % earningsPerShareTTM

	expectedGrowthRate = scraper.getElementFromPageUsingXpath('http://finance.yahoo.com/quote/' + stockSymbol + '/analysts?ltr=1',
		'//*[@id="main-0-Quote-Proxy"]/section/div[2]/section/div/section/table[6]/tbody/tr[5]/td[2]/text()',
		lambda x: float(x.replace("%", "")))

	print "Expected growth rate is %s" % expectedGrowthRate

	scraper.doneScraping()

	estimatedGrowthRate = 1 + ((expectedGrowthRate * (1 - marginOfSafety)) / 100)
	print "Conservative growth rate is %s" % estimatedGrowthRate

	fiveYearPriceTarget = earningsPerShareTTM * (estimatedGrowthRate ** numOfYearsInFuture) * medianHistoricalPE
	print "Value in five years is %s" % fiveYearPriceTarget

	currentPriceValue = fiveYearPriceTarget / (discountRate ** numOfYearsInFuture)

	print "Estimated value of %s right now is %d" % (stockSymbol, currentPriceValue)

	# teardown
