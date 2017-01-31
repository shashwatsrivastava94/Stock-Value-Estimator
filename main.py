import argparse
from PERatioEstimator import startPERatioEstimator

def main():
	parser = argparse.ArgumentParser(description="Estimate value of stocks by different methods")
	parser.add_argument("-stockSymbol")
	args = parser.parse_args()
	print args.stockSymbol

	startPERatioEstimator(args.stockSymbol)

main()