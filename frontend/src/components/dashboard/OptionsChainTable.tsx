import React, { useState, useMemo } from 'react';
import { Card } from '../common/Card';
import { Button } from '../common/Button';
import { Skeleton } from '../common/Loader';
import { Download, ChevronUp, ChevronDown, Search } from 'lucide-react';
import clsx from 'clsx';
import type { OptionsChainItem } from '../../types';

interface OptionsChainTableProps {
  data: OptionsChainItem[];
  isLoading: boolean;
  onExport: () => void;
}

type SortField = 'strike' | 'market_price' | 'heston_price' | 'mc_price' | 'bs_price';
type SortDirection = 'asc' | 'desc';

export const OptionsChainTable: React.FC<OptionsChainTableProps> = ({
  data,
  isLoading,
  onExport,
}) => {
  const [sortField, setSortField] = useState<SortField>('strike');
  const [sortDirection, setSortDirection] = useState<SortDirection>('asc');
  const [filter, setFilter] = useState<'all' | 'itm' | 'otm'>('all');
  const [searchTerm, setSearchTerm] = useState('');

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('asc');
    }
  };

  const filteredAndSortedData = useMemo(() => {
    let result = [...data];

    // Filter by ITM/OTM
    if (filter === 'itm') {
      result = result.filter((item) => item.is_itm);
    } else if (filter === 'otm') {
      result = result.filter((item) => !item.is_itm);
    }

    // Search by strike
    if (searchTerm) {
      result = result.filter((item) =>
        item.strike.toString().includes(searchTerm)
      );
    }

    // Sort
    result.sort((a, b) => {
      const aVal = a[sortField] ?? 0;
      const bVal = b[sortField] ?? 0;
      return sortDirection === 'asc' ? (aVal as number) - (bVal as number) : (bVal as number) - (aVal as number);
    });

    return result;
  }, [data, filter, searchTerm, sortField, sortDirection]);

  const SortHeader: React.FC<{ field: SortField; label: string }> = ({
    field,
    label,
  }) => (
    <th
      className="text-right py-3 px-4 font-medium text-slate-500 dark:text-slate-400 cursor-pointer hover:text-slate-700 dark:hover:text-slate-300"
      onClick={() => handleSort(field)}
    >
      <div className="flex items-center justify-end gap-1">
        {label}
        {sortField === field && (
          sortDirection === 'asc' ? (
            <ChevronUp className="h-4 w-4" />
          ) : (
            <ChevronDown className="h-4 w-4" />
          )
        )}
      </div>
    </th>
  );

  if (isLoading) {
    return (
      <Card title="Options Chain">
        <div className="space-y-3">
          {[...Array(5)].map((_, i) => (
            <Skeleton key={i} className="h-12 w-full" />
          ))}
        </div>
      </Card>
    );
  }

  if (!data || data.length === 0) {
    return (
      <Card title="Options Chain">
        <div className="text-center py-8 text-slate-500">
          No options data available.
        </div>
      </Card>
    );
  }

  return (
    <Card
      title="Options Chain"
      subtitle={`${filteredAndSortedData.length} options`}
      action={
        <Button
          variant="outline"
          size="sm"
          onClick={onExport}
          icon={<Download className="h-4 w-4" />}
        >
          Export CSV
        </Button>
      }
    >
      {/* Filters */}
      <div className="flex flex-wrap items-center gap-4 mb-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
          <input
            type="text"
            placeholder="Search strike..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-9 pr-4 py-2 text-sm border border-slate-200 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
        </div>
        <div className="flex items-center gap-2">
          {(['all', 'itm', 'otm'] as const).map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={clsx(
                'px-3 py-1.5 text-sm rounded-lg transition-colors',
                filter === f
                  ? 'bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300'
                  : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
              )}
            >
              {f === 'all' ? 'All' : f === 'itm' ? 'ITM' : 'OTM'}
            </button>
          ))}
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-200 dark:border-slate-700">
              <SortHeader field="strike" label="Strike" />
              <th className="text-right py-3 px-4 font-medium text-slate-500 dark:text-slate-400">
                Expiry
              </th>
              <th className="text-right py-3 px-4 font-medium text-slate-500 dark:text-slate-400">
                Days
              </th>
              <SortHeader field="market_price" label="Market" />
              <SortHeader field="heston_price" label="Heston" />
              <SortHeader field="mc_price" label="MC" />
              <SortHeader field="bs_price" label="BS" />
              <th className="text-right py-3 px-4 font-medium text-slate-500 dark:text-slate-400">
                IV
              </th>
              <th className="text-center py-3 px-4 font-medium text-slate-500 dark:text-slate-400">
                Status
              </th>
            </tr>
          </thead>
          <tbody>
            {filteredAndSortedData.map((item, index) => (
              <tr
                key={`${item.strike}-${index}`}
                className={clsx(
                  'border-b border-slate-100 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800/50',
                  item.is_itm && 'bg-emerald-50/50 dark:bg-emerald-900/10'
                )}
              >
                <td className="py-3 px-4 text-right font-mono-numbers font-medium text-slate-900 dark:text-white">
                  ${item.strike.toLocaleString()}
                </td>
                <td className="py-3 px-4 text-right text-slate-600 dark:text-slate-300">
                  {item.expiry}
                </td>
                <td className="py-3 px-4 text-right font-mono-numbers text-slate-600 dark:text-slate-300">
                  {item.days_to_expiry}
                </td>
                <td className="py-3 px-4 text-right font-mono-numbers text-slate-900 dark:text-white">
                  ${item.market_price.toLocaleString(undefined, { maximumFractionDigits: 2 })}
                </td>
                <td className="py-3 px-4 text-right font-mono-numbers text-primary-600 dark:text-primary-400">
                  {item.heston_price
                    ? `$${item.heston_price.toLocaleString(undefined, { maximumFractionDigits: 2 })}`
                    : '-'}
                </td>
                <td className="py-3 px-4 text-right font-mono-numbers text-emerald-600 dark:text-emerald-400">
                  {item.mc_price
                    ? `$${item.mc_price.toLocaleString(undefined, { maximumFractionDigits: 2 })}`
                    : '-'}
                </td>
                <td className="py-3 px-4 text-right font-mono-numbers text-amber-600 dark:text-amber-400">
                  {item.bs_price
                    ? `$${item.bs_price.toLocaleString(undefined, { maximumFractionDigits: 2 })}`
                    : '-'}
                </td>
                <td className="py-3 px-4 text-right font-mono-numbers text-slate-600 dark:text-slate-300">
                  {item.implied_volatility
                    ? `${(item.implied_volatility * 100).toFixed(1)}%`
                    : '-'}
                </td>
                <td className="py-3 px-4 text-center">
                  <span
                    className={clsx(
                      'text-xs px-2 py-0.5 rounded-full font-medium',
                      item.is_itm
                        ? 'bg-emerald-100 dark:bg-emerald-800 text-emerald-700 dark:text-emerald-300'
                        : 'bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300'
                    )}
                  >
                    {item.is_itm ? 'ITM' : 'OTM'}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
};

export default OptionsChainTable;
