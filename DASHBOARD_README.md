# Heston Model BTC Options Dashboard

A full-stack web application for pricing Bitcoin options using the Heston Stochastic Volatility Model.

## 🚀 Quick Start

### Option 1: Run everything with one command
```bash
chmod +x start_dashboard.sh
./start_dashboard.sh
```

### Option 2: Run backend and frontend separately

**Terminal 1 - Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Then open http://localhost:5173 in your browser.

## 📁 Project Structure

```
Heston_model_btc/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py            # API endpoints
│   └── requirements.txt
│
├── frontend/                   # React Frontend
│   ├── src/
│   │   ├── api/               # API client
│   │   ├── components/        # React components
│   │   │   ├── charts/        # Plotly visualizations
│   │   │   ├── common/        # Reusable UI components
│   │   │   ├── config/        # Configuration panel
│   │   │   ├── dashboard/     # Dashboard sections
│   │   │   └── layout/        # Header, Footer
│   │   ├── hooks/             # React Query hooks
│   │   ├── styles/            # Tailwind CSS
│   │   ├── types/             # TypeScript interfaces
│   │   ├── App.tsx            # Main component
│   │   └── main.tsx           # Entry point
│   ├── index.html
│   ├── package.json
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   └── vite.config.ts
│
├── src/                        # Core Python modules
│   ├── models/
│   │   ├── heston_model.py
│   │   ├── mle_optimizer.py
│   │   └── option_pricer.py
│   └── utils/
│       ├── data_fetcher.py
│       └── visualization.py
│
└── start_dashboard.sh          # One-click startup script
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/market-data` | GET | Current BTC price & rates |
| `/api/historical` | GET | Historical price data |
| `/api/calibrate` | POST | MLE parameter estimation |
| `/api/simulate` | POST | Monte Carlo simulation |
| `/api/price-options` | POST | Price options (all methods) |
| `/api/options-chain` | GET | Deribit options data |
| `/api/expiry-dates` | GET | Available expiries |
| `/api/error-analysis` | POST | Calculate pricing errors |
| `/api/export/csv` | GET | Download results as CSV |

## 🎨 Features

### Dashboard Components

1. **Market Data Cards** - Live BTC price, risk-free rate, volatility
2. **Heston Parameters** - Calibrated κ, θ, σ, ρ, v₀ with optimization stats
3. **Monte Carlo Chart** - Simulated price paths with confidence bands
4. **Pricing Comparison** - Interactive chart comparing all pricing methods
5. **Error Analysis** - MAE, RMSE, MAPE metrics with visual comparison
6. **Options Chain** - Sortable/filterable table with all pricing data

### Configuration Options

- Historical start date
- Rolling volatility window
- Number of simulations (100-5000)
- Option expiry selection

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **NumPy/SciPy** - Numerical computations
- **yfinance** - Market data

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Plotly.js** - Interactive charts
- **React Query** - Data fetching
- **Vite** - Build tool

## 📊 Screenshots

The dashboard displays:
- Real-time BTC price with change indicator
- Calibrated Heston model parameters
- Monte Carlo simulation fan chart
- Option pricing comparison scatter plot
- Error analysis with bar charts
- Complete options chain table

## 🔧 Development

### Backend Development
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API documentation available at http://localhost:8000/docs

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

Hot reload enabled at http://localhost:5173

### Build for Production
```bash
cd frontend
npm run build
```

## 📝 Notes

- The frontend proxies API requests to `localhost:8000`
- First run will install dependencies automatically
- Calibration may take 1-2 minutes depending on data size
- Yahoo Finance API may have rate limits

## 🐛 Troubleshooting

**Backend won't start:**
```bash
pip install fastapi uvicorn pydantic
```

**Frontend dependencies error:**
```bash
cd frontend && rm -rf node_modules && npm install
```

**API timeout:**
- Reduce `n_guesses` in calibration
- Reduce `num_sims` in simulation

## 📄 License

MIT License - See LICENSE file
