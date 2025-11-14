# Day Trading Stock Screener

A comprehensive Python application that analyzes US stocks in real-time and provides day trading recommendations with confidence scores and predicted price movements.

## Features

### Basic Screener (`day_trading_screener.py`)
- ✅ Real-time stock data fetching via yfinance
- ✅ Technical indicator calculations:
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
  - Bollinger Bands
  - VWAP (Volume Weighted Average Price)
  - Moving Averages (SMA/EMA)
  - ATR (Average True Range)
  - Volume analysis
- ✅ Multi-factor confidence scoring (0-100)
- ✅ Predicted price movement percentage
- ✅ Trade direction recommendations (LONG/SHORT/NEUTRAL)
- ✅ Risk level assessment (LOW/MEDIUM/HIGH)
- ✅ Automated stock universe scanning
- ✅ CSV export of results

### Advanced Screener (`advanced_screener.py`)
- ✅ All basic features PLUS:
- ✅ Extended technical indicators:
  - Stochastic Oscillator
  - ADX (Average Directional Index)
  - OBV (On Balance Volume)
  - MFI (Money Flow Index)
  - Ichimoku Cloud
  - Parabolic SAR
- ✅ Machine Learning predictions
- ✅ Sentiment analysis integration capability
- ✅ Fundamental data (market cap, beta, sector, etc.)
- ✅ Enhanced confidence scoring
- ✅ Multi-timeframe analysis (5m, 1h, daily)

## Installation

```bash
# Clone or download the repository
cd day_trading_screener

# Install required packages
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from day_trading_screener import DayTradingScreener

# Initialize screener
screener = DayTradingScreener(
    min_price=5.0,        # Minimum stock price
    max_price=500.0,      # Maximum stock price
    min_volume=1000000    # Minimum average volume
)

# Scan all stocks
results = screener.scan_all_stocks(top_n=20)

# Generate report
report = screener.generate_report(results)
print(report)

# Save to CSV
results.to_csv('trading_opportunities.csv', index=False)
```

### Custom Stock Universe

```python
# Analyze specific stocks
custom_tickers = ['AAPL', 'TSLA', 'NVDA', 'AMD', 'META']
results = screener.scan_all_stocks(custom_tickers=custom_tickers, top_n=10)
```

### Analyze Single Stock

```python
# Get detailed analysis for one stock
analysis = screener.analyze_stock('AAPL')
print(f"Ticker: {analysis['ticker']}")
print(f"Confidence Score: {analysis['confidence_score']}")
print(f"Predicted Move: {analysis['predicted_move_pct']}%")
print(f"Direction: {analysis['trade_direction']}")
```

## Understanding the Output

### Confidence Score (0-100)
Measures the strength of trading signals:
- **80-100**: Very strong signals, high alignment
- **60-79**: Strong signals
- **40-59**: Moderate signals
- **20-39**: Weak signals
- **0-19**: Very weak or conflicting signals

Calculated from:
- RSI position (15% weight)
- MACD signals (20% weight)
- Bollinger Band position (10% weight)
- VWAP relationship (20% weight)
- Moving average alignment (15% weight)
- Volume activity (10% weight)
- Momentum (10% weight)

### Predicted Move Percentage
Estimates the potential intraday price movement based on:
- Current volatility (ATR)
- Signal strength and direction
- Volume patterns
- Historical price action

Example: `+2.5%` means a predicted upward move of 2.5%

### Trade Direction
- **LONG**: Bullish signals dominate (buy opportunity)
- **SHORT**: Bearish signals dominate (short opportunity)
- **NEUTRAL**: Mixed or weak signals (avoid)
- **STRONG_LONG/SHORT**: (Advanced only) Very strong directional bias

### Risk Level
- **LOW**: Low volatility, stable volume patterns
- **MEDIUM**: Moderate volatility or volume
- **HIGH**: High volatility, unusual volume, or high beta

## Sample Output

```
================================================================================
DAY TRADING OPPORTUNITIES - 2025-11-14 09:30:00
================================================================================

#1. NVDA - $145.32
   Direction: LONG
   Confidence Score: 87.5/100
   Predicted Move: +2.34%
   Risk Level: MEDIUM
   Day Change: +1.23%
   RSI: 45.2
   Volume Ratio: 1.87x

#2. TSLA - $242.18
   Direction: LONG
   Confidence Score: 82.3/100
   Predicted Move: +3.12%
   Risk Level: HIGH
   Day Change: +2.45%
   RSI: 58.7
   Volume Ratio: 2.14x

#3. AMD - $142.56
   Direction: SHORT
   Confidence Score: 76.8/100
   Predicted Move: -1.89%
   Risk Level: MEDIUM
   Day Change: -0.87%
   RSI: 72.3
   Volume Ratio: 1.45x
```

## Advanced Features

### Machine Learning Integration

```python
from advanced_screener import AdvancedDayTradingScreener

screener = AdvancedDayTradingScreener(use_ml=True)

# Train ML model with historical data (optional)
# historical_data = fetch_historical_data()
# screener.train_ml_model(historical_data)

# Analyze with ML predictions
analysis = screener.analyze_with_sentiment('AAPL')
print(f"ML Probability (upward): {analysis['ml_probability']}%")
print(f"ML Confidence: {analysis['ml_confidence']}%")
```

### Sentiment Analysis Integration

```python
# If you have a sentiment agent/API
sentiment_score = get_sentiment_for_stock('AAPL')  # Returns -1 to 1

# Integrate sentiment into analysis
analysis = screener.analyze_with_sentiment('AAPL', sentiment_score=sentiment_score)
print(f"Sentiment Score: {analysis['sentiment_score']}")
print(f"Sentiment Impact: {analysis['sentiment_impact']}")
```

