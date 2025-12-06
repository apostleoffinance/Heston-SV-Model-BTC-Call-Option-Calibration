# Bitcoin Options Pricing with Heston Stochastic Volatility Model

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/React-18-61dafb.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A comprehensive implementation of the Heston stochastic volatility model for pricing Bitcoin options, featuring both a command-line interface and a full-stack web dashboard with real-time market data.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Web Dashboard](#web-dashboard)
- [API Reference](#api-reference)
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
5. **Web Dashboard**: Interactive React dashboard for real-time analysis and visualization
6. **Generates Analytics**: Creates comprehensive visualizations and performance metrics

## ✨ Features

- **Full-Stack Web Dashboard**: React + TypeScript frontend with FastAPI backend
- **Modular Architecture**: Clean, well-organized code structure with separate modules for different functionalities
- **Multiple Pricing Methods**: Compare Heston, Monte Carlo, and Black-Scholes approaches
- **Robust Parameter Estimation**: MLE optimization with multiple initial guesses and methods
- **Interactive Visualizations**: Real-time Plotly charts for simulation and pricing
- **Live Market Data**: Integrates with Yahoo Finance and Deribit API
- **Error Analysis**: Detailed pricing error metrics (MAE, RMSE, MAPE)
- **Configurable**: Centralized configuration for easy parameter adjustment

## 📁 Project Structure

```
Heston_model_btc/
│
├── README.md                          # This file
├── requirements.txt                   # Core Python dependencies
├── config.py                          # Configuration parameters
├── main.py                            # Main CLI execution script
├── start_dashboard.sh                 # Start full-stack dashboard
│
├── src/                               # Core Python modules
│   ├── models/                        # Core models
│   │   ├── heston_model.py           # Heston model implementation
│   │   ├── option_pricer.py          # Option pricing methods
│   │   └── mle_optimizer.py          # MLE parameter estimation
│   │
│   └── utils/                         # Utility modules
│       ├── data_fetcher.py           # Data fetching and processing
│       └── visualization.py          # Plotting and visualization
│
├── backend/                           # FastAPI Backend
│   ├── requirements.txt              # Backend dependencies
│   └── app/
│       └── main.py                   # FastAPI application
│
├── frontend/                          # React Frontend
│   ├── package.json                  # Node.js dependencies
│   ├── vite.config.ts                # Vite + proxy configuration
│   └── src/
│       ├── App.tsx                   # Main dashboard component
│       ├── api/endpoints.ts          # API client
│       ├── components/               # React components
│       │   ├── charts/               # Plotly chart components
│       │   ├── dashboard/            # Dashboard panels
│       │   └── common/               # Reusable UI components
│       └── types/                    # TypeScript interfaces
│
├── outputs/                           # Generated outputs (CLI)
│
└── Heston_BTC (1).ipynb              # Original Jupyter notebook (reference)
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Node.js 18+ and npm (for web dashboard)
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

3. **Install core Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **For Web Dashboard - Install backend dependencies**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   cd ..
   ```

5. **For Web Dashboard - Install frontend dependencies**:
   ```bash
   cd frontend
   npm install
   cd ..
   ```

## 💻 Usage

### Option 1: Web Dashboard (Recommended)

Start both backend and frontend servers:

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Then open **http://localhost:5173** in your browser.

### Option 2: Command Line Interface

Run the main script to execute the entire pipeline:

```bash
python main.py
```

This will:
1. Fetch historical Bitcoin data from Yahoo Finance
2. Estimate Heston parameters via MLE
3. Run Monte Carlo simulations
4. Price options using all methods
5. Generate visualizations and save results to `outputs/`

### Option 3: Quick Demo (No Internet Required)

```bash
python demo.py
```

## 🌐 Web Dashboard

The web dashboard provides an interactive interface for:

### Features

- **Real-Time Market Data**: Live BTC price, volatility, and risk-free rate
- **Parameter Calibration**: One-click MLE calibration with configurable settings
- **Monte Carlo Simulation**: Interactive chart with confidence bands
- **Options Pricing**: Compare Heston, Monte Carlo, and Black-Scholes prices
- **Error Analysis**: MAE, RMSE, MAPE metrics with method rankings
- **Live Options Chain**: Real options data from Deribit exchange

### Screenshots

The dashboard includes:
- Market data cards showing current BTC metrics
- Calibrated Heston parameters panel
- Interactive Monte Carlo simulation chart
- Options pricing comparison chart
- Error analysis table with rankings
- Live options chain table

## 📡 API Reference

### Backend Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/market-data` | GET | Current BTC price, volatility, risk-free rate |
| `/api/historical?days=365` | GET | Historical price data |
| `/api/calibrate` | POST | Calibrate Heston parameters via MLE |
| `/api/simulate` | POST | Run Monte Carlo simulation |
| `/api/price-options` | POST | Price options using all methods |
| `/api/options-chain?currency=BTC` | GET | Fetch live options from Deribit |
| `/api/expiry-dates?currency=BTC` | GET | Available expiration dates |
| `/api/error-analysis` | POST | Calculate pricing error metrics |
| `/api/export/csv` | GET | Export results as CSV |

### Example API Usage

```bash
# Health check
curl http://localhost:8000/api/health

# Get market data
curl http://localhost:8000/api/market-data

# Calibrate model
curl -X POST http://localhost:8000/api/calibrate \
  -H "Content-Type: application/json" \
  -d '{"start_date": "2020-01-01", "window": 21, "n_guesses": 5}'

# Price options
curl -X POST http://localhost:8000/api/price-options \
  -H "Content-Type: application/json" \
  -d '{
    "strikes": [85000, 90000, 95000, 100000],
    "trading_days": 30,
    "kappa": 0.5, "theta": 0.37, "sigma": 0.16, "rho": -0.31, "v0": 0.5,
    "S0": 90000, "r": 0.04
  }'
```

### Advanced Usage - Python API

```python
from src.utils.data_fetcher import DataFetcher
from src.models.heston_model import HestonModel
from src.models.option_pricer import OptionPricer
from src.models.mle_optimizer import MLEOptimizer
import numpy as np

# Fetch data
fetcher = DataFetcher(ticker='BTC-USD')
df = fetcher.fetch_asset_data(start_date='2020-01-01')
df = fetcher.calculate_rolling_volatility(df, window=21)

# Get risk-free rate
treasury = fetcher.fetch_treasury_data()
r = treasury['risk_free_rate']

# Calibrate parameters via MLE
returns = np.log(df['Close'] / df['Close'].shift(1)).dropna().values
volatility = df['rolling_vol'].dropna().values
min_len = min(len(returns), len(volatility))

optimizer = MLEOptimizer(returns[:min_len], volatility[:min_len], r)
params = optimizer.estimate_parameters_robust()

# Create Heston model and run simulation
model = HestonModel(
    S0=float(df['Close'].iloc[-1]), r=r,
    kappa=params['k'], theta=params['theta'],
    sigma=params['sigma'], rho=params['rho'], 
    v0=float(df['rolling_vol'].iloc[-1])
)
S, V = model.heston_monte_carlo(T=1, N=252, mu=0.05, num_sims=1000)

# Price options
pricer = OptionPricer(
    S0=model.S0, r=r,
    kappa=params['k'], theta=params['theta'],
    sigma=params['sigma'], rho=params['rho'], v0=model.v0,
    option_type='call', pricer='heston'
)
prices = pricer.price_options([85000, 90000, 95000, 100000], trading_days=30)
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
