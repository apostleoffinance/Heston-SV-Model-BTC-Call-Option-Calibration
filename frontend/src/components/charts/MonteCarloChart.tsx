import React from 'react';
import Plot from 'react-plotly.js';
import { Card } from '../common/Card';
import { Loader } from '../common/Loader';
import type { SimulationResult } from '../../types';

interface MonteCarloChartProps {
  data: SimulationResult | null;
  isLoading: boolean;
  S0: number;
  darkMode: boolean;
}

export const MonteCarloChart: React.FC<MonteCarloChartProps> = ({
  data,
  isLoading,
  S0,
  darkMode,
}) => {
  if (isLoading) {
    return (
      <Card title="Monte Carlo Simulation">
        <div className="h-80 flex items-center justify-center">
          <Loader text="Running simulation..." />
        </div>
      </Card>
    );
  }

  if (!data) {
    return (
      <Card title="Monte Carlo Simulation">
        <div className="h-80 flex items-center justify-center text-slate-500">
          No simulation data. Run analysis to generate paths.
        </div>
      </Card>
    );
  }

  const xValues = Array.from({ length: data.all_paths_summary.mean.length }, (_, i) => i);

  // Create traces for the plot
  const traces: Plotly.Data[] = [];

  // Add confidence band (5-95 percentile)
  traces.push({
    x: [...xValues, ...xValues.slice().reverse()],
    y: [
      ...data.all_paths_summary.percentile_95,
      ...data.all_paths_summary.percentile_5.slice().reverse(),
    ],
    fill: 'toself',
    fillcolor: darkMode ? 'rgba(59, 130, 246, 0.1)' : 'rgba(59, 130, 246, 0.15)',
    line: { color: 'transparent' },
    name: '5%-95% Band',
    showlegend: true,
    hoverinfo: 'skip',
  });

  // Add 25-75 percentile band
  traces.push({
    x: [...xValues, ...xValues.slice().reverse()],
    y: [
      ...data.all_paths_summary.percentile_75,
      ...data.all_paths_summary.percentile_25.slice().reverse(),
    ],
    fill: 'toself',
    fillcolor: darkMode ? 'rgba(59, 130, 246, 0.2)' : 'rgba(59, 130, 246, 0.25)',
    line: { color: 'transparent' },
    name: '25%-75% Band',
    showlegend: true,
    hoverinfo: 'skip',
  });

  // Add sample paths
  data.sample_paths.forEach((path, i) => {
    traces.push({
      x: xValues,
      y: path,
      type: 'scatter',
      mode: 'lines',
      line: {
        color: darkMode ? 'rgba(148, 163, 184, 0.3)' : 'rgba(100, 116, 139, 0.3)',
        width: 1,
      },
      name: `Path ${i + 1}`,
      showlegend: false,
      hoverinfo: 'y',
    });
  });

  // Add mean path
  traces.push({
    x: xValues,
    y: data.all_paths_summary.mean,
    type: 'scatter',
    mode: 'lines',
    line: {
      color: '#3b82f6',
      width: 3,
    },
    name: 'Mean Path',
    showlegend: true,
  });

  // Add starting price line
  traces.push({
    x: xValues,
    y: Array(xValues.length).fill(S0),
    type: 'scatter',
    mode: 'lines',
    line: {
      color: darkMode ? '#f59e0b' : '#d97706',
      width: 2,
      dash: 'dash',
    },
    name: `S₀ = $${S0.toLocaleString()}`,
    showlegend: true,
  });

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
      title: { text: 'Trading Days' },
      gridcolor: darkMode ? 'rgba(148, 163, 184, 0.1)' : 'rgba(148, 163, 184, 0.2)',
      zerolinecolor: darkMode ? 'rgba(148, 163, 184, 0.2)' : 'rgba(148, 163, 184, 0.3)',
    },
    yaxis: {
      title: { text: 'BTC Price ($)' },
      gridcolor: darkMode ? 'rgba(148, 163, 184, 0.1)' : 'rgba(148, 163, 184, 0.2)',
      zerolinecolor: darkMode ? 'rgba(148, 163, 184, 0.2)' : 'rgba(148, 163, 184, 0.3)',
      tickformat: ',.0f',
      tickprefix: '$',
    },
    legend: {
      x: 0,
      y: 1,
      bgcolor: 'transparent',
    },
    hovermode: 'x unified',
  };

  return (
    <Card
      title="Monte Carlo Simulation"
      subtitle={`${data.sample_paths.length * 100} paths simulated`}
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

      {/* Statistics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4 pt-4 border-t border-slate-200 dark:border-slate-700">
        <div className="text-center">
          <p className="text-xs text-slate-500 dark:text-slate-400">Mean Terminal</p>
          <p className="text-lg font-mono-numbers font-semibold text-slate-900 dark:text-white">
            ${data.statistics.mean_terminal.toLocaleString(undefined, { maximumFractionDigits: 0 })}
          </p>
        </div>
        <div className="text-center">
          <p className="text-xs text-slate-500 dark:text-slate-400">Std Dev</p>
          <p className="text-lg font-mono-numbers font-semibold text-slate-900 dark:text-white">
            ${data.statistics.std_terminal.toLocaleString(undefined, { maximumFractionDigits: 0 })}
          </p>
        </div>
        <div className="text-center">
          <p className="text-xs text-slate-500 dark:text-slate-400">5th Percentile</p>
          <p className="text-lg font-mono-numbers font-semibold text-red-600">
            ${data.statistics.percentile_5.toLocaleString(undefined, { maximumFractionDigits: 0 })}
          </p>
        </div>
        <div className="text-center">
          <p className="text-xs text-slate-500 dark:text-slate-400">95th Percentile</p>
          <p className="text-lg font-mono-numbers font-semibold text-emerald-600">
            ${data.statistics.percentile_95.toLocaleString(undefined, { maximumFractionDigits: 0 })}
          </p>
        </div>
      </div>
    </Card>
  );
};

export default MonteCarloChart;
