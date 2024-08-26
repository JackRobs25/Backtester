import pandas as pd
import math

# change this back to what the project brief says!!!
def assess_strategy(trade_file = "./trades/trades.csv", starting_value = 1000000, fixed_cost = 9.95, floating_cost = 0.005):
    trades = pd.read_csv(trade_file, parse_dates=['Date'])
    
    symbols = trades['Symbol'].unique()
    
    spy_data = pd.read_csv('data/SPY.csv', index_col='Date', parse_dates=True, usecols=['Date'])
    
    # Filter SPY dates between start_date and end_date
    start_date = trades['Date'].min()
    end_date = trades['Date'].max()
    spy_data = spy_data[(spy_data.index >= start_date) & (spy_data.index <= end_date)]

    # Initialize daily_portfolio_values using trading days
    daily_portfolio_values = pd.DataFrame(index=spy_data.index)
    daily_portfolio_values['CASH'] = float(starting_value)
  

    for symbol in symbols:
        daily_portfolio_values[symbol] = 0.0


    for date in pd.date_range(start_date, end_date):
        normalized_date = date.normalize()
        prev_date = normalized_date - pd.Timedelta(days=1)
        prev_row = daily_portfolio_values.loc[prev_date].copy() if prev_date in daily_portfolio_values.index else daily_portfolio_values.iloc[0].copy()


        if date in trades['Date'].values:
            # Update the row if there is a trade on this day
            trades_on_day = trades[trades['Date'] == date]
            for index, trade in trades_on_day.iterrows():
                symbol = trade["Symbol"]
                direction = trade["Direction"]
                shares = trade["Shares"]

                price = get_adj_close(date, symbol)
                stock_value = price * shares

                if direction == "BUY":
                    prev_row['CASH'] -= stock_value + fixed_cost + (stock_value*floating_cost)
                    prev_row[symbol] += shares
                elif direction == "SELL":
                    prev_row['CASH'] += stock_value - fixed_cost - (stock_value*floating_cost)
                    prev_row[symbol] -= shares
                    
        # Update the current day's row with the computed changes
        daily_portfolio_values.loc[date] = prev_row
    
    df = pd.DataFrame(index=spy_data.index)
    df['Portfolio Value'] = daily_portfolio_values['CASH']  # Start with CASH values
    # Add the current adjusted close value of all stocks to the Portfolio Value each day
    for date in pd.date_range(start_date, end_date):
        for symbol in symbols:
            df.loc[df.index == date, 'Portfolio Value'] += daily_portfolio_values.loc[date, symbol] * get_adj_close(date, symbol)


    

    daily_portfolio_values = df

    SR, ADR, CR, SD, final = calculate_info(daily_portfolio_values)
    SR_bench, ADR_bench, CR_bench, SD_bench, final_bench = assess_portfolio(trades['Date'].min(), trades['Date'].max(), ['^SPX'], [1.0])

    print("Start Date: ", trades['Date'].min())
    print("Start Date: ", trades['Date'].max())
    print("\n")
    print("Portfolio Sharpe Ratio: ", SR)
    print("Benchmark Sharpe Ratio: ", SR_bench)
    print("\n")
    print("Portfolio ADR: ", ADR)
    print("Benchmark ADR: ", ADR_bench)
    print("\n")
    print("Portfolio CR: ", CR)
    print("Benchmark CR: ", CR_bench)
    print("\n")
    print("Portfolio SD: ", SD)
    print("Benchmark SD: ", SD_bench)
    print("\n")
    print("Final Portfolio value: ", final)





    return daily_portfolio_values

def get_adj_close(date, symbol, column_name="Adj Close", data_folder="./data"):
    df = pd.read_csv('Data/' + symbol + '.csv')
    row = df[df['Date'].str.strip() == date.date().strftime('%Y-%m-%d')]
    if row.empty:
        return 0 
    adj_close = row[column_name].values[0]
    return adj_close

def calculate_info(daily_prices_df, risk_free_rate=0, sample_freq=252):
    # Multiply each column by the allocation to that stock
    cumulative_return = (daily_prices_df.iloc[-1] / daily_prices_df.iloc[0]) - 1
    # pct_change() --> Fractional change between the current and a prior element
    daily_returns = daily_prices_df.pct_change().dropna()
    average_daily_return = daily_returns.mean()
    stdev_daily_return = daily_returns.std()
    # Calculate Sharpe Ratio
    excess_daily_returns = daily_returns - risk_free_rate
    sharpe_ratio = (excess_daily_returns.mean() / excess_daily_returns.std()) * math.sqrt(sample_freq)
    end_value = daily_prices_df.iloc[-1]
    return sharpe_ratio.values[0], average_daily_return.values[0], cumulative_return.values[0], stdev_daily_return.values[0], end_value.values[0]



############### Project 1 code (adjusted slightly) ##################

def get_data(start, end, symbols, column_name="Adj Close", include_spy=True, data_folder="./data"):
    dates = pd.date_range(start, end)
    df1 = pd.DataFrame(index=dates)
    df2 = pd.read_csv('data/SPY.csv', index_col='Date', parse_dates=True, usecols=['Date', column_name])
    df2.rename(columns={column_name: "SPY"}, inplace=True)
    df1 = df1.join(df2, how='inner')
    for symbol in symbols:
        tmp_df = pd.read_csv(data_folder + '/'+ symbol + ".csv", index_col='Date', parse_dates=True, usecols=['Date', column_name])
        tmp_df.rename(columns={column_name: symbol}, inplace=True)
        df1 = df1.join(tmp_df, how='left', rsuffix='_'+symbol)
    if (not include_spy):
        df1.drop('SPY', axis=1, inplace=True)
    return df1

def assess_portfolio (start_date, end_date, symbols, allocations,
                      starting_value=1000000, risk_free_rate=0.0,
                      sample_freq=252, plot_returns=True):
    daily_prices_df = get_data(start_date, end_date, symbols)
    # Normalize stock prices to the first day
    normalized_prices = daily_prices_df / daily_prices_df.iloc[0]
    # Multiply each column by the allocation to that stock
    allocated_prices = normalized_prices.iloc[:, 1:] * allocations
    # Multiply normalized allocations by starting portfolio dollar value
    portfolio_values = allocated_prices * starting_value
    # Sum each date (across the stocks) to get daily portfolio dollar value
    daily_portfolio_value = portfolio_values.sum(axis=1)
    cumulative_return = (daily_portfolio_value.iloc[-1] / daily_portfolio_value.iloc[0]) - 1
    # pct_change() --> Fractional change between the current and a prior element
    daily_returns = daily_portfolio_value.pct_change().dropna()
    average_daily_return = daily_returns.mean()
    stdev_daily_return = daily_returns.std()
    # Calculate Sharpe Ratio
    excess_daily_returns = daily_returns - risk_free_rate
    sharpe_ratio = (excess_daily_returns.mean() / excess_daily_returns.std()) * math.sqrt(sample_freq)
    end_value = daily_portfolio_value.iloc[-1]


    return sharpe_ratio, average_daily_return, cumulative_return, stdev_daily_return, end_value 

#####################################



def main():
    assess_strategy()


if __name__ == "__main__":
    main()
