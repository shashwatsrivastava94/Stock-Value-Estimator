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

def valueAfterGrowth(value, growthRate):
	return value * growthRate

def startDCFEstimator(stockSymbol):
	## Setup
	print "----------Estimating value of " + stockSymbol + " using DCF Model----------"
	marginOfSafety = 0.25
	discountRate = 1.1
	year10Multiplier = 12
	numOfYearsInFuture = 10
	declineRate = 0.05
	scraper = DynamicsWebScraper(stockSymbol)

	# Scrape for the required data
	scraper.get("http://finance.yahoo.com/quote/%s/financials?ltr=1" % stockSymbol)
	scraper.performActionOnElement('//*[@id="main-0-Quote-Proxy"]/section/div[2]/section/div/section/div[2]/button[1]',
		lambda x: x.click())
	totalCashFlow = scraper.getElementOnCurrentPageUsingXpath('//*[@id="main-0-Quote-Proxy"]/section/div[2]/section/div/section/div[4]/table/tbody/tr[10]/td[2]/span/span/text()',
		lambda x: float(x.replace(",", "")))
	print "The total cash flow is %d" % totalCashFlow 

	capitalExpenditure = scraper.getElementOnCurrentPageUsingXpath('//*[@id="main-0-Quote-Proxy"]/section/div[2]/section/div/section/div[4]/table/tbody/tr[12]/td[2]/span/span/text()',
		lambda x: float(x.replace(",", "")) * -1)
	print "The capital expenditure is %d" % capitalExpenditure 

	fcfValue = totalCashFlow - capitalExpenditure
	print "The free cash flow is %d" % fcfValue

	scraper.performActionOnElement('//*[@id="main-0-Quote-Proxy"]/section/div[2]/section/div/section/div[2]/button[2]',
		lambda x: x.click())
	cashAndCashEq = scraper.getElementOnCurrentPageUsingXpath('//*[@id="main-0-Quote-Proxy"]/section/div[2]/section/div/section/div[4]/table/tbody/tr[3]/td[2]/span/span/text()',
		lambda x: float(x.replace(",", "")))
	print "Cash and cash equivalents are %d" % cashAndCashEq 

	debts = scraper.getElementOnCurrentPageUsingXpath('//*[@id="main-0-Quote-Proxy"]/section/div[2]/section/div/section/div[4]/table/tbody/tr[22]/td[2]/span/span/text()',
		lambda x: float(x.replace(",", "")))
	print "Total debts are %d" % debts

	expectedGrowthRate = scraper.getElementFromPageUsingXpath('http://finance.yahoo.com/quote/' + stockSymbol + '/analysts?ltr=1',
		'//*[@id="main-0-Quote-Proxy"]/section/div[2]/section/div/section/table[6]/tbody/tr[5]/td[2]/text()',
		lambda x: float(x.replace("%", "")))
	print "Expected growth rate is %s" % expectedGrowthRate 

	conservativeGrowthRate = 1 + ((expectedGrowthRate * (1 - marginOfSafety)) / 100)
	print "Conservative growth rate is %s" % conservativeGrowthRate 
	growthRate = conservativeGrowthRate - 1

	outstandingStockNum = scraper.getElementFromPageUsingXpath('http://finance.yahoo.com/quote/%s/key-statistics?ltr=1' % stockSymbol,
		'//*[@id="main-0-Quote-Proxy"]/section/div[2]/section/div/section/div[2]/div[2]/div/div[2]/table/tbody/tr[3]/td[2]/text()',
		formatOutstandingStock)
	print "Number of outstanding shares is %d" % outstandingStockNum 

	totalNpvFcf = 0
	year10FcfValue = 0
	for x in xrange(1, numOfYearsInFuture + 1):
		fcfValue = valueAfterGrowth(fcfValue, conservativeGrowthRate)
		growthRate *= (1 - declineRate)
		conservativeGrowthRate = 1 + growthRate
		# print "FCF value " + str(fcfValue) + " and the FCF NPV value " + str(fcfValue / (discountRate ** x))
		totalNpvFcf += float(fcfValue / (discountRate ** x))
		year10FcfValue = float(fcfValue / (discountRate ** x)) * year10Multiplier

	print "Total NPV FCF is %d" % totalNpvFcf
	print "Year 10 FCF Value is %d" % year10FcfValue

	companyValue = totalNpvFcf + year10FcfValue + cashAndCashEq - debts
	print "Company value is %d" % companyValue

	fairStockPrice = (companyValue * 1000) / float(outstandingStockNum)
	print "---------- The fair price of the company by DCF method is %.2f ----------" % fairStockPrice

	# Teardown 
	scraper.doneScraping()



