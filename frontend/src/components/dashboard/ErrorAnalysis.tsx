import React from 'react';
import { Card } from '../common/Card';
import { Skeleton } from '../common/Loader';
import clsx from 'clsx';
import type { ErrorAnalysis as ErrorAnalysisType } from '../../types';

interface ErrorAnalysisProps {
  data: ErrorAnalysisType | null;
  isLoading: boolean;
}

const ErrorBar: React.FC<{
  value: number;
  maxValue: number;
  color: string;
}> = ({ value, maxValue, color }) => {
  const percentage = Math.min((value / maxValue) * 100, 100);
  return (
    <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2.5">
      <div
        className={clsx('h-2.5 rounded-full', color)}
        style={{ width: `${percentage}%` }}
      />
    </div>
  );
};

export const ErrorAnalysis: React.FC<ErrorAnalysisProps> = ({
  data,
  isLoading,
}) => {
  if (isLoading) {
    return (
      <Card title="Error Analysis">
        <div className="space-y-4">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="flex items-center gap-4">
              <Skeleton className="h-6 w-24" />
              <Skeleton className="h-6 flex-1" />
              <Skeleton className="h-6 w-20" />
            </div>
          ))}
        </div>
      </Card>
    );
  }

  if (!data) {
    return (
      <Card title="Error Analysis">
        <div className="text-center py-8 text-slate-500">
          No error analysis available. Run pricing first.
        </div>
      </Card>
    );
  }

  const methods = [
    { name: 'Heston', data: data.heston, color: 'bg-primary-500' },
    { name: 'Monte Carlo', data: data.monte_carlo, color: 'bg-emerald-500' },
    { name: 'Black-Scholes', data: data.black_scholes, color: 'bg-amber-500' },
  ].filter(m => m.data); // Filter out any undefined data

  if (methods.length === 0) {
    return (
      <Card title="Error Analysis">
        <div className="text-center py-8 text-slate-500">
          No error analysis data available.
        </div>
      </Card>
    );
  }

  // Find best method (lowest MAPE)
  const bestMethod = methods.reduce((best, current) =>
    current.data.mape < best.data.mape ? current : best
  );

  // Calculate max values for scaling bars
  const maxMape = Math.max(...methods.map((m) => m.data.mape));

  return (
    <Card title="Error Analysis" subtitle="Pricing accuracy comparison">
      {/* Summary Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-200 dark:border-slate-700">
              <th className="text-left py-3 px-4 font-medium text-slate-500 dark:text-slate-400">
                Method
              </th>
              <th className="text-right py-3 px-4 font-medium text-slate-500 dark:text-slate-400">
                MAE ($)
              </th>
              <th className="text-right py-3 px-4 font-medium text-slate-500 dark:text-slate-400">
                RMSE ($)
              </th>
              <th className="text-right py-3 px-4 font-medium text-slate-500 dark:text-slate-400">
                MAPE (%)
              </th>
              <th className="text-center py-3 px-4 font-medium text-slate-500 dark:text-slate-400">
                Rank
              </th>
            </tr>
          </thead>
          <tbody>
            {methods.map((method, index) => {
              const isBest = method.name === bestMethod.name;
              return (
                <tr
                  key={method.name}
                  className={clsx(
                    'border-b border-slate-100 dark:border-slate-800',
                    isBest && 'bg-emerald-50 dark:bg-emerald-900/20'
                  )}
                >
                  <td className="py-3 px-4">
                    <div className="flex items-center gap-2">
                      <div className={clsx('w-3 h-3 rounded-full', method.color)} />
                      <span className="font-medium text-slate-900 dark:text-white">
                        {method.name}
                      </span>
                      {isBest && (
                        <span className="text-xs bg-emerald-100 dark:bg-emerald-800 text-emerald-700 dark:text-emerald-300 px-2 py-0.5 rounded-full">
                          Best
                        </span>
                      )}
                    </div>
                  </td>
                  <td className="py-3 px-4 text-right font-mono-numbers text-slate-900 dark:text-white">
                    ${method.data.mae.toLocaleString(undefined, { maximumFractionDigits: 2 })}
                  </td>
                  <td className="py-3 px-4 text-right font-mono-numbers text-slate-900 dark:text-white">
                    ${method.data.rmse.toLocaleString(undefined, { maximumFractionDigits: 2 })}
                  </td>
                  <td className="py-3 px-4 text-right font-mono-numbers text-slate-900 dark:text-white">
                    {method.data.mape.toFixed(2)}%
                  </td>
                  <td className="py-3 px-4 text-center">
                    <span
                      className={clsx(
                        'inline-flex items-center justify-center w-6 h-6 rounded-full text-xs font-bold',
                        index === 0 && 'bg-amber-100 text-amber-700',
                        index === 1 && 'bg-slate-200 text-slate-600',
                        index === 2 && 'bg-orange-100 text-orange-700'
                      )}
                    >
                      {[...methods].sort((a, b) => a.data.mape - b.data.mape).indexOf(method) + 1}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Visual Bars */}
      <div className="mt-6 space-y-4">
        <h4 className="text-sm font-medium text-slate-500 dark:text-slate-400">
          MAPE Comparison
        </h4>
        {methods.map((method) => (
          <div key={method.name} className="flex items-center gap-3">
            <span className="w-24 text-sm text-slate-600 dark:text-slate-300">
              {method.name}
            </span>
            <div className="flex-1">
              <ErrorBar value={method.data.mape} maxValue={maxMape} color={method.color} />
            </div>
            <span className="w-16 text-right text-sm font-mono-numbers text-slate-600 dark:text-slate-300">
              {method.data.mape.toFixed(1)}%
            </span>
          </div>
        ))}
      </div>
    </Card>
  );
};

export default ErrorAnalysis;
