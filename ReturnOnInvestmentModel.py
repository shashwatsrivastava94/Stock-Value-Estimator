from dynamicWebScraper import DynamicsWebScraper

def formatOutstandingStock(x):
	if "B" in x:
		return float(x.replace("B", "")) * 1000000000
	elif "M" in x:
		return float(x.replace("B", "")) * 1000000
	else: 
		## Shouldnt ever reach here
		print "---------- Error occured. Number of outstanding stock was read incorrectly----------"
		return float(x)

def calculateROI(scraper, stockSymbol):
	scraper.get('http://financials.morningstar.com/ratios/r.html?t=%s&region=usa&culture=en-US' % stockSymbol)

	roeArray = []
	for x in xrange(1, 11):
		roeArray.append(scraper.getElementOnCurrentPageUsingXpath('//*[@id="tab-profitability"]/table[2]/tbody/tr[12]/td[%d]/text()' % x,
				lambda x: float(x)))

	avgRoe = reduce(lambda x,y: x + y, roeArray) / len(roeArray)
	print "The average return on investment is %d" % avgRoe
	roeArray.sort()
	medianRoe = (roeArray[5] + roeArray[5]) / 2
	print "The median return on investment is %d" % medianRoe

	## use lower value to be conservative
	return min(avgRoe, medianRoe)

def ROIEstimator(stockSymbol):
	## Setup
	print "----------Estimating value of " + stockSymbol + " using ROI Model----------"
	marginOfSafety = 0.25
	discountRate = 1.1
	year10Multiplier = 12
	numOfYearsInFuture = 10
	historicalMarketReturn = 0.1
	declineRate = 0.05
	scraper = DynamicsWebScraper(stockSymbol)

	## Scrape for required data
	outstandingStockNum = scraper.getElementFromPageUsingXpath('http://finance.yahoo.com/quote/%s/key-statistics?ltr=1' % stockSymbol,
		'//*[@id="main-0-Quote-Proxy"]/section/div[2]/section/div/section/div[2]/div[2]/div/div[2]/table/tbody/tr[3]/td[2]/text()',
		formatOutstandingStock)
	print "Number of outstanding shares is %d" % outstandingStockNum 

	returnOnInvestment = calculateROI(scraper, stockSymbol)

	scraper.get("http://finance.yahoo.com/quote/%s/financials?ltr=1" % stockSymbol)
	scraper.performActionOnElement('//*[@id="main-0-Quote-Proxy"]/section/div[2]/section/div/section/div[2]/button[2]',
		lambda x: x.click())
	shareholdersEquity = scraper.getElementOnCurrentPageUsingXpath('//*[@id="main-0-Quote-Proxy"]/section/div[2]/section/div/section/div[4]/table/tbody/tr[37]/td[2]/span/span/text()',
		lambda x: float(x))
	print "The total shareholders equity is %d" % shareholdersEquity

	scraper.get('http://finance.yahoo.com/quote/%s/key-statistics?ltr=1' % stockSymbol)
	payoutRatio = scraper.getElementOnCurrentPageUsingXpath('//*[@id="main-0-Quote-Proxy"]/section/div[2]/section/div/section/div[2]/div[2]/div/div[3]/table/tbody/tr[6]/td[2]/text()',
		lambda x: float(x.replace("%", "")))
	print "Payout ratio is %d" % payoutRatio
	forwardDividendYield = scraper.getElementOnCurrentPageUsingXpath('//*[@id="main-0-Quote-Proxy"]/section/div[2]/section/div/section/div[2]/div[2]/div/div[3]/table/tbody/tr[2]/td[2]/text()',
		lambda x : float(x.replace("%", "")))
	print "The forward dividend yield is %d" % forwardDividendYield

	sustainableGrowthRate = (1 - marginOfSafety) * (returnOnInvestment / 100) * (1 - (payoutRatio / 100))
	print "The conservative sustainable growth rate is %d" % sustainableGrowthRate

	shareholderEquityPerShare = shareholdersEquity / outstandingStockNum
	dividendNPVs = []
	year10Dividend.append(dividendNPVs)

	year10EquityPerShare = shareholderEquityPerShare
	for x in xrange(numOfYearsInFuture):
		year10EquityPerShare *= sustainableGrowthRate
		newDividendNPV = (dividendNPVs[len(dividendNPVs) - 1] * sustainableGrowthRate) / discountRate 
		dividendNPVs.append(newDividendNPV)

	year10EquityPerShareNPV = year10EquityPerShare / (discountRate ** numOfYearsInFuture)
	print "The year 10 equity per share is %d" % year10EquityPerShareNPV
	print "The divident NPVs are " + str(newDividendNPV)

	




