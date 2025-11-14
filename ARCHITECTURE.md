# Day Trading Screener - Architecture & Workflow

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Day Trading Screener System                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────┐
│  Configuration  │
│   (config.py)   │
│                 │
│ • Price ranges  │
│ • Indicators    │
│ • Weights       │
│ • Risk params   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Data Layer                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│   ┌─────────────┐      ┌──────────────┐      ┌──────────────┐  │
│   │  yfinance   │─────▶│ Stock Data   │─────▶│   Pandas     │  │
│   │  (API)      │      │ Fetching     │      │  DataFrame   │  │
│   └─────────────┘      └──────────────┘      └──────────────┘  │
│                                                                   │
└───────────────────────────────┬───────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Technical Analysis Engine                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │     RSI      │  │     MACD     │  │   Bollinger  │          │
│  │   14-period  │  │  12/26/9     │  │    Bands     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │     VWAP     │  │   Moving     │  │    Volume    │          │
│  │              │  │   Averages   │  │   Analysis   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │     ATR      │  │  Stochastic  │  │     ADX      │          │
│  │  (Volatility)│  │  (Advanced)  │  │  (Advanced)  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                   │
└───────────────────────────────┬───────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Signal Generation                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│   Each Indicator → Signal Score (-1, 0, +1)                      │
│                                                                   │
│   RSI < 30      → +1 (Oversold/Bullish)                         │
│   RSI > 70      → -1 (Overbought/Bearish)                       │
│   MACD Cross ↑  → +1 (Bullish)                                  │
│   MACD Cross ↓  → -1 (Bearish)                                  │
│   Price > VWAP  → +1 (Bullish)                                  │
│   Volume > 1.5x → +1 (Confirmation)                             │
│   etc...                                                         │
│                                                                   │
└───────────────────────────────┬───────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Scoring & Analysis Layer                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │         Confidence Score Calculation (0-100)            │    │
│  │                                                          │    │
│  │  Weighted Sum:                                          │    │
│  │  • RSI Signal      × 15%                                │    │
│  │  • MACD Signal     × 20%                                │    │
│  │  • BB Signal       × 10%                                │    │
│  │  • VWAP Signal     × 20%                                │    │
│  │  • MA Signal       × 15%                                │    │
│  │  • Volume Signal   × 10%                                │    │
│  │  • Momentum        × 10%                                │    │
│  │                                                          │    │
│  │  Bonuses:                                                │    │
│  │  • Signal Alignment: +20%                               │    │
│  │  • BB Squeeze:       +10%                               │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │           Price Movement Prediction                      │    │
│  │                                                          │    │
│  │  Base: ATR (Average True Range)                         │    │
│  │  Direction: Sum of signals                              │    │
│  │  Magnitude: Signal strength × Volatility                │    │
│  │  Volume Boost: +20% if high volume                      │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              Risk Assessment                             │    │
│  │                                                          │    │
│  │  Factors:                                                │    │
│  │  • Volatility (ATR %)                                   │    │
│  │  • Volume patterns                                       │    │
│  │  • Beta (if available)                                   │    │
│  │                                                          │    │
│  │  Output: LOW / MEDIUM / HIGH                            │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                   │
└───────────────────────────────┬───────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Optional: ML Enhancement                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │         Machine Learning Model (Advanced)               │    │
│  │                                                          │    │
│  │  Features:                                               │    │
│  │  • All technical indicators                             │    │
│  │  • Price changes (1, 5, 20 periods)                     │    │
│  │  • Volatility measures                                   │    │
│  │  • Volume ratios                                         │    │
│  │                                                          │    │
│  │  Model: Random Forest Classifier                        │    │
│  │  Output: Probability of upward move                      │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │         Sentiment Integration (Optional)                 │    │
│  │                                                          │    │
│  │  Your Sentiment Agent → Sentiment Score (-1 to +1)      │    │
│  │  Combined: Technical (70%) + Sentiment (30%)            │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                   │
└───────────────────────────────┬───────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Output & Reporting                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────────────┐    ┌────────────────────┐              │
│  │  Console Report    │    │    CSV Export      │              │
│  │  • Top N stocks    │    │  • Full results    │              │
│  │  • Rankings        │    │  • All metrics     │              │
│  │  • Key metrics     │    │  • Timestamps      │              │
│  └────────────────────┘    └────────────────────┘              │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
┌──────────┐
│  Start   │
└────┬─────┘
     │
     ▼
