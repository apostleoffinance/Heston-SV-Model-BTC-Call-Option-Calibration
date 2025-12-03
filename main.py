"""
Main Execution Script
=====================
This script orchestrates the entire Heston model workflow:
1. Fetch and process market data
2. Estimate Heston parameters using MLE
3. Run Monte Carlo simulations
4. Price options using multiple methods
5. Generate visualizations and reports
"""

import sys
import os
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to prevent display issues

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.data_fetcher import DataFetcher
from models.heston_model import HestonModel
from models.mle_optimizer import MLEOptimizer
from models.option_pricer import OptionPricer, OptionAnalyzer
from utils.visualization import SimulationVisualizer, OptionVisualizer, DataVisualizer


def main():
    """Main execution function."""
    
    print("\n" + "="*70)
    print("BITCOIN OPTIONS PRICING WITH HESTON MODEL")
    print("="*70 + "\n")
    
    # Configuration
    TICKER = 'BTC-USD'
    START_DATE = '2014-01-01'
    WINDOW = 21
    TRADING_DAYS_PER_YEAR = 365
    NUM_SIMULATIONS = 1000
    MONTE_CARLO_DAYS = 252
    
    # Step 1: Fetch and process asset data
    print("Step 1: Fetching asset data...")
    data_fetcher = DataFetcher(ticker=TICKER)
    df = data_fetcher.fetch_asset_data(start_date=START_DATE)
    df = data_fetcher.calculate_rolling_volatility(df, window=WINDOW, 
                                                   trading_days=TRADING_DAYS_PER_YEAR)
    print(f"✓ Fetched {len(df)} days of historical data")
    
    # Current spot price
    S0 = df['Close'].iloc[-1]
    print(f"✓ Current BTC price: ${S0:,.2f}")
    
    # Step 2: Fetch treasury data for risk-free rate
    print("\nStep 2: Fetching risk-free rate...")
    treasury_info = data_fetcher.fetch_treasury_data()
    r = treasury_info['risk_free_rate']
    print(f"✓ Risk-free rate: {r:.6f} ({treasury_info['3M_yield']:.4f}% annual)")
    
    # Step 3: Prepare data for MLE
    print("\nStep 3: Preparing data for parameter estimation...")
    Q, V = data_fetcher.prepare_data_for_mle(df, window=WINDOW)
    print(f"✓ Prepared {len(Q)} observations for MLE")
    
    # Step 4: Estimate Heston parameters
    print("\nStep 4: Estimating Heston parameters via MLE...")
    print("(This may take a few minutes...)")
    mle = MLEOptimizer(Q, V, r, n_guesses=20)
    results = mle.estimate_parameters_robust()
    mle.print_estimation_results(results)
    
    # Extract parameters
    kappa = results['k']
    theta = results['theta']
    sigma = results['sigma']
    rho = results['rho']
    v0 = df['rolling_vol'].mean()
    
    # Step 5: Fetch options data
    print("Step 5: Fetching options data from Deribit...")
    df_calls = data_fetcher.fetch_options_data(currency='BTC')
    
    # Adjust option prices by current BTC price
    df_calls['lastPrice'] *= S0
    
    # Select a specific expiration date (find one with at least 7 days to expiry)
    today_date = datetime.today().strftime('%Y-%m-%d')
    df_calls['days_to_expiry'] = df_calls['strike_dates'].apply(
        lambda x: len(pd.bdate_range(start=today_date, end=x))
    )
    
    # Filter for options with at least 7 trading days to expiry
    valid_expiries = df_calls[df_calls['days_to_expiry'] >= 7]['strike_dates'].unique()
    
    if len(valid_expiries) == 0:
        print("Warning: No options with sufficient time to expiry found. Using closest available.")
        exp_date = df_calls['strike_dates'].iloc[0]
    else:
        # Select the first valid expiry with multiple strikes
        for exp in sorted(valid_expiries)[:5]:  # Check first 5 valid expiries
            temp_df = df_calls[df_calls['strike_dates'] == exp]
            if len(temp_df) >= 5:  # Need at least 5 strikes
                exp_date = exp
                break
        else:
            exp_date = valid_expiries[0]
    
    df_calls_filtered = df_calls[df_calls['strike_dates'] == exp_date].reset_index(drop=True)
    strikes = df_calls_filtered['strike'].values
    market_prices = df_calls_filtered['lastPrice'].values
    
    print(f"✓ Fetched {len(df_calls)} option contracts")
    print(f"✓ Selected expiry date: {exp_date}")
    print(f"✓ Number of strikes for selected expiry: {len(strikes)}")
    
    # Calculate trading days to expiration
    today_date = datetime.today().strftime('%Y-%m-%d')
    trading_days = len(pd.bdate_range(start=today_date, end=exp_date))
    
    # Ensure we have at least 1 trading day
    if trading_days < 1:
        trading_days = 1
    
    print(f"✓ Trading days to expiration: {trading_days}")
    
    # Step 6: Run Monte Carlo simulation
    print("\nStep 6: Running Monte Carlo simulation...")
    model = HestonModel(S0, r, kappa, theta, sigma, rho, v0)
    T = 1  # 1 year
    N = MONTE_CARLO_DAYS
    mu = r
    S, V = model.heston_monte_carlo(T, N, mu, num_sims=NUM_SIMULATIONS)
    print(f"✓ Completed {NUM_SIMULATIONS} simulation paths")
    
    # Step 7: Price options using different methods
    print("\nStep 7: Pricing options...")
    
    # Heston semi-analytical
    print("  - Heston semi-analytical pricing...")
    heston_pricer = OptionPricer(S0, r, kappa, theta, sigma, rho, v0,
                                 option_type='call', pricer='heston')
    heston_prices = heston_pricer.price_options(strikes, trading_days)
    
    # Monte Carlo
    print("  - Monte Carlo pricing...")
    mc_pricer = OptionPricer(S0, r, kappa, theta, sigma, rho, v0,
                            option_type='call', pricer='monte_carlo')
    mc_prices = mc_pricer.price_options(strikes, trading_days, S)
    
    # Black-Scholes
    print("  - Black-Scholes pricing...")
    bs_pricer = OptionPricer(S0, r, kappa, theta, sigma, rho, v0,
                            option_type='call', pricer='black_scholes')
    bs_prices = bs_pricer.price_options(strikes, trading_days)
    
    print("✓ Completed all pricing methods")
    
    # Step 8: Analyze pricing errors
    print("\nStep 8: Analyzing pricing errors...")
    analyzer = OptionAnalyzer()
    
    # Filter out any NaN values
    valid_mask = ~(np.isnan(heston_prices) | np.isnan(mc_prices) | 
                   np.isnan(bs_prices) | np.isnan(market_prices))
    
    if not valid_mask.any():
        print("Warning: All pricing results contain NaN. Check parameters and data.")
    else:
        heston_errors = analyzer.calculate_pricing_error(
            [heston_prices[i] for i in range(len(heston_prices)) if valid_mask[i]], 
            [market_prices[i] for i in range(len(market_prices)) if valid_mask[i]]
        )
        mc_errors = analyzer.calculate_pricing_error(
            [mc_prices[i] for i in range(len(mc_prices)) if valid_mask[i]], 
            [market_prices[i] for i in range(len(market_prices)) if valid_mask[i]]
        )
        bs_errors = analyzer.calculate_pricing_error(
            [bs_prices[i] for i in range(len(bs_prices)) if valid_mask[i]], 
            [market_prices[i] for i in range(len(market_prices)) if valid_mask[i]]
        )
        
        print("\nPricing Error Summary:")
        print(f"{'Method':<20} {'MAE':<12} {'RMSE':<12} {'MAPE (%)':<12}")
        print("-" * 56)
        print(f"{'Heston':<20} ${heston_errors['mae']:<11.2f} ${heston_errors['rmse']:<11.2f} {heston_errors['mape']:<11.2f}")
        print(f"{'Monte Carlo':<20} ${mc_errors['mae']:<11.2f} ${mc_errors['rmse']:<11.2f} {mc_errors['mape']:<11.2f}")
        print(f"{'Black-Scholes':<20} ${bs_errors['mae']:<11.2f} ${bs_errors['rmse']:<11.2f} {bs_errors['mape']:<11.2f}")
    
    # Step 9: Generate visualizations
    print("\nStep 9: Generating visualizations...")
    
    # Create output directory if it doesn't exist
    output_dir = 'outputs'
    os.makedirs(output_dir, exist_ok=True)
    
    # Simulation visualizations
    sim_viz = SimulationVisualizer()
    sim_viz.plot_all_paths(S, TICKER, NUM_SIMULATIONS,
                           save_path=f'{output_dir}/mc_all_paths.png')
    sim_viz.plot_sample_paths(S, TICKER, num_samples=10,
                              save_path=f'{output_dir}/mc_sample_paths.png')
    
    # Option pricing visualization
    opt_viz = OptionVisualizer()
    opt_viz.plot_option_prices(strikes, TICKER, exp_date,
                              heston_prices=heston_prices,
                              mc_prices=mc_prices,
                              bs_prices=bs_prices,
                              market_prices=market_prices,
                              save_path=f'{output_dir}/option_prices_comparison.png')
    
    print(f"✓ Visualizations saved to '{output_dir}/' directory")
    
    # Step 10: Save results
    print("\nStep 10: Saving results...")
    
    # Create comparison DataFrame
    comparison_df = pd.DataFrame({
        'Strike': strikes,
        'Market': market_prices,
        'Heston': heston_prices,
        'Monte_Carlo': mc_prices,
        'Black_Scholes': bs_prices,
        'Heston_Error': np.abs(np.array(heston_prices) - market_prices),
        'MC_Error': np.abs(np.array(mc_prices) - market_prices),
        'BS_Error': np.abs(np.array(bs_prices) - market_prices)
    })
    comparison_df.to_csv(f'{output_dir}/option_pricing_results.csv', index=False)
    
    # Save parameters
    params_df = pd.DataFrame({
        'Parameter': ['S0', 'r', 'kappa', 'theta', 'sigma', 'rho', 'v0'],
        'Value': [S0, r, kappa, theta, sigma, rho, v0],
        'Description': [
            'Initial stock price',
            'Risk-free rate',
            'Mean reversion rate',
            'Long-term volatility',
            'Volatility of volatility',
            'Correlation coefficient',
            'Initial volatility'
        ]
    })
    params_df.to_csv(f'{output_dir}/heston_parameters.csv', index=False)
    
    print(f"✓ Results saved to '{output_dir}/' directory")
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE!")
    print("="*70 + "\n")
    print("Output files generated:")
    print(f"  • {output_dir}/mc_all_paths.png")
    print(f"  • {output_dir}/mc_sample_paths.png")
    print(f"  • {output_dir}/option_prices_comparison.png")
    print(f"  • {output_dir}/option_pricing_results.csv")
    print(f"  • {output_dir}/heston_parameters.csv")
    print("\n")


if __name__ == "__main__":
    main()
