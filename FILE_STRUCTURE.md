# Project File Structure

```
Heston_model_btc/
│
├── 📄 README.md                          # Main project documentation
├── 📄 QUICKSTART.md                      # Quick start guide for users
├── 📄 PROJECT_SUMMARY.md                 # Detailed project summary
├── 📄 DASHBOARD_README.md                # Dashboard documentation
├── 📄 LICENSE                            # MIT License
├── 📄 requirements.txt                   # Python dependencies (core)
├── 📄 config.py                          # Configuration parameters
├── 📄 .gitignore                         # Git ignore rules
├── 📄 start_dashboard.sh                 # Script to start full-stack app
│
├── 🐍 main.py                            # Main execution script (CLI)
├── 🐍 example.py                         # Quick example script
├── 🐍 demo.py                            # Demo with sample data
│
├── 📓 Heston_BTC (1).ipynb              # Original notebook (UNCHANGED)
│
├── 📁 src/                               # Core Python source code
│   ├── __init__.py                      # Package initialization
│   │
│   ├── 📁 models/                        # Core financial models
│   │   ├── __init__.py
│   │   ├── heston_model.py              # Heston stochastic volatility model
│   │   ├── option_pricer.py             # Option pricing implementations
│   │   └── mle_optimizer.py             # Maximum Likelihood Estimation
│   │
│   └── 📁 utils/                         # Utility modules
│       ├── __init__.py
│       ├── data_fetcher.py              # Data fetching and processing
│       └── visualization.py             # Plotting and visualization
│
├── 📁 backend/                           # FastAPI Backend Server
│   ├── 📄 requirements.txt              # Backend Python dependencies
│   ├── 📁 venv/                         # Backend virtual environment
│   └── 📁 app/
│       ├── __init__.py
│       └── main.py                      # FastAPI application with all endpoints
│
├── 📁 frontend/                          # React Frontend Dashboard
│   ├── 📄 package.json                  # Node.js dependencies
│   ├── 📄 vite.config.ts                # Vite configuration with proxy
│   ├── 📄 tailwind.config.js            # Tailwind CSS configuration
│   ├── 📄 tsconfig.json                 # TypeScript configuration
│   ├── 📄 index.html                    # HTML entry point
│   │
│   └── 📁 src/
│       ├── main.tsx                     # React entry point
│       ├── App.tsx                      # Main dashboard component
│       │
│       ├── 📁 api/
│       │   └── endpoints.ts             # Axios API client
│       │
│       ├── 📁 components/
│       │   ├── 📁 charts/               # Chart components
│       │   │   ├── MonteCarloChart.tsx  # MC simulation visualization
│       │   │   ├── PricingComparisonChart.tsx  # Options pricing chart
│       │   │   └── index.ts
│       │   │
│       │   ├── 📁 common/               # Reusable UI components
│       │   │   ├── Button.tsx
│       │   │   ├── Card.tsx
│       │   │   ├── Loader.tsx
│       │   │   └── index.ts
│       │   │
│       │   ├── 📁 config/               # Configuration components
│       │   │   └── ConfigPanel.tsx      # Analysis settings panel
│       │   │
│       │   ├── 📁 dashboard/            # Dashboard-specific components
│       │   │   ├── MarketDataCards.tsx  # BTC price & metrics cards
│       │   │   ├── ParametersPanel.tsx  # Heston parameters display
│       │   │   ├── ErrorAnalysis.tsx    # Pricing error metrics
│       │   │   ├── OptionsChainTable.tsx # Options data table
│       │   │   └── index.ts
│       │   │
│       │   └── 📁 layout/               # Layout components
│       │       └── Header.tsx
│       │
│       ├── 📁 hooks/
│       │   └── useApi.ts                # React Query hooks
│       │
│       ├── 📁 styles/
│       │   └── index.css                # Global styles (Tailwind)
│       │
│       └── 📁 types/
│           └── index.ts                 # TypeScript interfaces
│
├── 📁 outputs/                           # Generated outputs (created on run)
│   ├── .gitkeep
│   ├── mc_all_paths.png                 # (Generated) All MC paths
│   ├── mc_sample_paths.png              # (Generated) Sample paths
│   ├── option_prices_comparison.png     # (Generated) Price comparison
│   ├── option_pricing_results.csv       # (Generated) Detailed results
│   └── heston_parameters.csv            # (Generated) Estimated parameters
│
└── 📁 tests/                             # Unit tests (template)
    └── (Add your test files here)

```

