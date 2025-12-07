"""
FastAPI Backend for Heston Model BTC Options Pricing Dashboard
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import sys
import os
import io
import csv
import numpy as np
import pandas as pd

# Add parent directories to path for imports (works both locally and on Railway)
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(backend_dir)
sys.path.insert(0, project_root)
sys.path.insert(0, backend_dir)

from src.models.heston_model import HestonModel
from src.models.option_pricer import OptionPricer, OptionAnalyzer
from src.models.mle_optimizer import MLEOptimizer
from src.utils.data_fetcher import DataFetcher

app = FastAPI(
    title="Heston Model BTC Options API",
    description="API for Bitcoin options pricing using the Heston stochastic volatility model",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174", 
        "http://localhost:5175",
        "http://localhost:3000",
        "https://heston-sv-model-btc-call-option-cal.vercel.app",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize data fetcher
data_fetcher = DataFetcher()

# Cache for expensive computations
cache = {
    "market_data": None,
    "calibration": None,
    "options_data": None,
    "simulation": None
}


# ============== Pydantic Models ==============

class MarketDataResponse(BaseModel):
    btc_price: float
    price_change_pct: float
    risk_free_rate: float
    risk_free_rate_annual_pct: float
    current_volatility: float
    data_points: int
    last_updated: str


class HistoricalDataResponse(BaseModel):
    dates: List[str]
    prices: List[float]
    returns: List[float]
    rolling_volatility: List[float]


class CalibrationRequest(BaseModel):
    start_date: str = "2014-01-01"
    window: int = 21
    n_guesses: int = 5


class CalibrationResponse(BaseModel):
    kappa: float
    theta: float
    sigma: float
    rho: float
    v0: float
    log_likelihood: float
    optimization_method: str
    status: str
    observations: int


class SimulationRequest(BaseModel):
    num_sims: int = Field(default=1000, ge=100, le=10000)
    trading_days: int = Field(default=252, ge=30, le=504)
    kappa: float
    theta: float
    sigma: float
    rho: float
    v0: float
    S0: float
    r: float
    mu: float = 0.05


class SimulationResponse(BaseModel):
    sample_paths: List[List[float]]  # 10 representative paths
    all_paths_summary: Dict[str, List[float]]  # mean, percentile bands
    statistics: Dict[str, float]


class PricingRequest(BaseModel):
    strikes: List[float]
    trading_days: int = 365
    kappa: float
    theta: float
    sigma: float
    rho: float
    v0: float
    S0: float
    r: float
    T: Optional[float] = None  # Time to expiry (alternative to trading_days)
    n_simulations: int = 10000


class PricingResponse(BaseModel):
    strikes: List[float]
    heston_prices: List[float]
    mc_prices: List[float]
    bs_prices: List[float]
    market_prices: Optional[List[float]] = None


class ErrorMetrics(BaseModel):
    mae: float
    rmse: float
    mape: float


class ErrorAnalysisResponse(BaseModel):
    heston: ErrorMetrics
    monte_carlo: ErrorMetrics
    black_scholes: ErrorMetrics


class OptionsChainItem(BaseModel):
    strike: float
    expiry: str
    days_to_expiry: int
    market_price: float
    heston_price: Optional[float] = None
    mc_price: Optional[float] = None
    bs_price: Optional[float] = None
    implied_volatility: Optional[float] = None
    is_itm: bool


class OptionsChainResponse(BaseModel):
    expiry_date: str
    options: List[OptionsChainItem]


# ============== API Endpoints ==============

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Heston Model API"}


@app.get("/api/market-data", response_model=MarketDataResponse)
async def get_market_data():
    """Get current market data including BTC price and risk-free rate"""
    try:
        # Fetch BTC data
        df = data_fetcher.fetch_asset_data(start_date="2014-01-01")
        
        if df is None or df.empty:
            raise HTTPException(status_code=500, detail="Failed to fetch BTC data")
        
        # Calculate rolling volatility
        df = data_fetcher.calculate_rolling_volatility(df, window=21)
        
        # Fetch risk-free rate
        treasury_data = data_fetcher.fetch_treasury_data()
        r = treasury_data['risk_free_rate']
        r_annual = treasury_data['3M_yield'] / 100  # Convert percentage to decimal
        
        # Calculate price change
        if len(df) >= 2:
            price_change = ((df['Close'].iloc[-1] - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100
        else:
            price_change = 0.0
        
        # Cache the data
        cache["market_data"] = df
        
        return MarketDataResponse(
            btc_price=float(df['Close'].iloc[-1]),
            price_change_pct=float(price_change),
            risk_free_rate=float(r),
            risk_free_rate_annual_pct=float(r_annual * 100),
            current_volatility=float(df['rolling_vol'].iloc[-1]) if 'rolling_vol' in df.columns else 0.0,
            data_points=len(df),
            last_updated=str(df.index[-1])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/historical", response_model=HistoricalDataResponse)
async def get_historical_data(days: int = 365):
    """Get historical price data"""
    try:
        df = cache.get("market_data")
        if df is None:
            df = data_fetcher.fetch_asset_data(start_date="2014-01-01")
            df = data_fetcher.calculate_rolling_volatility(df, window=21)
            # Calculate log returns
            df['returns'] = np.log(df['Close'] / df['Close'].shift(1))
            cache["market_data"] = df
        
        # Get last N days
        df_subset = df.tail(days)
        
        return HistoricalDataResponse(
            dates=[str(d) for d in df_subset.index],
            prices=df_subset['Close'].tolist(),
            returns=df_subset['returns'].fillna(0).tolist() if 'returns' in df_subset.columns else [],
            rolling_volatility=df_subset['rolling_vol'].fillna(0).tolist() if 'rolling_vol' in df_subset.columns else []
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/calibrate", response_model=CalibrationResponse)
async def calibrate_model(request: CalibrationRequest):
    """Calibrate Heston model parameters using MLE"""
    try:
        # Fetch and prepare data
        df = cache.get("market_data")
        if df is None:
            df = data_fetcher.fetch_asset_data(start_date=request.start_date)
            df = data_fetcher.calculate_rolling_volatility(df, window=request.window)
            # Calculate log returns
            df['returns'] = np.log(df['Close'] / df['Close'].shift(1))
            cache["market_data"] = df
        
        # Ensure returns column exists
        if 'returns' not in df.columns:
            df['returns'] = np.log(df['Close'] / df['Close'].shift(1))
            cache["market_data"] = df
        
        # Prepare data for MLE
        returns = df['returns'].dropna().values
        volatility = df['rolling_vol'].dropna().values
        
        # Align arrays
        min_len = min(len(returns), len(volatility))
        returns = returns[:min_len]
        volatility = volatility[:min_len]
        
        # Get risk-free rate
        treasury_data = data_fetcher.fetch_treasury_data()
        r = treasury_data['risk_free_rate']
        
        # Run MLE optimization
        optimizer = MLEOptimizer(returns, volatility, r, n_guesses=request.n_guesses)
        results = optimizer.estimate_parameters_robust()
        
        # Get v0 (most recent volatility)
        v0 = float(df['rolling_vol'].iloc[-1])
        
        # Cache results
        cache["calibration"] = {
            "kappa": results['k'],
            "theta": results['theta'],
            "sigma": results['sigma'],
            "rho": results['rho'],
            "v0": v0,
            "log_likelihood": results['log_likelihood']
        }
        
        return CalibrationResponse(
            kappa=float(results['k']),
            theta=float(results['theta']),
            sigma=float(results['sigma']),
            rho=float(results['rho']),
            v0=v0,
            log_likelihood=float(results['log_likelihood']),
            optimization_method=results.get('method', 'SLSQP'),
            status=results.get('message', 'Success'),
            observations=len(returns)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/simulate", response_model=SimulationResponse)
async def run_simulation(request: SimulationRequest):
    """Run Monte Carlo simulation"""
    try:
        import numpy as np
        
        # Create Heston model
        model = HestonModel(
            S0=request.S0,
            r=request.r,
            kappa=request.kappa,
            theta=request.theta,
            sigma=request.sigma,
            rho=request.rho,
            v0=request.v0
        )
        
        # Run simulation
        S, V = model.heston_monte_carlo(
            T=request.trading_days / 252,
            N=request.trading_days,
            mu=request.mu,
            num_sims=request.num_sims
        )
        
        # Get 10 sample paths
        sample_indices = np.linspace(0, request.num_sims - 1, 10, dtype=int)
        sample_paths = [S[i].tolist() for i in sample_indices]
        
        # Calculate summary statistics
        mean_path = np.mean(S, axis=0).tolist()
        percentile_5 = np.percentile(S, 5, axis=0).tolist()
        percentile_25 = np.percentile(S, 25, axis=0).tolist()
        percentile_75 = np.percentile(S, 75, axis=0).tolist()
        percentile_95 = np.percentile(S, 95, axis=0).tolist()
        
        # Terminal statistics
        terminal_prices = S[:, -1]
        
        # Cache simulation results
        cache["simulation"] = {"S": S, "V": V}
        
        return SimulationResponse(
            sample_paths=sample_paths,
            all_paths_summary={
                "mean": mean_path,
                "percentile_5": percentile_5,
                "percentile_25": percentile_25,
                "percentile_75": percentile_75,
                "percentile_95": percentile_95
            },
            statistics={
                "mean_terminal": float(np.mean(terminal_prices)),
                "median_terminal": float(np.median(terminal_prices)),
                "std_terminal": float(np.std(terminal_prices)),
                "min_terminal": float(np.min(terminal_prices)),
                "max_terminal": float(np.max(terminal_prices)),
                "percentile_5": float(np.percentile(terminal_prices, 5)),
                "percentile_95": float(np.percentile(terminal_prices, 95))
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/price-options", response_model=PricingResponse)
async def price_options(request: PricingRequest):
    """Price options using all three methods"""
    try:
        # Create option pricer instances
        heston_pricer = OptionPricer(
            S0=request.S0, r=request.r,
            kappa=request.kappa, theta=request.theta,
            sigma=request.sigma, rho=request.rho, v0=request.v0,
            option_type='call', pricer='heston'
        )
        
        mc_pricer = OptionPricer(
            S0=request.S0, r=request.r,
            kappa=request.kappa, theta=request.theta,
            sigma=request.sigma, rho=request.rho, v0=request.v0,
            option_type='call', pricer='monte_carlo'
        )
        
        bs_pricer = OptionPricer(
            S0=request.S0, r=request.r,
            kappa=request.kappa, theta=request.theta,
            sigma=request.sigma, rho=request.rho, v0=request.v0,
            option_type='call', pricer='black_scholes'
        )
        
        # Price using Heston
        heston_prices = heston_pricer.price_options(request.strikes, request.trading_days)
        
        # Price using Monte Carlo
        simulation = cache.get("simulation")
        if simulation is not None:
            S = simulation["S"]
            mc_prices = mc_pricer.price_options(request.strikes, request.trading_days, S=S)
        else:
            # Run a quick simulation if none cached
            model = HestonModel(
                S0=request.S0, r=request.r,
                kappa=request.kappa, theta=request.theta,
                sigma=request.sigma, rho=request.rho, v0=request.v0
            )
            S, V = model.heston_monte_carlo(T=request.trading_days/252, N=request.trading_days, mu=0.05, num_sims=500)
            mc_prices = mc_pricer.price_options(request.strikes, request.trading_days, S=S)
        
        # Price using Black-Scholes
        bs_prices = bs_pricer.price_options(request.strikes, request.trading_days)
        
        return PricingResponse(
            strikes=request.strikes,
            heston_prices=heston_prices,
            mc_prices=mc_prices,
            bs_prices=bs_prices
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/options-chain")
async def get_options_chain(currency: str = "BTC"):
    """Fetch options chain from Deribit"""
    try:
        options_df = data_fetcher.fetch_options_data(currency)
        
        if options_df is None or options_df.empty:
            raise HTTPException(status_code=500, detail="Failed to fetch options data")
        
        # Cache options data
        cache["options_data"] = options_df
        
        # Get current BTC price
        df = cache.get("market_data")
        if df is not None:
            S0 = float(df['Close'].iloc[-1])
        else:
            S0 = 90000  # fallback
        
        # Group by expiry (using strike_dates column from data_fetcher)
        expiry_col = 'strike_dates' if 'strike_dates' in options_df.columns else 'expiry_date'
        expiry_groups = options_df.groupby(expiry_col)
        
        result = {}
        for expiry, group in expiry_groups:
            options_list = []
            for _, row in group.iterrows():
                # Calculate days to expiry
                try:
                    expiry_date = pd.to_datetime(expiry)
                    days_to_expiry = (expiry_date - pd.Timestamp.now()).days
                    if days_to_expiry < 1:
                        days_to_expiry = 1  # At least 1 day for same-day expiry
                except:
                    days_to_expiry = 30  # fallback
                
                # Market price from Deribit is in BTC, convert to USD
                market_price_btc = float(row['lastPrice']) if 'lastPrice' in row and pd.notna(row['lastPrice']) else 0.0
                market_price_usd = market_price_btc * S0
                
                options_list.append({
                    "strike": float(row['strike']),
                    "expiry": str(expiry),
                    "days_to_expiry": max(1, days_to_expiry),
                    "market_price": market_price_usd,
                    "implied_volatility": float(row['impliedVolatility']) if 'impliedVolatility' in row and pd.notna(row['impliedVolatility']) else None,
                    "is_itm": float(row['strike']) < S0
                })
            result[str(expiry)] = options_list
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/expiry-dates")
async def get_expiry_dates(currency: str = "BTC"):
    """Get available expiration dates"""
    try:
        options_df = cache.get("options_data")
        if options_df is None:
            options_df = data_fetcher.fetch_options_data(currency)
            cache["options_data"] = options_df
        
        if options_df is None or options_df.empty:
            return {"expiry_dates": []}
        
        # Use strike_dates column from data_fetcher
        expiry_col = 'strike_dates' if 'strike_dates' in options_df.columns else 'expiry_date'
        expiry_dates = sorted(options_df[expiry_col].unique().tolist())
        return {"expiry_dates": [str(d) for d in expiry_dates]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class ErrorAnalysisRequest(BaseModel):
    market_prices: List[float]
    heston_prices: List[float]
    mc_prices: List[float]
    bs_prices: List[float]


@app.post("/api/error-analysis", response_model=ErrorAnalysisResponse)
async def analyze_errors(request: ErrorAnalysisRequest):
    """Calculate error metrics for all pricing methods"""
    try:
        market = np.array(request.market_prices)
        heston = np.array(request.heston_prices)
        mc = np.array(request.mc_prices)
        bs = np.array(request.bs_prices)
        
        def calculate_metrics(pred, actual):
            mae = np.mean(np.abs(pred - actual))
            rmse = np.sqrt(np.mean((pred - actual) ** 2))
            # Avoid division by zero
            non_zero = actual != 0
            if np.any(non_zero):
                mape = np.mean(np.abs((pred[non_zero] - actual[non_zero]) / actual[non_zero])) * 100
            else:
                mape = 0.0
            return {"mae": float(mae), "rmse": float(rmse), "mape": float(mape)}
        
        return ErrorAnalysisResponse(
            heston=ErrorMetrics(**calculate_metrics(heston, market)),
            monte_carlo=ErrorMetrics(**calculate_metrics(mc, market)),
            black_scholes=ErrorMetrics(**calculate_metrics(bs, market))
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/export/csv")
async def export_csv():
    """Export pricing results as CSV"""
    try:
        options_data = cache.get("options_data")
        calibration = cache.get("calibration")
        
        if options_data is None:
            raise HTTPException(status_code=400, detail="No data to export. Run analysis first.")
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            "Strike", "Expiry", "Days to Expiry", "Market Price",
            "Heston Price", "MC Price", "BS Price", "Implied Vol"
        ])
        
        # Write data
        for _, row in options_data.iterrows():
            writer.writerow([
                row.get('strike', ''),
                row.get('expiry_date', ''),
                row.get('trading_days', ''),
                row.get('mark_price', ''),
                row.get('heston_price', ''),
                row.get('mc_price', ''),
                row.get('bs_price', ''),
                row.get('mark_iv', '')
            ])
        
        output.seek(0)
        
        return StreamingResponse(
            io.BytesIO(output.getvalue().encode()),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=options_pricing_results.csv"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