┌──────────────────┐
│ Load Config      │
│ • Price range    │
│ • Volume min     │
│ • Indicator      │
│   settings       │
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│ Get Stock        │
│ Universe         │
│ • Default: 60+   │
│ • Custom list    │
└────┬─────────────┘
     │
     ▼
┌──────────────────────────────┐
│ For Each Stock:              │
│                              │
│  1. Fetch Data               │
│     ├─ 5m intervals (5 days) │
│     ├─ OHLCV data            │
│     └─ Volume info           │
│                              │
│  2. Filter                   │
│     ├─ Price check           │
│     └─ Volume check          │
│                              │
│  3. Calculate Indicators     │
│     ├─ RSI                   │
│     ├─ MACD                  │
│     ├─ Bollinger Bands       │
│     ├─ VWAP                  │
│     ├─ Moving Averages       │
│     ├─ ATR                   │
│     └─ Volume Analysis       │
│                              │
│  4. Generate Signals         │
│     ├─ RSI signal            │
│     ├─ MACD signal           │
│     ├─ BB signal             │
│     ├─ VWAP signal           │
│     ├─ MA signal             │
│     ├─ Volume signal         │
│     └─ Momentum signal       │
│                              │
│  5. Calculate Scores         │
│     ├─ Confidence (0-100)    │
│     ├─ Predicted move %      │
│     ├─ Direction             │
│     └─ Risk level            │
│                              │
│  6. Optional ML/Sentiment    │
│     ├─ ML probability        │
│     └─ Sentiment score       │
└────┬─────────────────────────┘
     │
     ▼
┌──────────────────┐
│ Collect Results  │
│ • All analyzed   │
│   stocks         │
│ • Filter valid   │
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│ Rank by          │
│ Confidence       │
│ • Sort desc      │
│ • Take top N     │
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│ Generate Output  │
│ • Console report │
│ • CSV file       │
└────┬─────────────┘
     │
     ▼
┌──────────┐
│   Done   │
└──────────┘
```

## Typical Workflow

### Morning Pre-Market Routine
```
7:00 AM  │ Configure screener for the day
         │ Edit config.py if needed
         │
8:00 AM  │ Run full market scan
         │ python day_trading_screener.py
         │
8:15 AM  │ Review top 20 opportunities
         │ Check confidence scores
         │ Verify with your sentiment agent
         │
8:30 AM  │ Create watchlist
         │ Tier 1: Confidence > 80%
         │ Tier 2: Confidence 60-80%
         │
9:00 AM  │ Set up charts
         │ Prepare entry/exit plans
         │ Set alerts
         │
9:30 AM  │ Market opens
         │ Monitor watchlist
         │ Execute high-conviction setups
```

### Intraday Monitoring
```
During Trading Hours:

┌─────────────────────────────────────┐
│  Every 30-60 minutes:               │
│                                     │
│  1. Re-scan watchlist               │
│     screener.analyze_stock(ticker)  │
│                                     │
│  2. Check signal changes            │
│     • Confidence trending up?       │
│     • New indicator triggers?       │
│                                     │
│  3. Manage positions                │
│     • Move stops                    │
│     • Take profits                  │
│     • Exit weak signals             │
└─────────────────────────────────────┘
```

### Integration Pattern with Sentiment Agent

```
┌─────────────────────────────────────────────────────┐
│                Combined Analysis Flow                │
└─────────────────────────────────────────────────────┘

