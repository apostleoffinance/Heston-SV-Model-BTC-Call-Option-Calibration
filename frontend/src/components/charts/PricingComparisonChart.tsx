import React from 'react';
import Plot from 'react-plotly.js';
import { Card } from '../common/Card';
import { Loader } from '../common/Loader';
import type { PricingResult } from '../../types';

interface PricingComparisonChartProps {
  data: PricingResult | null;
  isLoading: boolean;
  darkMode: boolean;
  expiryDate: string;
}

export const PricingComparisonChart: React.FC<PricingComparisonChartProps> = ({
  data,
  isLoading,
  darkMode,
  expiryDate,
}) => {
  if (isLoading) {
    return (
      <Card title="Options Pricing Comparison">
        <div className="h-80 flex items-center justify-center">
          <Loader text="Pricing options..." />
        </div>
      </Card>
    );
  }

  if (!data) {
    return (
      <Card title="Options Pricing Comparison">
        <div className="h-80 flex items-center justify-center text-slate-500">
          No pricing data. Run analysis to price options.
        </div>
      </Card>
    );
  }

  const traces: Plotly.Data[] = [
    // Heston prices
    {
      x: data.strikes,
      y: data.heston_prices,
      type: 'scatter',
      mode: 'lines+markers',
      name: 'Heston',
      line: { color: '#3b82f6', width: 2 },
      marker: { size: 8, symbol: 'circle' },
    },
    // Monte Carlo prices
    {
      x: data.strikes,
      y: data.mc_prices,
      type: 'scatter',
      mode: 'lines+markers',
      name: 'Monte Carlo',
      line: { color: '#10b981', width: 2 },
      marker: { size: 8, symbol: 'triangle-up' },
    },
    // Black-Scholes prices
    {
      x: data.strikes,
      y: data.bs_prices,
      type: 'scatter',
      mode: 'lines+markers',
      name: 'Black-Scholes',
      line: { color: '#f59e0b', width: 2 },
      marker: { size: 8, symbol: 'square' },
    },
  ];

  // Add market prices if available
  if (data.market_prices && data.market_prices.length > 0) {
    traces.push({
      x: data.strikes,
      y: data.market_prices,
      type: 'scatter',
      mode: 'markers',
      name: 'Market',
      marker: {
        size: 12,
        symbol: 'diamond',
        color: '#ef4444',
        line: { color: '#fff', width: 1 },
      },
    });
  }

  const layout: Partial<Plotly.Layout> = {
    height: 350,
    margin: { t: 30, r: 30, b: 50, l: 70 },
    paper_bgcolor: 'transparent',
    plot_bgcolor: 'transparent',
    font: {
      family: 'Inter, system-ui, sans-serif',
      color: darkMode ? '#e2e8f0' : '#334155',
    },
    xaxis: {
      title: { text: 'Strike Price ($)' },
      gridcolor: darkMode ? 'rgba(148, 163, 184, 0.1)' : 'rgba(148, 163, 184, 0.2)',
      zerolinecolor: darkMode ? 'rgba(148, 163, 184, 0.2)' : 'rgba(148, 163, 184, 0.3)',
      tickformat: ',.0f',
      tickprefix: '$',
    },
    yaxis: {
      title: { text: 'Option Price ($)' },
      gridcolor: darkMode ? 'rgba(148, 163, 184, 0.1)' : 'rgba(148, 163, 184, 0.2)',
      zerolinecolor: darkMode ? 'rgba(148, 163, 184, 0.2)' : 'rgba(148, 163, 184, 0.3)',
      tickformat: ',.0f',
      tickprefix: '$',
    },
    legend: {
      x: 1,
      y: 1,
      xanchor: 'right',
      bgcolor: 'transparent',
    },
    hovermode: 'closest',
  };

  return (
    <Card
      title="Options Pricing Comparison"
      subtitle={`Expiry: ${expiryDate} | ${data.strikes.length} strikes`}
    >
      <Plot
        data={traces}
        layout={layout}
        config={{
          responsive: true,
          displayModeBar: false,
        }}
        style={{ width: '100%' }}
      />

      {/* Legend explanation */}
      <div className="flex flex-wrap items-center justify-center gap-6 mt-4 pt-4 border-t border-slate-200 dark:border-slate-700 text-sm">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-primary-500" />
          <span className="text-slate-600 dark:text-slate-300">Heston (Semi-analytical)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-emerald-500" />
          <span className="text-slate-600 dark:text-slate-300">Monte Carlo</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-amber-500" />
          <span className="text-slate-600 dark:text-slate-300">Black-Scholes</span>
        </div>
        {data.market_prices && data.market_prices.length > 0 && (
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-red-500" />
            <span className="text-slate-600 dark:text-slate-300">Market (Deribit)</span>
          </div>
        )}
      </div>
    </Card>
  );
};

export default PricingComparisonChart;
