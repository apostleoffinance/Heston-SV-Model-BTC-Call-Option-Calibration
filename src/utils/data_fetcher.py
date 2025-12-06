"""
Data Fetching Module
====================
This module handles all data fetching operations including:
- Stock/Cryptocurrency price data from Yahoo Finance
- Options data from Deribit API
- Treasury yield data for risk-free rate calculation
"""

import numpy as np
import pandas as pd
import requests
import yfinance as yf
from datetime import datetime, timedelta
from typing import Tuple, Dict


class DataFetcher:
    """Handles fetching and preprocessing of market data."""
    
    def __init__(self, ticker: str = 'BTC-USD'):
        """
        Initialize DataFetcher.
        
        Parameters:
        -----------
        ticker : str
            The ticker symbol for the asset (default: 'BTC-USD')
        """
        self.ticker = ticker
    
    def fetch_asset_data(self, start_date: str = '2014-01-01', 
                         end_date: datetime = None) -> pd.DataFrame:
        """
        Fetch historical asset price data from Yahoo Finance.
        
        Parameters:
        -----------
        start_date : str
            Start date for historical data (format: 'YYYY-MM-DD')
        end_date : datetime
            End date for historical data (default: today)
        
        Returns:
        --------
        pd.DataFrame
            DataFrame with asset price data and calculated returns
        """
        if end_date is None:
            end_date = datetime.today()
        
        # Try multiple times with increasing delay
        import time
        for attempt in range(3):
            try:
                asset_data = yf.download(self.ticker, start_date, end_date, 
                                        auto_adjust=True, progress=False)
                
                if len(asset_data) == 0:
                    raise ValueError("No data returned")
                
                df = pd.DataFrame(asset_data['Close'])
                df.reset_index(inplace=True)
                df.rename(columns={self.ticker: 'Close'}, inplace=True)
                df['Change in asset returns'] = df['Close'] / df['Close'].shift(1)
                
                return df
            except Exception as e:
                if attempt < 2:
                    print(f"  Warning: Attempt {attempt + 1} failed ({str(e)}). Retrying...")
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise Exception(f"Failed to fetch data after 3 attempts: {str(e)}")
    
    def calculate_rolling_volatility(self, df: pd.DataFrame, 
                                     window: int = 21, 
                                     trading_days: int = 365) -> pd.DataFrame:
        """
        Calculate rolling volatility for asset prices.
        
        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame with 'Close' price column
        window : int
            Rolling window size in days (default: 21)
        trading_days : int
            Number of trading days per year (default: 365 for crypto)
        
        Returns:
        --------
        pd.DataFrame
            DataFrame with added 'rolling_vol' column
        """
        prices = pd.Series(df['Close'])
        returns = prices.pct_change()
        # Use standard deviation (not variance) for volatility calculation
        rolling_std = returns.rolling(window=window).std()
        df['rolling_vol'] = rolling_std * np.sqrt(trading_days)
        
        return df
    
    def fetch_options_data(self, currency: str = 'BTC') -> pd.DataFrame:
        """
        Fetch options data from Deribit API.
        
        Parameters:
        -----------
        currency : str
            Currency for options (default: 'BTC')
        
        Returns:
        --------
        pd.DataFrame
            DataFrame with processed call options data
        """
        url = "https://www.deribit.com/api/v2/public/get_book_summary_by_currency"
        params = {"currency": currency, "kind": "option"}
        
        response = requests.get(url, params=params)
        options_data = pd.DataFrame(response.json()["result"])
        
        # Filter for call options only
        options_data = options_data[options_data["instrument_name"].str.endswith("C")].copy()
        
        # Extract strike and expiry information
        options_data["strike"] = options_data["instrument_name"].str.extract(r"-(\d+)-C")[0].astype(float)
        options_data["expiry"] = pd.to_datetime(
            options_data["instrument_name"].str.extract(r"-(\d+[A-Z]+\d+)-")[0], 
            format="%d%b%y", 
            errors="coerce"
        )
        options_data["contractSymbol"] = options_data["instrument_name"]
        options_data["strike_dates"] = pd.to_datetime(
            options_data["instrument_name"].str.extract(r"-(\d+[A-Z]+\d+)-")[0],
            format="%d%b%y",
            errors="coerce"
        ).dt.strftime("%Y-%m-%d")
        
        # Calculate mid prices and other fields
        options_data["lastPrice"] = (options_data["bid_price"] + options_data["ask_price"]) / 2
        options_data["bid"] = options_data["bid_price"]
        options_data["ask"] = options_data["ask_price"]
        options_data["impliedVolatility"] = options_data["mark_iv"]
        options_data["inTheMoney"] = options_data["strike"] < options_data["underlying_price"]
        options_data["contractSize"] = "REGULAR"
        options_data["currency"] = "USD"
        
        # Select relevant columns
        df_calls = options_data[[
            "contractSymbol", "strike", "strike_dates", "lastPrice", 
            "bid", "ask", "impliedVolatility", "inTheMoney", 
            "contractSize", "currency"
        ]]
        df_calls = df_calls.sort_values(by="strike_dates").reset_index(drop=True)
        
        return df_calls
    
    def fetch_treasury_data(self, days_back: int = 4) -> Dict[str, float]:
        """
        Fetch U.S. Treasury yield data.
        
        Parameters:
        -----------
        days_back : int
            Number of days back to fetch data (default: 4)
        
        Returns:
        --------
        dict
            Dictionary with treasury yields and calculated risk-free rate
        """
        tickers = ['^IRX', '^FVX', '^TNX', '^TYX']  # 3M, 5Y, 10Y, 30Y
        
        start_date = datetime.today() - timedelta(days=days_back)
        end_date = datetime.today()
        
        treasury_data = yf.download(tickers, start=start_date, end=end_date)
        
        df_treasury = pd.DataFrame(treasury_data['Close'])
        df_treasury.columns = ['3M', '5Y', '10Y', '30Y']
        df_treasury.reset_index(inplace=True)
        
        # Calculate risk-free rate from 3-month treasury yield
        three_month_yield = df_treasury['3M'].values[-1]
        r = np.log(1 + three_month_yield / 100)
        
        return {
            'treasury_data': df_treasury,
            'risk_free_rate': r,
            '3M_yield': three_month_yield
        }
    
    def prepare_data_for_mle(self, df: pd.DataFrame, 
                            window: int = 21) -> Tuple[list, list]:
        """
        Prepare data vectors for MLE parameter estimation.
        
        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame with calculated returns and volatility
        window : int
            Window size used for rolling calculations (default: 21)
        
        Returns:
        --------
        tuple
            (Q, V) where Q is change in asset returns and V is rolling volatility
        """
        Q = list(df['Change in asset returns'][window+1:])
        V = list(df['rolling_vol'][window+1:])
        
        return Q, V