┌──────────────────┐          ┌──────────────────┐
│  Your Sentiment  │          │  This Screener   │
│     Agent        │          │  (Technical)     │
└────────┬─────────┘          └────────┬─────────┘
         │                              │
         │  Sentiment Score            │  Technical Score
         │  (-1 to +1)                  │  (0-100)
         │                              │
         └──────────┬───────────────────┘
                    │
                    ▼
         ┌─────────────────────┐
         │  Combined Scoring   │
         │                     │
         │  Final Score =      │
         │    Technical × 70%  │
         │  + Sentiment × 30%  │
         └──────────┬──────────┘
                    │
                    ▼
         ┌─────────────────────┐
         │  Decision Making    │
         │                     │
         │  If Combined > 80:  │
         │    → Strong Buy     │
         │  If Combined > 60:  │
         │    → Moderate Buy   │
         │  Else:              │
         │    → Watch/Skip     │
         └─────────────────────┘
```

## File Structure

```
day_trading_screener/
│
├── day_trading_screener.py      [Main application - 21KB]
│   └── Class: DayTradingScreener
│       ├── get_stock_universe()
│       ├── fetch_stock_data()
│       ├── calculate_technical_indicators()
│       ├── analyze_stock()
│       ├── scan_all_stocks()
│       └── generate_report()
│
├── advanced_screener.py         [Extended features - 23KB]
│   └── Class: AdvancedDayTradingScreener
│       ├── All basic features +
│       ├── Extended indicators
│       ├── ML model training
│       └── Sentiment integration
│
├── config.py                    [Configuration - 8.8KB]
│   ├── All parameters
│   ├── Validation functions
│   └── Helper functions
│
├── examples.py                  [Usage examples - 11KB]
│   ├── Example 1: Basic scan
│   ├── Example 2: Custom tickers
│   ├── Example 3: Single stock
│   ├── Example 4: Filtering
│   ├── Example 5: Watchlist
│   └── Example 6: Comparison
│
├── requirements.txt             [Dependencies - 160B]
│   ├── yfinance
│   ├── pandas
│   ├── numpy
│   └── scikit-learn
│
├── README.md                    [Full docs - 11KB]
├── QUICKSTART.md                [Quick guide - 3.9KB]
└── PROJECT_SUMMARY.md           [Overview - 8.2KB]
```

## Key Classes & Methods

### DayTradingScreener

```python
# Initialize
screener = DayTradingScreener(
    min_price=5.0,
    max_price=500.0,
    min_volume=1000000
)

# Main methods
screener.scan_all_stocks(custom_tickers=None, top_n=20)
screener.analyze_stock(ticker)
screener.generate_report(results_df)

# Core calculations
screener.calculate_technical_indicators(df)
screener._generate_signals(df, latest, prev)
screener._calculate_confidence_score(signals)
screener._predict_price_move(df, signals)
```

## Performance Metrics

```
Operation              Time        Notes
─────────────────────────────────────────────────────
Single stock fetch     2-3 sec     Via yfinance API
Calculate indicators   <1 sec      Pure pandas/numpy
Generate signals       <0.1 sec    Fast computation
Full scan (60 stocks)  2-3 min     API rate limit
Custom scan (10)       20-30 sec   User watchlist
```

## Decision Tree

```
Stock Analysis Decision Flow:

START
  │
  ├─▶ Price < $5 OR > $500? ──YES──▶ SKIP
  │                  NO
  │                   │
  ├─▶ Volume < 1M? ──YES──▶ SKIP
  │                  NO
  │                   │
  └─▶ Calculate Indicators
           │
           ├─▶ RSI < 30? ──YES──▶ +1 Signal
           ├─▶ RSI > 70? ──YES──▶ -1 Signal
           │
           ├─▶ MACD Cross Up? ──YES──▶ +1 Signal
           ├─▶ MACD Cross Down? ──YES──▶ -1 Signal
           │
           ├─▶ Price at BB Lower? ──YES──▶ +1 Signal
           ├─▶ Price at BB Upper? ──YES──▶ -1 Signal
           │
           ├─▶ Price > VWAP? ──YES──▶ +1 Signal
           ├─▶ Price < VWAP? ──YES──▶ -1 Signal
           │
           └─▶ Combine All Signals
                    │
                    ├─▶ Calculate Confidence
                    ├─▶ Predict Movement
                    ├─▶ Assess Risk
                    │
                    └─▶ OUTPUT RESULTS
```

---

This architecture provides a robust, scalable foundation for day trading analysis that can be easily extended with your sentiment agent or other data sources!
