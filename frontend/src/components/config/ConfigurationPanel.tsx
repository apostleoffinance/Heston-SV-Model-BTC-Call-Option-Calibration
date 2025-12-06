import React from 'react';
import { Card } from '../common/Card';
import { Button } from '../common/Button';
import { Play } from 'lucide-react';
import type { ConfigSettings } from '../../types';

interface ConfigurationPanelProps {
  config: ConfigSettings;
  onConfigChange: (config: ConfigSettings) => void;
  onRunAnalysis: () => void;
  isRunning: boolean;
  currentStep: number;
  expiryDates: string[];
  selectedExpiry: string;
  onExpiryChange: (expiry: string) => void;
}

const steps = [
  'Fetching market data',
  'Calibrating parameters',
  'Running simulation',
  'Pricing options',
  'Analyzing errors',
];

export const ConfigurationPanel: React.FC<ConfigurationPanelProps> = ({
  config,
  onConfigChange,
  onRunAnalysis,
  isRunning,
  currentStep,
  expiryDates,
  selectedExpiry,
  onExpiryChange,
}) => {
  return (
    <Card
      title="Configuration"
      action={
        <Button
          variant="primary"
          onClick={onRunAnalysis}
          loading={isRunning}
          icon={<Play className="h-4 w-4" />}
        >
          {isRunning ? `Step ${currentStep}/5` : 'Run Analysis'}
        </Button>
      }
    >
      <div className="space-y-4">
        {/* Progress indicator when running */}
        {isRunning && (
          <div className="mb-4 p-3 bg-primary-50 dark:bg-primary-900/20 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <div className="animate-spin h-4 w-4 border-2 border-primary-500 border-t-transparent rounded-full" />
              <span className="text-sm font-medium text-primary-700 dark:text-primary-300">
                {steps[currentStep - 1] || 'Processing...'}
              </span>
            </div>
            <div className="w-full bg-primary-200 dark:bg-primary-800 rounded-full h-1.5">
              <div
                className="bg-primary-600 h-1.5 rounded-full transition-all duration-300"
                style={{ width: `${(currentStep / 5) * 100}%` }}
              />
            </div>
          </div>
        )}

        {/* Configuration inputs */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Start Date */}
          <div>
            <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
              Start Date
            </label>
            <input
              type="date"
              value={config.startDate}
              onChange={(e) =>
                onConfigChange({ ...config, startDate: e.target.value })
              }
              className="w-full px-3 py-2 text-sm border border-slate-200 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              disabled={isRunning}
            />
          </div>

          {/* Rolling Window */}
          <div>
            <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
              Rolling Window (days)
            </label>
            <input
              type="number"
              value={config.window}
              onChange={(e) =>
                onConfigChange({ ...config, window: parseInt(e.target.value) || 21 })
              }
              min={5}
              max={60}
              className="w-full px-3 py-2 text-sm border border-slate-200 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              disabled={isRunning}
            />
          </div>

          {/* Number of Simulations */}
          <div>
            <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
              Simulations: {config.numSims.toLocaleString()}
            </label>
            <input
              type="range"
              value={config.numSims}
              onChange={(e) =>
                onConfigChange({ ...config, numSims: parseInt(e.target.value) })
              }
              min={100}
              max={5000}
              step={100}
              className="w-full h-2 bg-slate-200 dark:bg-slate-700 rounded-lg appearance-none cursor-pointer accent-primary-600"
              disabled={isRunning}
            />
          </div>

          {/* Expiry Date */}
          <div>
            <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
              Option Expiry
            </label>
            <select
              value={selectedExpiry}
              onChange={(e) => onExpiryChange(e.target.value)}
              className="w-full px-3 py-2 text-sm border border-slate-200 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              disabled={isRunning || expiryDates.length === 0}
            >
              {expiryDates.length === 0 ? (
                <option>Run analysis first</option>
              ) : (
                expiryDates.map((date) => (
                  <option key={date} value={date}>
                    {date}
                  </option>
                ))
              )}
            </select>
          </div>
        </div>
      </div>
    </Card>
  );
};

export default ConfigurationPanel;
