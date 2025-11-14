# Quick Start Guide - Day Trading Stock Screener

## Installation (5 minutes)

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Verify installation
python config.py
```

## Run Your First Scan (2 minutes)

```bash
# Basic scan - analyzes default stock universe
python day_trading_screener.py
```

This will:
- Scan ~60 popular stocks
- Calculate technical indicators
- Generate confidence scores
- Output top 15 opportunities
- Save results to CSV

## Quick Examples

### 1. Analyze Your Watchlist
```python
from day_trading_screener import DayTradingScreener

screener = DayTradingScreener()
results = screener.scan_all_stocks(
    custom_tickers=['AAPL', 'TSLA', 'NVDA'],
    top_n=10
)
print(screener.generate_report(results))
```

### 2. Get Single Stock Analysis
```python
analysis = screener.analyze_stock('NVDA')
print(f"{analysis['ticker']}: {analysis['confidence_score']}% confidence")
print(f"Predicted move: {analysis['predicted_move_pct']}%")
print(f"Direction: {analysis['trade_direction']}")
```

### 3. Run Example Scripts
```bash
python examples.py
# Choose from 6 different example use cases
```

## Understanding Output

### Confidence Score (0-100)
- **80-100**: Very strong signals ⭐⭐⭐
- **60-79**: Strong signals ⭐⭐
- **40-59**: Moderate signals ⭐
- **Below 40**: Weak signals ❌

### Trade Direction
- **LONG**: Buy opportunity (bullish signals)
- **SHORT**: Short opportunity (bearish signals)
- **NEUTRAL**: No clear direction

### Risk Level
- **LOW**: Stable, low volatility
- **MEDIUM**: Moderate volatility
- **HIGH**: High volatility, requires tight stops

## Sample Output
```
#1. NVDA - $145.32
   Direction: LONG
   Confidence Score: 87.5/100
   Predicted Move: +2.34%
   Risk Level: MEDIUM
   RSI: 45.2
   Volume Ratio: 1.87x
```

## Customization

Edit `config.py` to adjust:
- Price ranges
- Volume requirements
- Technical indicator periods
- Confidence score weights
- Stock universe

## Integration with Sentiment Agent

```python
from day_trading_screener import DayTradingScreener
# from your_sentiment_agent import analyze_sentiment

screener = DayTradingScreener()
results = screener.scan_all_stocks()

# Enhance with sentiment
for _, stock in results.iterrows():
    # sentiment = analyze_sentiment(stock['ticker'])
    # Combine technical + sentiment scores
    pass
```

## Best Practices

1. **Run Before Market Opens**
   - Scan 30-60 minutes before 9:30 AM ET
   - Create your watchlist
   - Set alerts

2. **Focus on High Confidence**
   - Only trade signals > 70% confidence
   - Check multiple indicators align
   - Confirm with volume

3. **Risk Management**
   - Use 2% stop losses
   - Position size based on risk level
   - Never risk more than you can afford

4. **Market Context**
   - Check SPY/QQQ trend first
   - Best opportunities align with market
   - Avoid fighting the trend

## Common Issues

**No results found:**
- Lower min_volume in config
- Expand price range
- Check if market is open

**Slow scanning:**
- Reduce stock universe
- Use larger interval (15m vs 5m)

**Import errors:**
- Run: `pip install -r requirements.txt`

## Next Steps

1. ✅ Run basic scan
2. ✅ Review top opportunities
3. ✅ Customize config.py
4. ✅ Try example scripts
5. ✅ Integrate with your sentiment agent
6. ✅ Backtest your strategy

## Files Overview

- `day_trading_screener.py` - Main screener (start here)
- `advanced_screener.py` - ML & sentiment features
- `config.py` - Customize all settings
- `examples.py` - 6 usage examples
- `requirements.txt` - Python dependencies
- `README.md` - Full documentation

## Support

Read the full `README.md` for:
- Detailed explanations
- Advanced features
- Technical indicator descriptions
- Integration patterns
- Troubleshooting

---

⚠️ **Disclaimer**: This tool is for educational purposes only. Not financial advice. Always practice proper risk management.

🚀 **Ready to scan?** Run: `python day_trading_screener.py`
