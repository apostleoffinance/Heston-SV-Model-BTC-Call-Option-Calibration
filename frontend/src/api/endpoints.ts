import axios from 'axios';
import type {
  MarketData,
  HistoricalData,
  CalibrationResult,
  SimulationRequest,
  SimulationResult,
  PricingRequest,
  PricingResult,
  ErrorAnalysis,
  OptionsChainItem,
} from '../types';

// Use environment variable for API URL, fallback to localhost for development
const API_BASE = import.meta.env.VITE_API_URL 
  ? `${import.meta.env.VITE_API_URL}/api`
  : '/api';

const api = axios.create({
  baseURL: API_BASE,
  timeout: 120000, // 2 minutes for long operations
});

export const endpoints = {
  // Health check
  health: async (): Promise<{ status: string }> => {
    const { data } = await api.get('/health');
    return data;
  },

  // Market data
  getMarketData: async (): Promise<MarketData> => {
    const { data } = await api.get('/market-data');
    return data;
  },

  // Historical data
  getHistoricalData: async (days: number = 365): Promise<HistoricalData> => {
    const { data } = await api.get(`/historical?days=${days}`);
    return data;
  },

  // Calibration
  calibrate: async (params: {
    start_date?: string;
    window?: number;
    n_guesses?: number;
  }): Promise<CalibrationResult> => {
    const { data } = await api.post('/calibrate', params);
    return data;
  },

  // Simulation
  simulate: async (params: SimulationRequest): Promise<SimulationResult> => {
    const { data } = await api.post('/simulate', params);
    return data;
  },

  // Options pricing
  priceOptions: async (params: PricingRequest): Promise<PricingResult> => {
    const { data } = await api.post('/price-options', params);
    return data;
  },

  // Options chain
  getOptionsChain: async (currency: string = 'BTC'): Promise<Record<string, OptionsChainItem[]>> => {
    const { data } = await api.get(`/options-chain?currency=${currency}`);
    return data;
  },

  // Expiry dates
  getExpiryDates: async (currency: string = 'BTC'): Promise<{ expiry_dates: string[] }> => {
    const { data } = await api.get(`/expiry-dates?currency=${currency}`);
    return data;
  },

  // Error analysis
  analyzeErrors: async (
    market_prices: number[],
    heston_prices: number[],
    mc_prices: number[],
    bs_prices: number[]
  ): Promise<ErrorAnalysis> => {
    const { data } = await api.post('/error-analysis', {
      market_prices,
      heston_prices,
      mc_prices,
      bs_prices,
    });
    return data;
  },

  // Export CSV
  exportCsv: async (): Promise<Blob> => {
    const response = await api.get('/export/csv', { responseType: 'blob' });
    return response.data;
  },
};

export default endpoints;