## Technical Indicators Explained

### RSI (Relative Strength Index)
- **< 30**: Oversold (potential buy)
- **> 70**: Overbought (potential sell)
- **40-60**: Neutral zone

### MACD
- **Bullish Crossover**: MACD line crosses above signal line
- **Bearish Crossover**: MACD line crosses below signal line
- **Histogram**: Shows momentum strength

### Bollinger Bands
- **Price at Lower Band**: Potential bounce opportunity
- **Price at Upper Band**: Potential reversal
- **BB Squeeze**: Low volatility, breakout imminent

### VWAP
- **Price > VWAP**: Bullish (buyers in control)
- **Price < VWAP**: Bearish (sellers in control)
- Used by institutions for trade execution

### Volume Analysis
- **Volume Ratio > 1.5**: High activity (confirmation)
- **Volume Ratio < 1.0**: Below average (weak signal)

## Best Practices

1. **Pre-Market Preparation**
   ```python
   # Run scan before market opens
   screener = DayTradingScreener()
   results = screener.scan_all_stocks(top_n=30)
   # Review results and create watchlist
   ```

2. **Intraday Monitoring**
   ```python
   # Check specific stocks throughout the day
   watchlist = ['AAPL', 'NVDA', 'TSLA']
   for ticker in watchlist:
       analysis = screener.analyze_stock(ticker)
       # Check if signals changed
   ```

3. **Risk Management**
   - Use the predicted move % to set stop-losses
   - Higher risk levels require tighter stops
   - Never risk more than 1-2% per trade

4. **Signal Confirmation**
   - High confidence scores (>70) are more reliable
   - Wait for multiple indicator alignment
   - Confirm with volume (ratio > 1.2)

5. **Market Context**
   - Check SPY/QQQ trend before individual stocks
   - Avoid trading against the overall market
   - Best opportunities align with market direction

## Customization

### Adjust Filtering Criteria

```python
screener = DayTradingScreener(
    min_price=10.0,       # Higher minimum price
    max_price=300.0,      # Lower maximum price
    min_volume=5000000    # Higher volume requirement
)
```

### Modify Indicator Periods

Edit the calculation methods in the screener class:
```python
# Change RSI period from 14 to 9 for faster signals
df = self._calculate_rsi(df, period=9)
```

### Weight Adjustment

Modify `_calculate_confidence_score()` to change indicator weights:
```python
weights = {
    'vwap_signal': 0.30,    # Increase VWAP importance
    'rsi_signal': 0.10,     # Decrease RSI importance
    # ... adjust as needed
}
```

## Integration with Stock Sentiment Agent

```python
# Example integration
from day_trading_screener import DayTradingScreener
from your_sentiment_agent import StockSentimentAnalyzer

screener = DayTradingScreener()
sentiment_analyzer = StockSentimentAnalyzer()

# Get top technical opportunities
technical_results = screener.scan_all_stocks(top_n=50)

# Enhance with sentiment
final_results = []
for _, stock in technical_results.iterrows():
    sentiment = sentiment_analyzer.analyze(stock['ticker'])
    
    # Combine scores
    combined_score = (
        stock['confidence_score'] * 0.7 +  # 70% technical
        sentiment['score'] * 0.3            # 30% sentiment
    )
    
    final_results.append({
        **stock,
        'sentiment': sentiment['score'],
        'combined_score': combined_score
    })

# Sort by combined score
final_df = pd.DataFrame(final_results).sort_values('combined_score', ascending=False)
```

## Limitations & Disclaimers

⚠️ **Important Notes:**

1. **Data Dependency**: Relies on yfinance API (may have delays or limitations)
2. **Market Hours**: Best used during regular trading hours (9:30 AM - 4:00 PM ET)
3. **Liquidity**: Requires minimum volume threshold for reliable signals
4. **Not Financial Advice**: This tool is for informational purposes only
5. **Past Performance**: Historical accuracy does not guarantee future results
6. **Risk**: Day trading involves substantial risk of loss

## Performance Optimization

### For Faster Scanning

```python
# Reduce stock universe
quick_scan = ['SPY', 'QQQ', 'AAPL', 'TSLA', 'NVDA']
results = screener.scan_all_stocks(custom_tickers=quick_scan)

# Use shorter data periods
df = self.fetch_stock_data(ticker, period="1d", interval="5m")
```

### For More Accuracy

```python
# Extend lookback period
df = self.fetch_stock_data(ticker, period="5d", interval="5m")

# Add more indicators (in advanced version)
screener = AdvancedDayTradingScreener(use_ml=True)
```

## Troubleshooting

### Common Issues

1. **No stocks found**
   - Lower min_volume threshold
   - Expand price range
   - Check if market is open

2. **Slow scanning**
   - Reduce stock universe
   - Use faster interval (15m instead of 5m)
   - Implement caching

3. **yfinance errors**
   - Check internet connection
   - Verify ticker symbols
   - Try alternative data source

## Future Enhancements

- [ ] Real-time WebSocket data feeds
- [ ] Backtesting framework
- [ ] Paper trading integration
- [ ] Discord/Slack notifications
- [ ] Web dashboard interface
- [ ] More exchange support (crypto, forex)
- [ ] Options flow analysis
- [ ] Dark pool activity detection

## Contributing

Contributions welcome! Areas for improvement:
- Additional technical indicators
- Better ML models
- Performance optimization
- More data sources
- UI/visualization improvements

## License

MIT License - Use at your own risk

## Support

For issues or questions:
1. Check this README
2. Review the code comments
3. Test with small stock universe first
4. Verify data availability

---

**Remember**: Always practice proper risk management and never trade with money you can't afford to lose!
