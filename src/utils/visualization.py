"""
Visualization Module
====================
This module provides visualization functions for:
- Monte Carlo simulation paths
- Option pricing comparisons
- Volatility surfaces
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Optional
from datetime import datetime


class SimulationVisualizer:
    """Handles visualization of Monte Carlo simulation results."""
    
    @staticmethod
    def plot_all_paths(S: np.ndarray, ticker: str, num_sims: int,
                       save_path: Optional[str] = None) -> None:
        """
        Plot all Monte Carlo simulation paths.
        
        Parameters:
        -----------
        S : np.ndarray
            Simulated stock price paths
        ticker : str
            Asset ticker symbol
        num_sims : int
            Number of simulations
        save_path : str, optional
            Path to save the figure
        """
        plt.figure(figsize=(12, 6))
        plt.plot(S.T, color="blue", alpha=0.1)
        
        plt.xlabel("Trading Days", fontsize=12)
        plt.ylabel("Stock Price ($)", fontsize=12)
        plt.title(f"Monte Carlo Simulation of {ticker} Price (All {num_sims} Paths)",
                 fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
    
    @staticmethod
    def plot_sample_paths(S: np.ndarray, ticker: str, num_samples: int = 10,
                         save_path: Optional[str] = None) -> None:
        """
        Plot sample paths with mean and confidence bands.
        
        Parameters:
        -----------
        S : np.ndarray
            Simulated stock price paths
        ticker : str
            Asset ticker symbol
        num_samples : int
            Number of sample paths to display (default: 10)
        save_path : str, optional
            Path to save the figure
        """
        plt.figure(figsize=(12, 6))
        
        # Plot sample paths
        for i in range(min(num_samples, S.shape[0])):
            plt.plot(S[i, :], alpha=0.7, linewidth=1)
        
        # Calculate and plot statistics
        mean_path = np.mean(S, axis=0)
        percentile_5 = np.percentile(S, 5, axis=0)
        percentile_95 = np.percentile(S, 95, axis=0)
        
        plt.plot(mean_path, color="black", linewidth=2.5, 
                label="Mean Path", linestyle='--')
        plt.fill_between(range(S.shape[1]), percentile_5, percentile_95,
                        color="gray", alpha=0.3, label="5%-95% Range")
        
        plt.xlabel("Trading Days", fontsize=12)
        plt.ylabel("Stock Price ($)", fontsize=12)
        plt.title(f"Monte Carlo Simulation of {ticker} Price ({num_samples} Sample Paths)",
                 fontsize=14, fontweight='bold')
        plt.legend(loc='best', fontsize=10)
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
    
    @staticmethod
    def plot_volatility_paths(V: np.ndarray, num_samples: int = 10,
                             save_path: Optional[str] = None) -> None:
        """
        Plot volatility paths from Monte Carlo simulation.
        
        Parameters:
        -----------
        V : np.ndarray
            Simulated volatility paths
        num_samples : int
            Number of sample paths to display (default: 10)
        save_path : str, optional
            Path to save the figure
        """
        plt.figure(figsize=(12, 6))
        
        # Plot sample volatility paths
        for i in range(min(num_samples, V.shape[0])):
            plt.plot(V[i, :], alpha=0.7, linewidth=1)
        
        # Calculate and plot statistics
        mean_vol = np.mean(V, axis=0)
        plt.plot(mean_vol, color="red", linewidth=2.5,
                label="Mean Volatility", linestyle='--')
        
        plt.xlabel("Trading Days", fontsize=12)
        plt.ylabel("Volatility", fontsize=12)
        plt.title("Simulated Volatility Paths", fontsize=14, fontweight='bold')
        plt.legend(loc='best', fontsize=10)
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()


class OptionVisualizer:
    """Handles visualization of option pricing results."""
    
    @staticmethod
    def plot_option_prices(strikes: List[float], ticker: str, exp_date: str,
                          heston_prices: Optional[List[float]] = None,
                          mc_prices: Optional[List[float]] = None,
                          bs_prices: Optional[List[float]] = None,
                          market_prices: Optional[List[float]] = None,
                          save_path: Optional[str] = None) -> None:
        """
        Plot option prices from different pricing models and market data.
        
        Parameters:
        -----------
        strikes : list of float
            Strike prices
        ticker : str
            Asset ticker symbol
        exp_date : str
            Expiration date
        heston_prices : list of float, optional
            Heston model prices
        mc_prices : list of float, optional
            Monte Carlo prices
        bs_prices : list of float, optional
            Black-Scholes prices
        market_prices : list of float, optional
            Market prices
        save_path : str, optional
            Path to save the figure
        """
        plt.figure(figsize=(12, 7))
        
        if heston_prices is not None and len(heston_prices) > 0:
            plt.scatter(strikes, heston_prices, label='Heston', 
                       s=100, marker='o', alpha=0.7)
        if bs_prices is not None and len(bs_prices) > 0:
            plt.scatter(strikes, bs_prices, label='Black-Scholes',
                       s=100, marker='s', alpha=0.7)
        if mc_prices is not None and len(mc_prices) > 0:
            plt.scatter(strikes, mc_prices, label='Heston Monte Carlo',
                       s=100, marker='^', alpha=0.7)
        if market_prices is not None and len(market_prices) > 0:
            plt.scatter(strikes, market_prices, label='Market Data',
                       s=100, marker='D', alpha=0.7, color='red')
        
        plt.xlabel('Strike Price ($)', fontsize=12)
        plt.ylabel('Option Price ($)', fontsize=12)
        plt.title(f'{ticker} Call Option Prices - Expiry: {exp_date}',
                 fontsize=14, fontweight='bold')
        plt.legend(title="Pricing Method", fontsize=10, loc='best')
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
    
    @staticmethod
    def plot_pricing_errors(strikes: List[float], 
                           model_prices: List[float],
                           market_prices: List[float],
                           model_name: str,
                           save_path: Optional[str] = None) -> None:
        """
        Plot pricing errors between model and market prices.
        
        Parameters:
        -----------
        strikes : list of float
            Strike prices
        model_prices : list of float
            Model prices
        market_prices : list of float
            Market prices
        model_name : str
            Name of the pricing model
        save_path : str, optional
            Path to save the figure
        """
        errors = np.array(model_prices) - np.array(market_prices)
        pct_errors = (errors / np.array(market_prices)) * 100
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Absolute errors
        ax1.bar(strikes, errors, alpha=0.7, color='steelblue')
        ax1.axhline(y=0, color='r', linestyle='--', linewidth=1)
        ax1.set_xlabel('Strike Price ($)', fontsize=12)
        ax1.set_ylabel('Pricing Error ($)', fontsize=12)
        ax1.set_title(f'{model_name} Absolute Pricing Errors', 
                     fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Percentage errors
        ax2.bar(strikes, pct_errors, alpha=0.7, color='coral')
        ax2.axhline(y=0, color='r', linestyle='--', linewidth=1)
        ax2.set_xlabel('Strike Price ($)', fontsize=12)
        ax2.set_ylabel('Pricing Error (%)', fontsize=12)
        ax2.set_title(f'{model_name} Percentage Pricing Errors',
                     fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
    
    @staticmethod
    def plot_comparison_table(comparison_df: pd.DataFrame,
                             save_path: Optional[str] = None) -> None:
        """
        Display a formatted comparison table as a figure.
        
        Parameters:
        -----------
        comparison_df : pd.DataFrame
            DataFrame with pricing comparison data
        save_path : str, optional
            Path to save the figure
        """
        fig, ax = plt.subplots(figsize=(14, len(comparison_df) * 0.5 + 2))
        ax.axis('tight')
        ax.axis('off')
        
        table = ax.table(cellText=comparison_df.values,
                        colLabels=comparison_df.columns,
                        cellLoc='center',
                        loc='center',
                        bbox=[0, 0, 1, 1])
        
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 2)
        
        # Style header
        for i in range(len(comparison_df.columns)):
            table[(0, i)].set_facecolor('#4CAF50')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        # Alternate row colors
        for i in range(1, len(comparison_df) + 1):
            for j in range(len(comparison_df.columns)):
                if i % 2 == 0:
                    table[(i, j)].set_facecolor('#f0f0f0')
        
        plt.title('Option Pricing Comparison', 
                 fontsize=16, fontweight='bold', pad=20)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()


class DataVisualizer:
    """Handles visualization of market data."""
    
    @staticmethod
    def plot_price_history(df: pd.DataFrame, ticker: str,
                          save_path: Optional[str] = None) -> None:
        """
        Plot historical price data.
        
        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame with 'Date' and 'Close' columns
        ticker : str
            Asset ticker symbol
        save_path : str, optional
            Path to save the figure
        """
        plt.figure(figsize=(14, 6))
        plt.plot(df['Date'], df['Close'], linewidth=2, color='steelblue')
        
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price ($)', fontsize=12)
        plt.title(f'{ticker} Historical Price', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
    
    @staticmethod
    def plot_rolling_volatility(df: pd.DataFrame, ticker: str,
                               save_path: Optional[str] = None) -> None:
        """
        Plot rolling volatility.
        
        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame with 'Date' and 'rolling_vol' columns
        ticker : str
            Asset ticker symbol
        save_path : str, optional
            Path to save the figure
        """
        plt.figure(figsize=(14, 6))
        plt.plot(df['Date'], df['rolling_vol'], 
                linewidth=2, color='coral')
        
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Volatility', fontsize=12)
        plt.title(f'{ticker} Rolling Volatility (21-day)', 
                 fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
