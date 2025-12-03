# Quick Start Guide

## Installation

1. **Navigate to project directory**:
   ```bash
   cd Heston_model_btc
   ```

2. **Create virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Project

### Option 1: Demo Script (Recommended First Run)

```bash
python demo.py
```

**What it does**:
- Demonstrates core functionality with sample parameters
- No internet connection required
- Runs 500 Monte Carlo simulations
- Prices options using 3 methods
- Generates visualizations
- Saves results to `outputs/`

**Expected runtime**: < 30 seconds

**Output location**: `outputs/` directory (demo_*.png, demo_results.csv)

**Perfect for**: Testing the installation, learning the API, offline usage

### Option 2: Full Analysis (Requires Internet)

```bash
python main.py
```

**What it does**:
- Fetches historical Bitcoin data (2014-present) from Yahoo Finance
- Estimates Heston parameters using MLE
- Runs 1000 Monte Carlo simulations
- Fetches live options data from Deribit
- Prices options using 3 methods
- Generates comprehensive visualizations
- Saves results to `outputs/`

**Expected runtime**: 5-10 minutes (depending on your machine)

**Output location**: `outputs/` directory

**Note**: If you see "Failed download" errors, Yahoo Finance API may be temporarily unavailable. Use `demo.py` instead.

## Understanding the Output

### Files Generated in `outputs/`

1. **mc_all_paths.png**
   - Shows all Monte Carlo simulation paths
   - Blue lines = simulated price trajectories

2. **mc_sample_paths.png**
   - 10 sample paths with statistics
   - Black dashed line = mean path
   - Gray shaded area = 5%-95% confidence interval

3. **option_prices_comparison.png**
   - Scatter plot comparing pricing methods
   - Red diamonds = actual market prices
   - Other markers = model prices

4. **option_pricing_results.csv**
   - Detailed table with all results
   - Columns: Strike, Market, Heston, Monte Carlo, Black-Scholes, Errors

5. **heston_parameters.csv**
   - Estimated model parameters
   - Includes descriptions

### Console Output

You'll see progress through these steps:
1. ✓ Fetching asset data
2. ✓ Fetching risk-free rate
3. ✓ Preparing data for MLE
4. ✓ Estimating parameters (longest step)
5. ✓ Fetching options data
6. ✓ Running Monte Carlo
7. ✓ Pricing options
8. ✓ Analyzing errors
9. ✓ Generating visualizations
10. ✓ Saving results

## Customization

### Change Parameters

Edit `config.py`:

```python
# Increase simulations for more accuracy
NUM_SIMULATIONS = 5000

# Change rolling window
ROLLING_WINDOW = 30

# More initial guesses for better parameter estimation
N_GUESSES = 30
```

### Use Different Dates

In `main.py` or create your own script:

```python
from src.utils.data_fetcher import DataFetcher

fetcher = DataFetcher(ticker='BTC-USD')
df = fetcher.fetch_asset_data(start_date='2020-01-01')
```

### Price Specific Strikes

```python
from src.models.option_pricer import OptionPricer

# Your parameters
pricer = OptionPricer(S0=50000, r=0.05, kappa=2.0, 
                     theta=0.04, sigma=0.3, rho=-0.7, v0=0.04,
                     option_type='call', pricer='heston')

# Your strikes
strikes = [45000, 48000, 50000, 52000, 55000]
trading_days = 30

prices = pricer.price_options(strikes, trading_days)
```

## Interpreting Results

### Heston Parameters

- **κ (kappa)**: 0.5-5.0
  - Higher = volatility reverts to mean faster
  - Typical: 1-3

- **θ (theta)**: 0-1
  - Long-term average volatility level
  - Higher = more volatile in long run

- **σ (sigma)**: 0-5
  - Volatility of volatility
  - Higher = more uncertainty in volatility

- **ρ (rho)**: -1 to 0
  - Usually negative (leverage effect)
  - More negative = stronger inverse relationship

### Pricing Errors

- **MAE < $500**: Good fit
- **MAPE < 5%**: Excellent fit
- **RMSE**: Check relative to option prices

### Model Comparison

- **Heston**: Best for capturing volatility smile
- **Monte Carlo**: Flexible but slower
- **Black-Scholes**: Simple baseline (often underestimates)

## Troubleshooting

### MLE Optimization Fails
```
ValueError: Optimization failed for all attempts
```
**Solution**: Increase `N_GUESSES` in `config.py`

### Data Fetch Errors
```
Connection error or empty data
```
**Solution**: 
- Check internet connection
- Yahoo Finance/Deribit might be temporarily down
- Try again later

### Import Errors
```
ModuleNotFoundError: No module named 'X'
```
**Solution**: 
```bash
pip install -r requirements.txt
```

### Slow Performance
**Solutions**:
- Reduce `NUM_SIMULATIONS` in `config.py`
- Reduce `N_GUESSES` for faster parameter estimation
- Use fewer time steps in Monte Carlo

## Next Steps

1. **Review the visualizations** in `outputs/`
2. **Check the CSV files** for detailed results
3. **Experiment** with different parameters
4. **Read the methodology** in README.md
5. **Explore the code** - each module is well-documented

## Common Workflows

### 1. Compare Multiple Expiries
```python
exp_dates = ['2025-01-10', '2025-02-14', '2025-03-21']
for date in exp_dates:
    # Filter options and price
    # Compare results
```

### 2. Sensitivity Analysis
```python
kappas = [1.0, 2.0, 3.0, 4.0]
for k in kappas:
    model = HestonModel(S0, r, k, theta, sigma, rho, v0)
    # Price and compare
```

### 3. Backtest Parameters
```python
# Estimate on training data
# Test on validation data
# Compare out-of-sample performance
```

## Resources

- **Full Documentation**: README.md
- **Project Structure**: PROJECT_SUMMARY.md
- **Code Examples**: example.py
- **Main Pipeline**: main.py
- **Individual Modules**: src/models/ and src/utils/

## Getting Help

1. Check this guide
2. Read the docstrings in the code
3. Review the README.md
4. Check the original notebook for reference

---

**Ready to go? Start with:**
```bash
python main.py
```
