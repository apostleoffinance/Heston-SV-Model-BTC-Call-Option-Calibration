"""
Option Pricing Module
======================
This module provides option pricing functionality using various models:
- Heston model (semi-analytical)
- Monte Carlo simulation
- Black-Scholes model
"""

import numpy as np
import pandas as pd
from scipy.stats import norm
from typing import List, Optional
from .heston_model import HestonModel


class OptionPricer(HestonModel):
    """
    Option pricing class that extends HestonModel to provide multiple pricing methods.
    
    Supports pricing European call options using:
    - Heston semi-analytical formula
    - Monte Carlo simulation with Heston dynamics
    - Black-Scholes closed-form formula
    """
    
    def __init__(self, S0: float, r: float, kappa: float, theta: float,
                 sigma: float, rho: float, v0: float, 
                 option_type: str = 'call', pricer: str = 'heston'):
        """
        Initialize OptionPricer.
        
        Parameters:
        -----------
        S0 : float
            Initial stock/asset price
        r : float
            Risk-free interest rate
        kappa : float
            Mean reversion rate of volatility
        theta : float
            Long-term average volatility
        sigma : float
            Volatility of volatility
        rho : float
            Correlation between asset returns and volatility
        v0 : float
            Initial volatility
        option_type : str
            Type of option ('call' or 'put'), default: 'call'
        pricer : str
            Pricing method ('heston', 'monte_carlo', 'black_scholes')
        """
        super().__init__(S0, r, kappa, theta, sigma, rho, v0)
        self.option_type = option_type
        self.pricer = pricer
    
    def MC_call_pricing(self, S: np.ndarray, trading_days: int, 
                       strike: float) -> float:
        """
        Price European call option using Monte Carlo simulation.
        
        Parameters:
        -----------
        S : np.ndarray
            Simulated stock price paths from Monte Carlo
        trading_days : int
            Number of trading days to maturity
        strike : float
            Strike price
        
        Returns:
        --------
        float
            Call option price
        """
        # Extract terminal stock prices
        S_T = np.array([x[trading_days - 1] for x in S])
        
        # Calculate payoffs
        call_payoffs = np.maximum(S_T - strike, 1e-15)
        call_price = np.mean(call_payoffs)
        
        # Discount to present value
        call_price = call_price * np.exp(-self.r * (trading_days / 252))
        return call_price
    
    def BS_CALL(self, T: float, K: float) -> float:
        """
        Price European call option using Black-Scholes formula.
        
        Parameters:
        -----------
        T : float
            Time to maturity in years
        K : float
            Strike price
        
        Returns:
        --------
        float
            Call option price
        """
        N = norm.cdf
        d1 = ((np.log(self.S0 / K) + (self.r + self.sigma**2 / 2) * T) / 
              (self.sigma * np.sqrt(T)))
        d2 = d1 - self.sigma * np.sqrt(T)
        return self.S0 * N(d1) - K * np.exp(-self.r * T) * N(d2)
    
    def price_options(self, strikes: List[float], trading_days: int,
                     S: Optional[np.ndarray] = None) -> List[float]:
        """
        Price multiple options across different strikes.
        
        Parameters:
        -----------
        strikes : list of float
            List of strike prices
        trading_days : int
            Number of trading days to maturity
        S : np.ndarray, optional
            Simulated stock price paths (required for Monte Carlo pricing)
        
        Returns:
        --------
        list of float
            List of option prices corresponding to each strike
        
        Raises:
        -------
        ValueError
            If Monte Carlo pricer is selected but S is not provided
        """
        if self.pricer == 'heston' and self.option_type == 'call':
            option_prices = [
                self.heston_option_price(K, trading_days / 252) 
                for K in strikes
            ]
        
        elif self.pricer == 'monte_carlo' and self.option_type == 'call':
            if S is None:
                raise ValueError("Monte Carlo pricing requires simulated paths (S)")
            option_prices = [
                self.MC_call_pricing(S, trading_days, K) 
                for K in strikes
            ]
        
        elif self.pricer == 'black_scholes' and self.option_type == 'call':
            option_prices = [
                self.BS_CALL(trading_days / 252, K) 
                for K in strikes
            ]
        
        else:
            raise ValueError(
                f"Unsupported combination: pricer='{self.pricer}', "
                f"option_type='{self.option_type}'"
            )
        
        return option_prices


class OptionAnalyzer:
    """Helper class for analyzing option pricing results."""
    
    @staticmethod
    def calculate_pricing_error(model_prices: List[float], 
                               market_prices: List[float]) -> dict:
        """
        Calculate pricing errors between model and market prices.
        
        Parameters:
        -----------
        model_prices : list of float
            Model-predicted option prices
        market_prices : list of float
            Market-observed option prices
        
        Returns:
        --------
        dict
            Dictionary containing various error metrics
        """
        model_prices = np.array(model_prices)
        market_prices = np.array(market_prices)
        
        errors = model_prices - market_prices
        abs_errors = np.abs(errors)
        pct_errors = (errors / market_prices) * 100
        
        return {
            'mae': np.mean(abs_errors),
            'rmse': np.sqrt(np.mean(errors**2)),
            'mape': np.mean(np.abs(pct_errors)),
            'max_error': np.max(abs_errors),
            'mean_error': np.mean(errors)
        }
    
    @staticmethod
    def compare_pricers(strikes: List[float], market_prices: List[float],
                       heston_prices: List[float], mc_prices: List[float],
                       bs_prices: List[float]) -> pd.DataFrame:
        """
        Create a comparison table of different pricing methods.
        
        Parameters:
        -----------
        strikes : list of float
            Strike prices
        market_prices : list of float
            Market prices
        heston_prices : list of float
            Heston model prices
        mc_prices : list of float
            Monte Carlo prices
        bs_prices : list of float
            Black-Scholes prices
        
        Returns:
        --------
        pd.DataFrame
            Comparison table
        """
        import pandas as pd
        
        df = pd.DataFrame({
            'Strike': strikes,
            'Market': market_prices,
            'Heston': heston_prices,
            'Monte Carlo': mc_prices,
            'Black-Scholes': bs_prices,
            'Heston Error': np.abs(np.array(heston_prices) - np.array(market_prices)),
            'MC Error': np.abs(np.array(mc_prices) - np.array(market_prices)),
            'BS Error': np.abs(np.array(bs_prices) - np.array(market_prices))
        })
        
        return df
