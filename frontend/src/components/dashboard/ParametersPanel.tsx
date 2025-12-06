import React from 'react';
import { Card } from '../common/Card';
import { Skeleton } from '../common/Loader';
import { CheckCircle, AlertCircle, RefreshCw } from 'lucide-react';
import type { CalibrationResult } from '../../types';

interface ParametersPanelProps {
  data: CalibrationResult | null;
  isLoading: boolean;
  onRecalibrate: () => void;
}

const ParameterCard: React.FC<{
  symbol: string;
  name: string;
  value: number;
  description: string;
}> = ({ symbol, name, value, description }) => (
  <div className="text-center p-4 bg-slate-50 dark:bg-slate-700/50 rounded-lg">
    <div className="text-lg font-mono text-primary-600 dark:text-primary-400">
      {symbol}
    </div>
    <div className="text-2xl font-bold font-mono-numbers text-slate-900 dark:text-white mt-1">
      {value.toFixed(4)}
    </div>
    <div className="text-xs text-slate-500 dark:text-slate-400 mt-1">
      {name}
    </div>
    <div className="text-xs text-slate-400 dark:text-slate-500 mt-0.5">
      {description}
    </div>
  </div>
);

export const ParametersPanel: React.FC<ParametersPanelProps> = ({
  data,
  isLoading,
  onRecalibrate,
}) => {
  if (isLoading) {
    return (
      <Card title="Heston Model Parameters">
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="text-center p-4 bg-slate-50 dark:bg-slate-700/50 rounded-lg">
              <Skeleton className="h-5 w-8 mx-auto mb-2" />
              <Skeleton className="h-8 w-20 mx-auto mb-2" />
              <Skeleton className="h-3 w-16 mx-auto" />
            </div>
          ))}
        </div>
      </Card>
    );
  }

  if (!data) {
    return (
      <Card title="Heston Model Parameters">
        <div className="text-center py-8 text-slate-500">
          Parameters not calibrated yet. Click "Run Analysis" to calibrate.
        </div>
      </Card>
    );
  }

  return (
    <Card
      title="Heston Model Parameters"
      action={
        <button
          onClick={onRecalibrate}
          className="flex items-center gap-1.5 text-sm text-primary-600 hover:text-primary-700 dark:text-primary-400"
        >
          <RefreshCw className="h-4 w-4" />
          Recalibrate
        </button>
      }
    >
      {/* Parameters Grid */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
        <ParameterCard
          symbol="κ"
          name="Kappa"
          value={data.kappa}
          description="Mean reversion"
        />
        <ParameterCard
          symbol="θ"
          name="Theta"
          value={data.theta}
          description="Long-term vol"
        />
        <ParameterCard
          symbol="σ"
          name="Sigma"
          value={data.sigma}
          description="Vol of vol"
        />
        <ParameterCard
          symbol="ρ"
          name="Rho"
          value={data.rho}
          description="Correlation"
        />
        <ParameterCard
          symbol="v₀"
          name="v0"
          value={data.v0}
          description="Initial vol"
        />
      </div>

      {/* Optimization Details */}
      <div className="flex flex-wrap items-center gap-4 pt-4 border-t border-slate-200 dark:border-slate-700 text-sm">
        <div className="flex items-center gap-2">
          <span className="text-slate-500">Log-Likelihood:</span>
          <span className="font-mono-numbers font-medium text-slate-900 dark:text-white">
            {data.log_likelihood.toFixed(2)}
          </span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-slate-500">Method:</span>
          <span className="font-medium text-slate-900 dark:text-white">
            {data.optimization_method}
          </span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-slate-500">Status:</span>
          {data.status.toLowerCase().includes('success') ? (
            <span className="flex items-center gap-1 text-emerald-600">
              <CheckCircle className="h-4 w-4" />
              Success
            </span>
          ) : (
            <span className="flex items-center gap-1 text-amber-600">
              <AlertCircle className="h-4 w-4" />
              {data.status}
            </span>
          )}
        </div>
        <div className="flex items-center gap-2">
          <span className="text-slate-500">Observations:</span>
          <span className="font-mono-numbers font-medium text-slate-900 dark:text-white">
            {data.observations.toLocaleString()}
          </span>
        </div>
      </div>
    </Card>
  );
};

export default ParametersPanel;
