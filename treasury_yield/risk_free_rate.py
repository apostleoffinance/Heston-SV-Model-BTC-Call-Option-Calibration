import yfinance as yf

# Fetch 10-Year U.S. Treasury yield (risk-free rate)
treasury_data = yf.Ticker("^TNX")
risk_free_rate = treasury_data.history(period="1d")['Close'].iloc[-1] / 100  # Convert to decimal
print(f"Risk-Free Rate: {risk_free_rate:.4f}")