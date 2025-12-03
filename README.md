# Bitcoin Options Pricing with Heston Stochastic Volatility Model

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A comprehensive implementation of the Heston stochastic volatility model for pricing Bitcoin options. This project includes parameter estimation via Maximum Likelihood Estimation (MLE), Monte Carlo simulation, and multiple option pricing methods.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Methodology](#methodology)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)

## 🔍 Overview

This project implements a sophisticated options pricing framework using the **Heston stochastic volatility model**, specifically tailored for Bitcoin (BTC) options. Unlike the Black-Scholes model which assumes constant volatility, the Heston model captures the dynamic nature of volatility, making it particularly suitable for cryptocurrency markets.

### What This Project Does

1. **Fetches Historical Data**: Retrieves Bitcoin price history from Yahoo Finance and options data from Deribit
2. **Estimates Model Parameters**: Uses Maximum Likelihood Estimation to calibrate Heston model parameters from historical data
3. **Simulates Price Paths**: Generates Monte Carlo simulations of future Bitcoin prices with stochastic volatility
4. **Prices Options**: Compares three pricing methods:
   - Heston semi-analytical formula
   - Monte Carlo simulation
   - Black-Scholes baseline
5. **Generates Analytics**: Creates comprehensive visualizations and performance metrics

## ✨ Features

- **Modular Architecture**: Clean, well-organized code structure with separate modules for different functionalities
- **Multiple Pricing Methods**: Compare Heston, Monte Carlo, and Black-Scholes approaches
- **Robust Parameter Estimation**: MLE optimization with multiple initial guesses and methods
- **Comprehensive Visualizations**: Generate publication-quality charts and graphs
- **Real Market Data**: Integrates with Yahoo Finance and Deribit API
- **Error Analysis**: Detailed pricing error metrics (MAE, RMSE, MAPE)
- **Configurable**: Centralized configuration for easy parameter adjustment

## 📁 Project Structure

```
Heston_model_btc/
│
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── config.py                          # Configuration parameters
├── main.py                            # Main execution script
│
├── src/                               # Source code
│   ├── __init__.py
│   ├── models/                        # Core models
│   │   ├── __init__.py
│   │   ├── heston_model.py           # Heston model implementation
│   │   ├── option_pricer.py          # Option pricing methods
│   │   └── mle_optimizer.py          # MLE parameter estimation
│   │
│   └── utils/                         # Utility modules
│       ├── __init__.py
│       ├── data_fetcher.py           # Data fetching and processing
│       └── visualization.py          # Plotting and visualization
│
├── outputs/                           # Generated outputs
│   ├── mc_all_paths.png              # Monte Carlo simulation paths
│   ├── mc_sample_paths.png           # Sample paths with statistics
│   ├── option_prices_comparison.png  # Pricing comparison chart
│   ├── option_pricing_results.csv    # Detailed results table
│   └── heston_parameters.csv         # Estimated parameters
│
├── tests/                             # Unit tests (optional)
│
└── Heston_BTC (1).ipynb              # Original Jupyter notebook (reference)
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone or navigate to the repository**:
   ```bash
   cd Heston_model_btc
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

### Quick Demo (Recommended First)

Run the demo script with sample parameters (no internet required):

```bash
python demo.py
```

This demonstrates the full functionality without requiring live data fetching.

### Full Analysis (Requires Internet)

Run the main script to execute the entire pipeline with live market data:

```bash
python main.py
```

This will:
1. Fetch historical Bitcoin data from Yahoo Finance
2. Estimate Heston parameters via MLE
3. Run Monte Carlo simulations
4. Price options using all methods
5. Generate visualizations and save results to `outputs/`

**Note:** If Yahoo Finance API is temporarily unavailable, use `demo.py` instead.

### Advanced Usage

#### Using Individual Modules

```python
from src.utils.data_fetcher import DataFetcher
from src.models.heston_model import HestonModel
from src.models.option_pricer import OptionPricer

# Fetch data
fetcher = DataFetcher(ticker='BTC-USD')
df = fetcher.fetch_asset_data(start_date='2020-01-01')

# Create Heston model
model = HestonModel(S0=50000, r=0.05, kappa=2.0, 
                   theta=0.04, sigma=0.3, rho=-0.7, v0=0.04)

# Run simulation
S, V = model.heston_monte_carlo(T=1, N=252, mu=0.05, num_sims=1000)

# Price options
pricer = OptionPricer(S0=50000, r=0.05, kappa=2.0, 
                     theta=0.04, sigma=0.3, rho=-0.7, v0=0.04,
                     option_type='call', pricer='heston')
prices = pricer.price_options([48000, 50000, 52000], trading_days=30)
```

#### Customizing Configuration

Edit `config.py` to adjust parameters:

```python
# Example: Increase number of simulations
NUM_SIMULATIONS = 5000

# Example: Change rolling window
ROLLING_WINDOW = 30
```

## 📊 Methodology

### 1. Data Collection and Processing

- **Asset Data**: Historical Bitcoin prices from Yahoo Finance (2014-present)
- **Options Data**: Live options chain from Deribit exchange
- **Risk-Free Rate**: U.S. 3-month Treasury yield as proxy

### 2. Heston Model

The Heston model describes asset price evolution with stochastic volatility:

```
dS_t = μS_t dt + √V_t S_t dW^S_t
dV_t = κ(θ - V_t)dt + σ√V_t dW^V_t
```

Where:
- **S_t**: Asset price at time t
- **V_t**: Variance (volatility²) at time t
- **μ**: Drift rate (risk-free rate under risk-neutral measure)
- **κ (kappa)**: Mean reversion rate of volatility
- **θ (theta)**: Long-term average volatility
- **σ (sigma)**: Volatility of volatility
- **ρ (rho)**: Correlation between asset returns and volatility
- **W^S, W^V**: Correlated Brownian motions with correlation ρ

### 3. Parameter Estimation via MLE

Maximum Likelihood Estimation calibrates the Heston parameters (κ, θ, σ, ρ) by maximizing the likelihood function based on observed returns and volatilities. The implementation:

- Uses transformation to enforce parameter constraints
- Employs multiple random initial guesses
- Tests multiple optimization algorithms (L-BFGS-B, SLSQP, TNC)
- Selects the best result across all attempts

### 4. Option Pricing Methods

#### a) Heston Semi-Analytical Formula
Uses the characteristic function and numerical integration to compute option prices in semi-closed form.

#### b) Monte Carlo Simulation
Simulates multiple price paths using the Euler-Maruyama discretization scheme and computes expected payoffs.

#### c) Black-Scholes (Baseline)
Classical closed-form solution assuming constant volatility, used for comparison.

### 5. Performance Metrics

- **MAE** (Mean Absolute Error): Average absolute difference between model and market prices
- **RMSE** (Root Mean Square Error): Square root of average squared errors
- **MAPE** (Mean Absolute Percentage Error): Average percentage deviation

## 📈 Results

The project generates several outputs:

### Visualizations

1. **Monte Carlo Paths**: Shows all simulated price trajectories
2. **Sample Paths with Statistics**: Displays mean path and confidence intervals
3. **Option Pricing Comparison**: Compares model prices vs. market prices

### Data Files

1. **option_pricing_results.csv**: Detailed comparison table with strikes, prices, and errors
2. **heston_parameters.csv**: Estimated Heston parameters with descriptions

### Example Output

```
HESTON MODEL PARAMETER ESTIMATION RESULTS
==============================================================

Estimated Parameters:
  κ (kappa):  2.156432  - Mean reversion rate
  θ (theta):  0.024567  - Long-term volatility
  σ (sigma):  0.428391  - Volatility of volatility
  ρ (rho):    -0.312456  - Correlation coefficient

Pricing Error Summary:
Method               MAE          RMSE         MAPE (%)    
--------------------------------------------------------
Heston              $245.32      $312.45      3.45        
Monte Carlo         $289.67      $356.78      4.12        
Black-Scholes       $567.89      $689.12      8.23        
```

## 🔧 Module Descriptions

### `src/models/heston_model.py`
Core implementation of the Heston stochastic volatility model, including:
- Characteristic function computation
- Semi-analytical option pricing
- Monte Carlo simulation with full truncation scheme

### `src/models/option_pricer.py`
Option pricing functionality extending the Heston model:
- Multiple pricing methods (Heston, Monte Carlo, Black-Scholes)
- Batch pricing across multiple strikes
- Error analysis utilities

### `src/models/mle_optimizer.py`
Maximum Likelihood Estimation for parameter calibration:
- Parameter transformation for constraint handling
- Robust optimization with multiple initial guesses
- Log-likelihood computation

### `src/utils/data_fetcher.py`
Data acquisition and preprocessing:
- Yahoo Finance integration for historical prices
- Deribit API for options data
- Rolling volatility calculation
- Treasury yield fetching

### `src/utils/visualization.py`
Comprehensive visualization tools:
- Monte Carlo path plotting
- Option price comparison charts
- Error analysis plots
- Historical data visualization

## 🧪 Testing

To run unit tests (if implemented):

```bash
pytest tests/
```

## 📚 References

1. Heston, S. L. (1993). "A Closed-Form Solution for Options with Stochastic Volatility with Applications to Bond and Currency Options". *Review of Financial Studies*, 6(2), 327-343.

2. Gatheral, J. (2006). *The Volatility Surface: A Practitioner's Guide*. Wiley Finance.

3. Rouah, F. D. (2013). *The Heston Model and its Extensions in Matlab and C#*. Wiley.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Add put option pricing
- Implement American option pricing
- Add more calibration methods (e.g., using implied volatility surface)
- Implement variance reduction techniques for Monte Carlo
- Add unit tests
- Support for other cryptocurrencies

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

Created as a modular refactoring of a Jupyter notebook implementation of the Heston model for Bitcoin options pricing.

## 🙏 Acknowledgments

- Data sources: Yahoo Finance and Deribit
- Inspiration: Academic literature on stochastic volatility models
- Libraries: NumPy, SciPy, Pandas, Matplotlib, yfinance

## 📞 Contact

For questions or feedback, please open an issue on the project repository.

---

**Note**: This project is for educational and research purposes. Options trading involves significant risk. Always consult with financial professionals before making investment decisions.