## File Descriptions

### Root Level Files

| File | Purpose | When to Use |
|------|---------|-------------|
| `README.md` | Comprehensive documentation | Understanding the project |
| `QUICKSTART.md` | Getting started guide | First time setup |
| `PROJECT_SUMMARY.md` | Technical details | Deep dive into architecture |
| `DASHBOARD_README.md` | Web dashboard guide | Using the frontend |
| `main.py` | Full pipeline execution (CLI) | Running complete analysis |
| `example.py` | Simple demo | Learning the API |
| `demo.py` | Demo with sample data | Testing without internet |
| `config.py` | Settings and parameters | Customizing behavior |
| `start_dashboard.sh` | Start full-stack app | Running the web dashboard |
| `requirements.txt` | Core dependencies | Installation |
| `LICENSE` | Legal terms | Understanding usage rights |

### Backend (`backend/`)

| File | Purpose |
|------|---------|
| `app/main.py` | FastAPI application with REST API endpoints |
| `requirements.txt` | Backend-specific dependencies (FastAPI, uvicorn, etc.) |

#### Backend API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/market-data` | GET | Current BTC price, volatility, risk-free rate |
| `/api/historical` | GET | Historical price data |
| `/api/calibrate` | POST | Calibrate Heston parameters via MLE |
| `/api/simulate` | POST | Run Monte Carlo simulation |
| `/api/price-options` | POST | Price options using Heston, MC, BS |
| `/api/options-chain` | GET | Fetch live options from Deribit |
| `/api/expiry-dates` | GET | Available expiration dates |
| `/api/error-analysis` | POST | Calculate pricing errors |
| `/api/export/csv` | GET | Export results as CSV |

### Frontend (`frontend/`)

| Component | Purpose |
|-----------|---------|
| `App.tsx` | Main dashboard orchestrator |
| `MarketDataCards.tsx` | Display BTC price and market metrics |
| `ParametersPanel.tsx` | Show calibrated Heston parameters |
| `MonteCarloChart.tsx` | Interactive MC simulation chart |
| `PricingComparisonChart.tsx` | Compare Heston vs MC vs BS prices |
| `ErrorAnalysis.tsx` | Pricing accuracy metrics table |
| `OptionsChainTable.tsx` | Live options chain display |
| `endpoints.ts` | API client with Axios |

### Source Code (`src/`)

#### Models (`src/models/`)

| File | Classes | Purpose |
|------|---------|---------|
| `heston_model.py` | `HestonModel` | Core Heston SV model, characteristic function, MC simulation |
| `option_pricer.py` | `OptionPricer`, `OptionAnalyzer` | Multiple pricing methods, error analysis |
| `mle_optimizer.py` | `MLEOptimizer` | Parameter estimation via MLE |

#### Utilities (`src/utils/`)

| File | Classes | Purpose |
|------|---------|---------|
| `data_fetcher.py` | `DataFetcher` | Fetch BTC prices, options, treasury data |
| `visualization.py` | `SimulationVisualizer`, `OptionVisualizer`, `DataVisualizer` | All plotting functions |

## Module Dependencies

```
┌─────────────────────────────────────────────────────────────────┐
│                        WEB DASHBOARD                             │
├─────────────────────────────────────────────────────────────────┤
│  Frontend (React + TypeScript)                                   │
│  └── Vite dev server (port 5173)                                │
│      └── Proxy /api → Backend                                   │
│                                                                  │
│  Backend (FastAPI + Python)                                      │
│  └── Uvicorn server (port 8000)                                 │
│      └── Uses src/ modules                                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     CORE PYTHON MODULES                          │
├─────────────────────────────────────────────────────────────────┤
│  main.py / backend/app/main.py                                  │
│      │                                                           │
│      ├─→ DataFetcher (utils.data_fetcher)                       │
│      │   └─→ Uses: yfinance, requests, pandas                   │
│      │                                                           │
│      ├─→ MLEOptimizer (models.mle_optimizer)                    │
│      │   └─→ Uses: scipy.optimize, numpy                        │
│      │                                                           │
│      ├─→ HestonModel (models.heston_model)                      │
│      │   └─→ Uses: numpy, scipy.integrate                       │
│      │                                                           │
│      ├─→ OptionPricer (models.option_pricer)                    │
│      │   ├─→ Inherits: HestonModel                              │
│      │   └─→ Uses: scipy.stats                                  │
│      │                                                           │
│      └─→ Visualizers (utils.visualization)                      │
│          └─→ Uses: matplotlib, pandas                           │
└─────────────────────────────────────────────────────────────────┘
```

