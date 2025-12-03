# Troubleshooting Guide

## Common Issues and Solutions

### 1. Yahoo Finance API Errors

**Error:**
```
Failed download: ['BTC-USD']: JSONDecodeError('Expecting value: line 1 column 1 (char 0)')
Exception: Failed to fetch data after 3 attempts: No data returned
```

**Cause:** Yahoo Finance API is temporarily unavailable or rate-limiting requests.

**Solution:**
1. Use the demo script instead: `python demo.py`
2. Wait 10-15 minutes and try `main.py` again
3. Check your internet connection
4. Verify you can access https://finance.yahoo.com in your browser

### 2. Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'X'
```

**Solution:**
```bash
pip install -r requirements.txt
```

### 3. Pandas Not Defined

**Error:**
```
NameError: name 'pd' is not defined
```

**Solution:** This has been fixed in the current version. Update your files or reinstall.

### 4. Matplotlib Display Issues

**Error:**
Window hangs or shows blank matplotlib windows

**Solution:** The project now uses non-interactive backend (`Agg`). Plots are saved to `outputs/` directory automatically.

### 5. Permission Errors

**Error:**
```
PermissionError: [Errno 13] Permission denied: 'outputs/'
```

**Solution:**
```bash
mkdir outputs
chmod 755 outputs
```

### 6. Memory Errors

**Error:**
```
MemoryError: Unable to allocate array
```

**Solution:** Reduce simulation parameters in `config.py`:
```python
NUM_SIMULATIONS = 500  # Instead of 1000
MC_TIME_STEPS = 126    # Instead of 252
```

### 7. MLE Optimization Fails

**Error:**
```
ValueError: Optimization failed for all attempts
```

**Solution:** Increase the number of initial guesses in `config.py`:
```python
N_GUESSES = 30  # Instead of 20
```

### 8. Deribit API Connection Issues

**Error:**
```
ConnectionError or timeout when fetching options data
```

**Solution:**
1. Check internet connection
2. Verify Deribit API is accessible: https://www.deribit.com/api/v2/public/test
3. Use demo script for offline testing

### 9. Slow Performance

**Issue:** Script takes too long to run

**Solution:**
Adjust these parameters in `config.py`:
```python
NUM_SIMULATIONS = 500      # Reduce from 1000
N_GUESSES = 10            # Reduce from 20
MC_TIME_STEPS = 126       # Reduce from 252
```

### 10. NaN Pricing Results

**Issue:** Option prices show as NaN

**Cause:** Usually occurs with:
- Options expiring same day (< 1 trading day remaining)
- Extreme parameter values
- Numerical integration issues

**Solution:**
1. Select options with at least 7 days to expiry (code now handles this)
2. Check parameter values are reasonable
3. Use demo script to verify code works with sample parameters

## Getting Help

If you encounter an issue not listed here:

1. **Check the documentation:**
   - README.md for general info
   - QUICKSTART.md for setup
   - INDEX.md for navigation

2. **Verify installation:**
   ```bash
   python -c "import numpy, scipy, pandas, matplotlib, yfinance; print('All imports OK')"
   ```

3. **Test with demo:**
   ```bash
   python demo.py
   ```
   If demo works but main.py doesn't, it's likely an API issue.

4. **Check Python version:**
   ```bash
   python --version
   ```
   Requires Python 3.8+

5. **Review error messages carefully:** They usually indicate the specific problem.

## API Status Checks

### Yahoo Finance
- Website: https://finance.yahoo.com
- If website loads but API fails, it's a temporary issue

### Deribit
- API Test: https://www.deribit.com/api/v2/public/test
- Status: https://www.deribit.com/

## Workarounds for API Issues

### Use Demo Script
```bash
python demo.py
```
Works offline with sample parameters.

### Use Cached Data
If you have previously run the script successfully, you can reuse cached data (if implemented).

### Use Alternative Data Sources
You can modify `src/utils/data_fetcher.py` to use alternative data sources like:
- CryptoCompare API
- Binance API
- Local CSV files

## Performance Tips

1. **Use fewer simulations for testing:**
   ```python
   NUM_SIMULATIONS = 100  # Quick test
   ```

2. **Use shorter time series for MLE:**
   Modify `START_DATE` in main.py to a more recent date

3. **Profile slow code:**
   ```bash
   python -m cProfile -s cumulative main.py > profile.txt
   ```

4. **Use PyPy for faster execution** (optional):
   ```bash
   pypy3 -m pip install -r requirements.txt
   pypy3 main.py
   ```

## Still Having Issues?

Create an issue with:
1. Full error message
2. Python version (`python --version`)
3. Operating system
4. Steps to reproduce
5. Output of: `pip list | grep -E "(numpy|scipy|pandas|yfinance)"`

---

**Last Updated:** December 3, 2025
