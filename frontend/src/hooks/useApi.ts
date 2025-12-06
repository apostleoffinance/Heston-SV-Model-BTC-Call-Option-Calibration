import { useQuery, useMutation } from '@tanstack/react-query';
import endpoints from '../api/endpoints';
import type { SimulationRequest, PricingRequest } from '../types';

// Market Data Hook
export const useMarketData = () => {
  return useQuery({
    queryKey: ['marketData'],
    queryFn: endpoints.getMarketData,
    staleTime: 60000, // 1 minute
    retry: 2,
  });
};

// Historical Data Hook
export const useHistoricalData = (days: number = 365) => {
  return useQuery({
    queryKey: ['historicalData', days],
    queryFn: () => endpoints.getHistoricalData(days),
    staleTime: 300000, // 5 minutes
  });
};

// Calibration Hook
export const useCalibration = () => {
  return useMutation({
    mutationFn: (params: { start_date?: string; window?: number; n_guesses?: number }) =>
      endpoints.calibrate(params),
  });
};

// Simulation Hook
export const useSimulation = () => {
  return useMutation({
    mutationFn: (params: SimulationRequest) => endpoints.simulate(params),
  });
};

// Options Pricing Hook
export const useOptionsPricing = () => {
  return useMutation({
    mutationFn: (params: PricingRequest) => endpoints.priceOptions(params),
  });
};

// Options Chain Hook
export const useOptionsChain = (currency: string = 'BTC') => {
  return useQuery({
    queryKey: ['optionsChain', currency],
    queryFn: () => endpoints.getOptionsChain(currency),
    staleTime: 60000,
  });
};

// Expiry Dates Hook
export const useExpiryDates = (currency: string = 'BTC') => {
  return useQuery({
    queryKey: ['expiryDates', currency],
    queryFn: () => endpoints.getExpiryDates(currency),
    staleTime: 60000,
  });
};

// Error Analysis Hook
export const useErrorAnalysis = () => {
  return useMutation({
    mutationFn: ({
      market_prices,
      heston_prices,
      mc_prices,
      bs_prices,
    }: {
      market_prices: number[];
      heston_prices: number[];
      mc_prices: number[];
      bs_prices: number[];
    }) => endpoints.analyzeErrors(market_prices, heston_prices, mc_prices, bs_prices),
  });
};
