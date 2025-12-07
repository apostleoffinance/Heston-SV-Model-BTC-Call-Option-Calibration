import React, { useState, useEffect, useCallback } from 'react';
import { Header, Footer } from './components/layout';
import { MarketDataCards, ParametersPanel, ErrorAnalysis, OptionsChainTable } from './components/dashboard';
import { MonteCarloChart, PricingComparisonChart } from './components/charts';
import { ConfigurationPanel } from './components/config';
import endpoints from './api/endpoints';
import type {
  MarketData,
  CalibrationResult,
  SimulationResult,
  PricingResult,
  ErrorAnalysis as ErrorAnalysisType,
  OptionsChainItem,
  ConfigSettings,
} from './types';

const App: React.FC = () => {
  // Theme state
  const [darkMode, setDarkMode] = useState(() => {
    if (typeof window !== 'undefined') {
      return window.matchMedia('(prefers-color-scheme: dark)').matches;
    }
    return false;
  });

  // Configuration state
  const [config, setConfig] = useState<ConfigSettings>({
    startDate: '2023-01-01',
    window: 21,
    numSims: 1000,
    tradingDays: 252,
    nGuesses: 5,
  });

  // Data state
  const [marketData, setMarketData] = useState<MarketData | null>(null);
  const [calibration, setCalibration] = useState<CalibrationResult | null>(null);
  const [simulation, setSimulation] = useState<SimulationResult | null>(null);
  const [pricing, setPricing] = useState<PricingResult | null>(null);
  const [errorAnalysis, setErrorAnalysis] = useState<ErrorAnalysisType | null>(null);
  const [optionsChain, setOptionsChain] = useState<Record<string, OptionsChainItem[]>>({});
  const [expiryDates, setExpiryDates] = useState<string[]>([]);
  const [selectedExpiry, setSelectedExpiry] = useState<string>('');

  // Loading states
  const [isRunning, setIsRunning] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [loadingMarket, setLoadingMarket] = useState(false);
  const [loadingCalibration, setLoadingCalibration] = useState(false);
  const [loadingSimulation, setLoadingSimulation] = useState(false);
  const [loadingPricing, setLoadingPricing] = useState(false);

  // Apply dark mode class
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  // Run complete analysis pipeline
  const runAnalysis = useCallback(async () => {
    setIsRunning(true);
    setCurrentStep(1);

    try {
      // Step 1: Fetch market data
      setLoadingMarket(true);
      const market = await endpoints.getMarketData();
      setMarketData(market);
      setLoadingMarket(false);
      setCurrentStep(2);

      // Step 2: Calibrate parameters
      setLoadingCalibration(true);
      const params = await endpoints.calibrate({
        start_date: config.startDate,
        window: config.window,
        n_guesses: config.nGuesses,
      });
      setCalibration(params);
      setLoadingCalibration(false);
      setCurrentStep(3);

      // Step 3: Run simulation
      setLoadingSimulation(true);
      const sim = await endpoints.simulate({
        num_sims: config.numSims,
        trading_days: config.tradingDays,
        kappa: params.kappa,
        theta: params.theta,
        sigma: params.sigma,
        rho: params.rho,
        v0: params.v0,
        S0: market.btc_price,
        r: market.risk_free_rate,
        mu: 0.05,
      });
      setSimulation(sim);
      setLoadingSimulation(false);
      setCurrentStep(4);

      // Step 4: Fetch options chain and price
      const chain = await endpoints.getOptionsChain('BTC');
      setOptionsChain(chain);
      const dates = Object.keys(chain).sort();
      setExpiryDates(dates);

      if (dates.length > 0) {
        // Find a good expiry (not too close)
        const goodExpiry = dates.find((d) => {
          const expDate = new Date(d);
          const now = new Date();
          const daysToExpiry = Math.floor((expDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
          return daysToExpiry >= 7;
        }) || dates[0];

        setSelectedExpiry(goodExpiry);

        // Get strikes for selected expiry
        const expOptions = chain[goodExpiry];
        if (expOptions && expOptions.length > 0) {
          const strikes = expOptions.map((o) => o.strike);
          const tradingDays = expOptions[0]?.days_to_expiry || 30;

          setLoadingPricing(true);
          const priceResult = await endpoints.priceOptions({
            strikes,
            trading_days: tradingDays,
            kappa: params.kappa,
            theta: params.theta,
            sigma: params.sigma,
            rho: params.rho,
            v0: params.v0,
            S0: market.btc_price,
            r: market.risk_free_rate,
          });

          // Add market prices to result
          priceResult.market_prices = expOptions.map((o) => o.market_price);
          setPricing(priceResult);
          setLoadingPricing(false);

          // Step 5: Error analysis
          setCurrentStep(5);
          if (priceResult.market_prices && priceResult.market_prices.length > 0) {
            const errors = await endpoints.analyzeErrors(
              priceResult.market_prices,
              priceResult.heston_prices,
              priceResult.mc_prices,
              priceResult.bs_prices
            );
            setErrorAnalysis(errors);
          }
        }
      }
    } catch (error) {
      console.error('Analysis error:', error);
      alert('An error occurred during analysis. Check console for details.');
    } finally {
      setIsRunning(false);
      setCurrentStep(0);
      setLoadingMarket(false);
      setLoadingCalibration(false);
      setLoadingSimulation(false);
      setLoadingPricing(false);
    }
  }, [config]);

  // Handle expiry change - re-price options
  const handleExpiryChange = useCallback(
    async (expiry: string) => {
      setSelectedExpiry(expiry);

      if (!calibration || !marketData || !optionsChain[expiry]) return;

      const expOptions = optionsChain[expiry];
      const strikes = expOptions.map((o) => o.strike);
      const tradingDays = expOptions[0]?.days_to_expiry || 30;

      setLoadingPricing(true);
      try {
        const priceResult = await endpoints.priceOptions({
          strikes,
          trading_days: tradingDays,
          kappa: calibration.kappa,
          theta: calibration.theta,
          sigma: calibration.sigma,
          rho: calibration.rho,
          v0: calibration.v0,
          S0: marketData.btc_price,
          r: marketData.risk_free_rate,
        });

        priceResult.market_prices = expOptions.map((o) => o.market_price);
        setPricing(priceResult);

        // Update error analysis
        if (priceResult.market_prices && priceResult.market_prices.length > 0) {
          const errors = await endpoints.analyzeErrors(
            priceResult.market_prices,
            priceResult.heston_prices,
            priceResult.mc_prices,
            priceResult.bs_prices
          );
          setErrorAnalysis(errors);
        }
      } catch (error) {
        console.error('Pricing error:', error);
      } finally {
        setLoadingPricing(false);
      }
    },
    [calibration, marketData, optionsChain]
  );

  // Export handler
  const handleExport = useCallback(async () => {
    try {
      const blob = await endpoints.exportCsv();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'options_pricing_results.csv';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Export error:', error);
      alert('Export failed. Run analysis first.');
    }
  }, []);

  // Build options chain items with pricing
  const optionsChainItems: OptionsChainItem[] = React.useMemo(() => {
    if (!selectedExpiry || !optionsChain[selectedExpiry]) return [];

    return optionsChain[selectedExpiry].map((opt, i) => ({
      ...opt,
      heston_price: pricing?.heston_prices[i],
      mc_price: pricing?.mc_prices[i],
      bs_price: pricing?.bs_prices[i],
    }));
  }, [selectedExpiry, optionsChain, pricing]);

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 transition-colors">
      <Header
        darkMode={darkMode}
        toggleDarkMode={() => setDarkMode(!darkMode)}
        onExport={handleExport}
      />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
        {/* Configuration */}
        <ConfigurationPanel
          config={config}
          onConfigChange={setConfig}
          onRunAnalysis={runAnalysis}
          isRunning={isRunning}
          currentStep={currentStep}
          expiryDates={expiryDates}
          selectedExpiry={selectedExpiry}
          onExpiryChange={handleExpiryChange}
        />

        {/* Market Data Cards */}
        <MarketDataCards data={marketData} isLoading={loadingMarket} />

        {/* Parameters Panel */}
        <ParametersPanel
          data={calibration}
          isLoading={loadingCalibration}
          onRecalibrate={runAnalysis}
        />

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <MonteCarloChart
            data={simulation}
            isLoading={loadingSimulation}
            S0={marketData?.btc_price || 90000}
            darkMode={darkMode}
          />
          <PricingComparisonChart
            data={pricing}
            isLoading={loadingPricing}
            darkMode={darkMode}
            expiryDate={selectedExpiry}
          />
        </div>

        {/* Error Analysis */}
        <ErrorAnalysis data={errorAnalysis} isLoading={loadingPricing} />

        {/* Options Chain Table */}
        <OptionsChainTable
          data={optionsChainItems}
          isLoading={loadingPricing}
          onExport={handleExport}
        />
      </main>

      <Footer />
    </div>
  );
};

export default App;
