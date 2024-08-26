This code evaluates a trading strategy using historical trade data and compares its performance against a benchmark index (SPY).

Key Functions

	•	assess_strategy(trade_file, starting_value, fixed_cost, floating_cost):
	•	Inputs:
	•	trade_file: Path to the CSV file containing trade data.
	•	starting_value: Initial portfolio value.
	•	fixed_cost: Fixed transaction cost per trade.
	•	floating_cost: Percentage-based transaction cost.
	•	Process:
	•	Reads trade data and filters SPY data for the relevant date range.
	•	Simulates trading activity based on the input file, adjusting portfolio values for each trade.
	•	Calculates daily portfolio values, including transaction costs.
	•	Compares portfolio performance with the SPY benchmark.
	•	Outputs:
	•	Prints the Sharpe Ratio, Average Daily Return, Cumulative Return, Volatility, and Final Portfolio Value for both the portfolio and the benchmark.
	•	get_adj_close(date, symbol, column_name="Adj Close", data_folder="./data"):
	•	Retrieves the adjusted closing price of a stock on a given date from CSV files.
	•	calculate_info(daily_prices_df, risk_free_rate=0, sample_freq=252):
	•	Inputs:
	•	daily_prices_df: DataFrame containing daily portfolio values.
	•	risk_free_rate: Risk-free rate for Sharpe Ratio calculation.
	•	sample_freq: Number of trading days in a year (default is 252).
	•	Outputs:
	•	Returns Sharpe Ratio, Average Daily Return, Cumulative Return, Standard Deviation of Daily Returns, and Final Portfolio Value.
	•	get_data(start, end, symbols, column_name="Adj Close", include_spy=True, data_folder="./data"):
	•	Inputs:
	•	start and end: Date range for fetching historical data.
	•	symbols: List of stock symbols to include.
	•	include_spy: Boolean to include SPY data.
	•	Outputs:
	•	Returns a DataFrame of adjusted closing prices for the specified symbols and date range.
	•	assess_portfolio(start_date, end_date, symbols, allocations, starting_value=1000000, risk_free_rate=0.0, sample_freq=252, plot_returns=True):
	•	Inputs:
	•	start_date and end_date: Date range for the analysis.
	•	symbols: List of stock symbols in the portfolio.
	•	allocations: Proportions of the portfolio allocated to each stock.
	•	Outputs:
	•	Returns Sharpe Ratio, Average Daily Return, Cumulative Return, Standard Deviation of Daily Returns, and Final Portfolio Value.

Usage

	•	Run the main() function to execute the strategy assessment and print the results.
	•	Ensure that the assess_strategy function is configured with the correct paths and parameters for your specific dataset.

This code provides a framework for assessing trading strategies and portfolio performance using historical data, with a focus on transaction costs and comparative analysis against a benchmark index.
