import React from 'react';
import { Bitcoin, Percent, Activity, Database } from 'lucide-react';
import { MetricCard } from '../common/Card';
import { CardSkeleton } from '../common/Loader';
import type { MarketData } from '../../types';

interface MarketDataCardsProps {
  data: MarketData | null;
  isLoading: boolean;
}

export const MarketDataCards: React.FC<MarketDataCardsProps> = ({
  data,
  isLoading,
}) => {
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {[...Array(4)].map((_, i) => (
          <CardSkeleton key={i} />
        ))}
      </div>
    );
  }

  if (!data) {
    return (
      <div className="text-center py-8 text-slate-500">
        No market data available. Click "Run Analysis" to fetch data.
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <MetricCard
        label="BTC Price"
        value={`$${data.btc_price.toLocaleString(undefined, {
          minimumFractionDigits: 2,
          maximumFractionDigits: 2,
        })}`}
        change={data.price_change_pct}
        icon={<Bitcoin className="h-5 w-5" />}
        color="blue"
      />
      <MetricCard
        label="Risk-Free Rate"
        value={`${data.risk_free_rate_annual_pct.toFixed(2)}%`}
        icon={<Percent className="h-5 w-5" />}
        color="green"
      />
      <MetricCard
        label="Current Volatility"
        value={`${(data.current_volatility * 100).toFixed(2)}%`}
        icon={<Activity className="h-5 w-5" />}
        color="amber"
      />
      <MetricCard
        label="Data Points"
        value={data.data_points.toLocaleString()}
        icon={<Database className="h-5 w-5" />}
        color="blue"
      />
    </div>
  );
};

export default MarketDataCards;