## Import Hierarchy

```
User Script (main.py or custom)
    ↓
src/__init__.py
    ↓
├─→ src/models/__init__.py
│   ├─→ heston_model.py
│   ├─→ option_pricer.py (imports heston_model)
│   └─→ mle_optimizer.py
│
└─→ src/utils/__init__.py
    ├─→ data_fetcher.py
    └─→ visualization.py
```

## Data Flow

```
1. DATA COLLECTION
   DataFetcher.fetch_asset_data()
        ↓
   Historical BTC prices
        ↓
   DataFetcher.calculate_rolling_volatility()
        ↓
   Prices + Volatility data
        ↓
   DataFetcher.prepare_data_for_mle()
        ↓
   Q (returns), V (volatility)

2. PARAMETER ESTIMATION
   MLEOptimizer(Q, V, r)
        ↓
   estimate_parameters_robust()
        ↓
   κ, θ, σ, ρ (Heston parameters)

3. SIMULATION
   HestonModel(S0, r, κ, θ, σ, ρ, v0)
        ↓
   heston_monte_carlo()
        ↓
   S (price paths), V (volatility paths)

4. PRICING
   OptionPricer(parameters)
        ↓
   price_options(strikes, days)
        ↓
   Model prices (Heston, MC, BS)

5. ANALYSIS
   OptionAnalyzer.calculate_pricing_error()
        ↓
   Error metrics (MAE, RMSE, MAPE)

6. VISUALIZATION
   SimulationVisualizer.plot_*()
   OptionVisualizer.plot_*()
        ↓
   PNG files in outputs/

7. RESULTS EXPORT
   pandas.DataFrame.to_csv()
        ↓
   CSV files in outputs/
```

## Size and Complexity

| Component | Lines of Code | Complexity |
|-----------|--------------|------------|
| `heston_model.py` | ~200 | High (Mathematical) |
| `option_pricer.py` | ~180 | Medium |
| `mle_optimizer.py` | ~200 | High (Optimization) |
| `data_fetcher.py` | ~190 | Low-Medium |
| `visualization.py` | ~300 | Low |
| `main.py` | ~200 | Low (Orchestration) |
| **Total** | **~1,270** | - |

## Key Design Patterns

1. **Class-Based Organization**: Each major component is a class
2. **Inheritance**: `OptionPricer` extends `HestonModel`
3. **Composition**: Classes use other classes' instances
4. **Factory Pattern**: Multiple pricer types from same interface
5. **Strategy Pattern**: Different pricing strategies selectable
6. **Separation of Concerns**: Data, models, visualization separated

## Configuration Flow

```
config.py
    ↓
Imported by main.py
    ↓
Parameters passed to:
    ├─→ DataFetcher (TICKER, WINDOW, etc.)
    ├─→ MLEOptimizer (N_GUESSES, etc.)
    ├─→ HestonModel (NUM_SIMULATIONS, etc.)
    └─→ Visualizers (FIGURE_DPI, etc.)
```

## Execution Order in main.py

```
1. Import modules
2. Fetch historical BTC data
3. Calculate rolling volatility
4. Fetch risk-free rate
5. Prepare MLE data (Q, V)
6. Run MLE optimization → Get parameters
7. Fetch options data
8. Create HestonModel with parameters
9. Run Monte Carlo simulation
10. Price options (Heston, MC, BS)
11. Calculate errors
12. Generate visualizations
13. Save results to outputs/
```

## Memory Usage Estimate

| Component | Typical Size |
|-----------|-------------|
| Historical data (10 years) | ~5 MB |
| Monte Carlo paths (1000 × 252) | ~2 MB |
| Options data | < 1 MB |
| Visualizations | ~3 MB |
| **Total Peak Usage** | **~50-100 MB** |

## File Sizes (Approximate)

```
Source Code:           ~50 KB
Documentation:         ~100 KB
Original Notebook:     ~500 KB
Generated Plots:       ~3 MB (3 × 1 MB each)
CSV Results:           ~50 KB
```

---

**Legend:**
- 📄 Documentation file
- 🐍 Python script
- 📁 Directory
- 📓 Jupyter Notebook
