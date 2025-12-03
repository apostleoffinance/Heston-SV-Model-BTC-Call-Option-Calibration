"""
Configuration File
==================
Central configuration for the Heston Model BTC Options Pricing project.
"""

# Asset Configuration
TICKER = 'BTC-USD'
START_DATE = '2014-01-01'
CURRENCY = 'BTC'

# Volatility Calculation Parameters
ROLLING_WINDOW = 21  # Days for rolling volatility calculation
TRADING_DAYS_PER_YEAR = 365  # For cryptocurrencies (24/7 trading)

# MLE Optimization Parameters
N_GUESSES = 20  # Number of random initial guesses for MLE optimization
MLE_MAX_ITER = 1000  # Maximum iterations for optimization
MLE_TOLERANCE = 1e-8  # Convergence tolerance

# Monte Carlo Simulation Parameters
NUM_SIMULATIONS = 1000  # Number of Monte Carlo paths
MC_TIME_STEPS = 252  # Number of time steps in simulation
MC_TIME_HORIZON = 1  # Time horizon in years

# Visualization Parameters
NUM_SAMPLE_PATHS = 10  # Number of sample paths to plot
FIGURE_DPI = 300  # DPI for saved figures
FIGURE_SIZE_WIDE = (12, 6)  # Wide figure size
FIGURE_SIZE_TALL = (10, 8)  # Tall figure size

# Output Configuration
OUTPUT_DIR = 'outputs'  # Directory for saving results
SAVE_FIGURES = True  # Whether to save figures
SAVE_RESULTS = True  # Whether to save CSV results

# API Configuration
DERIBIT_API_URL = "https://www.deribit.com/api/v2/public/get_book_summary_by_currency"
TREASURY_TICKERS = ['^IRX', '^FVX', '^TNX', '^TYX']  # 3M, 5Y, 10Y, 30Y

# Parameter Constraints for MLE
PARAM_CONSTRAINTS = {
    'kappa': {'min': 0.5, 'max': 5.0},     # Mean reversion rate
    'theta': {'min': 0.0, 'max': 1.0},     # Long-term volatility
    'sigma': {'min': 0.0, 'max': 5.0},     # Volatility of volatility
    'rho': {'min': -1.0, 'max': 0.0}       # Correlation (typically negative)
}

# Display Settings
PRINT_PROGRESS = True  # Whether to print progress messages
VERBOSE = True  # Detailed output
