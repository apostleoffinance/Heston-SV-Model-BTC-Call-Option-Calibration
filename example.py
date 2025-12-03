"""
Quick Example Script
====================
A simple example demonstrating basic usage of the Heston model modules.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models.heston_model import HestonModel
from models.option_pricer import OptionPricer
import numpy as np


def quick_example():
    """Run a quick example of Heston model pricing."""
    
    print("="*60)
    print("QUICK HESTON MODEL EXAMPLE")
    print("="*60)
    
    # Example parameters
    S0 = 50000      # Current BTC price
    r = 0.05        # Risk-free rate (5%)
    kappa = 2.0     # Mean reversion rate
    theta = 0.04    # Long-term volatility
    sigma = 0.3     # Vol of vol
    rho = -0.7      # Correlation
    v0 = 0.04       # Initial volatility
    
    print("\nModel Parameters:")
    print(f"  S0 (Spot Price):    ${S0:,.0f}")
    print(f"  r (Risk-free):      {r:.2%}")
    print(f"  κ (Kappa):          {kappa:.2f}")
    print(f"  θ (Theta):          {theta:.4f}")
    print(f"  σ (Sigma):          {sigma:.2f}")
    print(f"  ρ (Rho):            {rho:.2f}")
    print(f"  v0 (Init Vol):      {v0:.4f}")
    
    # Create model
    model = HestonModel(S0, r, kappa, theta, sigma, rho, v0)
    
    # Run Monte Carlo simulation
    print("\nRunning Monte Carlo simulation (100 paths)...")
    T = 1           # 1 year
    N = 252         # Trading days
    mu = r          # Drift
    num_sims = 100
    
    S, V = model.heston_monte_carlo(T, N, mu, num_sims)
    print(f"✓ Completed {num_sims} simulations")
    
    # Calculate statistics
    final_prices = S[:, -1]
    print(f"\nFinal Price Statistics:")
    print(f"  Mean:               ${np.mean(final_prices):,.2f}")
    print(f"  Std Dev:            ${np.std(final_prices):,.2f}")
    print(f"  Min:                ${np.min(final_prices):,.2f}")
    print(f"  Max:                ${np.max(final_prices):,.2f}")
    
    # Price some options
    print("\nPricing Call Options:")
    strikes = [48000, 50000, 52000]
    trading_days = 30  # 30 days to expiration
    
    # Heston pricing
    heston_pricer = OptionPricer(S0, r, kappa, theta, sigma, rho, v0,
                                 option_type='call', pricer='heston')
    heston_prices = heston_pricer.price_options(strikes, trading_days)
    
    # Black-Scholes pricing
    bs_pricer = OptionPricer(S0, r, kappa, theta, sigma, rho, v0,
                            option_type='call', pricer='black_scholes')
    bs_prices = bs_pricer.price_options(strikes, trading_days)
    
    print(f"\n{'Strike':<10} {'Heston':<12} {'Black-Scholes':<15} {'Difference'}")
    print("-" * 50)
    for K, hp, bp in zip(strikes, heston_prices, bs_prices):
        diff = hp - bp
        print(f"${K:<9,.0f} ${hp:<11,.2f} ${bp:<14,.2f} ${diff:>9,.2f}")
    
    print("\n" + "="*60)
    print("Example complete! Run main.py for full analysis.")
    print("="*60 + "\n")


if __name__ == "__main__":
    quick_example()
