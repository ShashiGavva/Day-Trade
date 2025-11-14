# How to Use the Advanced Screener

## What You Just Ran

When you ran `python advanced_screener.py`, you just loaded the module. It showed you what features are available but didn't actually scan any stocks.

## How to Actually Scan Stocks

### Option 1: Use the Quick Start Script (EASIEST)

```bash
python run_advanced_screener.py
```

This will:
- Scan 10 popular stocks (AAPL, NVDA, TSLA, etc.)
- Takes ~30-60 seconds
- Shows you results immediately
- Saves to CSV file

### Option 2: Use the Basic Screener (RECOMMENDED FOR DAILY USE)

```bash
python day_trading_screener.py
```

This is actually better for most users because:
- Faster and simpler
- Has everything you need
- Scans all S&P 500 stocks
- Takes 20-25 minutes

### Option 3: Custom Python Script

Create your own script:

```python
from advanced_screener import AdvancedDayTradingScreener

# Initialize
screener = AdvancedDayTradingScreener(
    min_price=5.0,
    max_price=500.0,
    min_volume=1000000,
    use_ml=False  # Set True if you have trained ML model
)

# Analyze single stock
result = screener.analyze_with_sentiment(
    ticker='AAPL',
    sentiment_score=None  # Or 0.75 if you have sentiment data
)

print(f"Stock: {result['ticker']}")
print(f"Confidence: {result['confidence_score']}")
print(f"Direction: {result['trade_direction']}")
print(f"Predicted Move: {result['predicted_move_pct']}%")

# Scan multiple stocks
my_watchlist = ['AAPL', 'NVDA', 'TSLA', 'AMD']

for ticker in my_watchlist:
    result = screener.analyze_with_sentiment(ticker)
    if result:
        print(f"{ticker}: {result['confidence_score']:.1f}% confidence")
```

## Quick Command Reference

```bash
# Quick scan (30-60 seconds)
python run_advanced_screener.py

# Full S&P 500 scan (20-25 minutes) - Use basic screener
python day_trading_screener.py

# Interactive examples
python examples.py
```

## What's the Difference?

### Basic Screener (`day_trading_screener.py`)
- ✅ Ready to use
- ✅ Fast and simple
- ✅ All core indicators
- ✅ **USE THIS ONE for daily scanning**

### Advanced Screener (`advanced_screener.py`)
- More indicators (Stochastic, ADX, MFI, Ichimoku)
- Machine Learning support (needs training first)
- Sentiment integration (needs your sentiment agent)
- **Use this if you need advanced features**

## Next Steps

1. **For quick results now:**
   ```bash
   python run_advanced_screener.py
   ```

2. **For daily scanning:**
   ```bash
   python day_trading_screener.py
   ```

3. **To customize:**
   - Edit `run_advanced_screener.py`
   - Change the `popular_stocks` list
   - Add your own tickers

## Common Tasks

### Scan Your Watchlist
```python
from advanced_screener import AdvancedDayTradingScreener

screener = AdvancedDayTradingScreener(use_ml=False)

my_stocks = ['AAPL', 'NVDA', 'TSLA', 'AMD', 'MSFT']

for ticker in my_stocks:
    result = screener.analyze_with_sentiment(ticker)
    print(f"{ticker}: {result['confidence_score']:.1f}%")
```

### Add Sentiment Analysis
```python
# Your sentiment agent
sentiment_score = your_sentiment_agent.analyze('AAPL')  # Returns -1 to 1

# Use with screener
result = screener.analyze_with_sentiment(
    ticker='AAPL',
    sentiment_score=sentiment_score
)

print(f"Technical: {result['confidence_score']}")
print(f"Sentiment: {result['sentiment_score']}")
```

### Scan by Sector
```python
tech_stocks = ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'AMD']
finance_stocks = ['JPM', 'BAC', 'GS', 'MS', 'C']

# Scan tech sector
print("Tech Sector:")
for ticker in tech_stocks:
    result = screener.analyze_with_sentiment(ticker)
    print(f"  {ticker}: {result['trade_direction']}")
```

## Summary

**To scan stocks RIGHT NOW:**
```bash
python run_advanced_screener.py
```

**For daily use:**
```bash
python day_trading_screener.py
```

**For custom analysis:**
Edit `run_advanced_screener.py` or create your own script!

The advanced screener gives you more indicators and features, but the basic screener is perfect for most traders.
