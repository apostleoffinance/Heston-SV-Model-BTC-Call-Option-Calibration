"""
Simple Demo Script (No Live Data Required)
===========================================
This script demonstrates the Heston model functionality without fetching live data.
Uses synthetic/sample data for demonstration purposes.
"""

import sys
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models.heston_model import HestonModel
from models.option_pricer import OptionPricer
from utils.visualization import SimulationVisualizer, OptionVisualizer


def main():
    print("\n" + "="*70)
    print("HESTON MODEL DEMO (USING SAMPLE PARAMETERS)")
    print("="*70 + "\n")
    
    # Sample Heston parameters (realistic for BTC)
    S0 = 90000          # Current BTC price
    r = 0.04            # Risk-free rate (4%)
    kappa = 2.0         # Mean reversion rate
    theta = 0.04        # Long-term volatility
    sigma = 0.3         # Volatility of volatility
    rho = -0.7          # Correlation (leverage effect)
    v0 = 0.04           # Initial volatility
    
    print("Heston Model Parameters:")
    print(f"  S0 (Spot Price):          ${S0:,.2f}")
    print(f"  r (Risk-free Rate):        {r:.4f}")
    print(f"  κ (kappa):                 {kappa:.4f}")
    print(f"  θ (theta):                 {theta:.4f}")
    print(f"  σ (sigma):                 {sigma:.4f}")
    print(f"  ρ (rho):                   {rho:.4f}")
    print(f"  v0 (Initial Volatility):   {v0:.4f}\n")
    
    # Step 1: Create Heston Model
    print("Step 1: Creating Heston Model...")
    model = HestonModel(S0, r, kappa, theta, sigma, rho, v0)
    print("✓ Model created\n")
    
    # Step 2: Run Monte Carlo Simulation
    print("Step 2: Running Monte Carlo simulation...")
    T = 1  # 1 year
    N = 252  # Trading days
    mu = r  # Risk-neutral drift
    num_sims = 500
    
    S, V = model.heston_monte_carlo(T, N, mu, num_sims=num_sims)
    print(f"✓ Completed {num_sims} simulation paths\n")
    
    # Step 3: Price Options
    print("Step 3: Pricing options...")
    strikes = [85000, 87500, 90000, 92500, 95000]
    trading_days = 30  # 30 days to expiry
    
    # Heston pricing
    print("  - Heston semi-analytical pricing...")
    heston_pricer = OptionPricer(S0, r, kappa, theta, sigma, rho, v0,
                                 option_type='call', pricer='heston')
    heston_prices = heston_pricer.price_options(strikes, trading_days)
    
    # Monte Carlo pricing
    print("  - Monte Carlo pricing...")
    mc_pricer = OptionPricer(S0, r, kappa, theta, sigma, rho, v0,
                            option_type='call', pricer='monte_carlo')
    mc_prices = mc_pricer.price_options(strikes, trading_days, S)
    
    # Black-Scholes pricing
    print("  - Black-Scholes pricing...")
    bs_pricer = OptionPricer(S0, r, kappa, theta, sigma, rho, v0,
                            option_type='call', pricer='black_scholes')
    bs_prices = bs_pricer.price_options(strikes, trading_days)
    
    print("✓ Completed all pricing methods\n")
    
    # Step 4: Display Results
    print("Pricing Results:")
    print(f"{'Strike':<12} {'Heston':<15} {'Monte Carlo':<15} {'Black-Scholes':<15}")
    print("-" * 60)
    for i, strike in enumerate(strikes):
        print(f"${strike:<11,.0f} ${heston_prices[i]:<14,.2f} ${mc_prices[i]:<14,.2f} ${bs_prices[i]:<14,.2f}")
    print()
    
    # Step 5: Generate Visualizations
    print("Step 5: Generating visualizations...")
    os.makedirs('outputs', exist_ok=True)
    
    # Monte Carlo paths
    sim_viz = SimulationVisualizer()
    sim_viz.plot_sample_paths(S, 'BTC-USD', num_samples=10,
                              save_path='outputs/demo_mc_paths.png')
    print("✓ Saved: outputs/demo_mc_paths.png")
    
    # Option pricing comparison
    opt_viz = OptionVisualizer()
    opt_viz.plot_option_prices(strikes, 'BTC-USD', '30 days',
                              heston_prices=heston_prices,
                              mc_prices=mc_prices,
                              bs_prices=bs_prices,
                              save_path='outputs/demo_option_prices.png')
    print("✓ Saved: outputs/demo_option_prices.png")
    
    # Step 6: Save Results to CSV
    print("\nStep 6: Saving results...")
    results_df = pd.DataFrame({
        'Strike': strikes,
        'Heston': heston_prices,
        'Monte_Carlo': mc_prices,
        'Black_Scholes': bs_prices,
        'Heston_vs_BS_Diff': np.array(heston_prices) - np.array(bs_prices),
        'MC_vs_Heston_Diff': np.array(mc_prices) - np.array(heston_prices)
    })
    results_df.to_csv('outputs/demo_results.csv', index=False)
    print("✓ Saved: outputs/demo_results.csv\n")
    
    print("="*70)
    print("DEMO COMPLETE!")
    print("="*70)
    print("\nGenerated files:")
    print("  • outputs/demo_mc_paths.png - Monte Carlo simulation paths")
    print("  • outputs/demo_option_prices.png - Option pricing comparison")
    print("  • outputs/demo_results.csv - Detailed results table")
    print("\nNote: This demo uses sample parameters. Run 'python main.py' for")
    print("      full analysis with live market data when API is available.\n")


if __name__ == "__main__":
    main()
