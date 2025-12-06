// TypeScript interfaces for Heston Model Dashboard

export interface MarketData {
  btc_price: number;
  price_change_pct: number;
  risk_free_rate: number;
  risk_free_rate_annual_pct: number;
  current_volatility: number;
  data_points: number;
  last_updated: string;
}

export interface HistoricalData {
  dates: string[];
  prices: number[];
  returns: number[];
  rolling_volatility: number[];
}

export interface HestonParameters {
  kappa: number;
  theta: number;
  sigma: number;
  rho: number;
  v0: number;
}

export interface CalibrationResult extends HestonParameters {
  log_likelihood: number;
  optimization_method: string;
  status: string;
  observations: number;
}

export interface SimulationRequest {
  num_sims: number;
  trading_days: number;
  kappa: number;
  theta: number;
  sigma: number;
  rho: number;
  v0: number;
  S0: number;
  r: number;
  mu: number;
}

export interface SimulationResult {
  sample_paths: number[][];
  all_paths_summary: {
    mean: number[];
    percentile_5: number[];
    percentile_25: number[];
    percentile_75: number[];
    percentile_95: number[];
  };
  statistics: {
    mean_terminal: number;
    median_terminal: number;
    std_terminal: number;
    min_terminal: number;
    max_terminal: number;
    percentile_5: number;
    percentile_95: number;
  };
}

export interface PricingRequest {
  strikes: number[];
  trading_days: number;
  kappa: number;
  theta: number;
  sigma: number;
  rho: number;
  v0: number;
  S0: number;
  r: number;
}

export interface PricingResult {
  strikes: number[];
  heston_prices: number[];
  mc_prices: number[];
  bs_prices: number[];
  market_prices?: number[];
}

export interface ErrorMetrics {
  mae: number;
  rmse: number;
  mape: number;
}

export interface ErrorAnalysis {
  heston: ErrorMetrics;
  monte_carlo: ErrorMetrics;
  black_scholes: ErrorMetrics;
}

export interface OptionsChainItem {
  strike: number;
  expiry: string;
  days_to_expiry: number;
  market_price: number;
  heston_price?: number;
  mc_price?: number;
  bs_price?: number;
  implied_volatility?: number;
  is_itm: boolean;
}

export interface DashboardState {
  marketData: MarketData | null;
  calibration: CalibrationResult | null;
  simulation: SimulationResult | null;
  pricing: PricingResult | null;
  errors: ErrorAnalysis | null;
  optionsChain: Record<string, OptionsChainItem[]>;
  selectedExpiry: string | null;
  isLoading: boolean;
  currentStep: number;
}

export interface ConfigSettings {
  startDate: string;
  window: number;
  numSims: number;
  tradingDays: number;
  nGuesses: number;
}
