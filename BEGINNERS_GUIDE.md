# Complete Beginner's Guide to Using Your Day Trading Screener

## 🎯 Table of Contents
1. [When to Run the Screener](#when-to-run)
2. [Understanding the Output](#understanding-output)
3. [How to Set Indicators](#setting-indicators)
4. [Step-by-Step Daily Workflow](#daily-workflow)
5. [Customizing for Your Style](#customization)
6. [Practical Examples](#practical-examples)
7. [Common Questions](#faq)

---

## 📅 When to Run the Screener {#when-to-run}

### Best Times to Scan

#### **Pre-Market (7:00 AM - 9:30 AM ET)**
```bash
# Run around 8:00-9:00 AM ET
python day_trading_screener.py
```
**Purpose**: Create your daily watchlist before market opens
- Market is closed, so you get pre-market setup data
- Gives you time to research top picks
- Plan your trades without pressure
- Set up charts and alerts

#### **Market Open (9:30 AM - 10:00 AM ET)**
```bash
# Run at 9:45 AM to catch opening momentum
python day_trading_screener.py
```
**Purpose**: Find stocks with strong opening momentum
- High volume, high volatility
- Best opportunities often appear here
- Look for confidence >75%

#### **Mid-Morning (10:30 AM - 11:00 AM ET)**
```bash
# Re-scan to update signals
python day_trading_screener.py
```
**Purpose**: Catch second wave of opportunities
- Early momentum has settled
- New patterns emerging
- Good for swing entries

#### **Afternoon Session (2:00 PM - 3:00 PM ET)**
```bash
# Afternoon scan for power hour setup
python day_trading_screener.py
```
**Purpose**: Position for final hour trading
- Find stocks building for close
- Power hour opportunities (3-4 PM)

### ⏰ Quick Time Reference
```
Best Times for Day Trading:
├─ 9:30-11:00 AM ET  ⭐⭐⭐ (Best - highest volume)
├─ 11:00 AM-2:00 PM  ⭐    (Slower - lunch period)
└─ 2:00-4:00 PM ET   ⭐⭐  (Good - power hour)

When to Scan:
├─ Pre-market:  8:00-9:00 AM   (Preparation)
├─ Open:        9:45 AM        (Momentum plays)
├─ Mid-morning: 10:30 AM       (Follow-through)
└─ Afternoon:   2:30 PM        (Power hour setup)
```

---

## 📊 Understanding the Output {#understanding-output}

### Sample Output Explained

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
```

Let's break down EVERY piece of information:

### Line-by-Line Explanation

#### **#1. NVDA - $145.32**
```
#1          → Rank (1 is best opportunity)
NVDA        → Stock ticker symbol
$145.32     → Current price per share
```

#### **Direction: LONG**
```
LONG        → Buy opportunity (stock likely to go UP)
SHORT       → Short opportunity (stock likely to go DOWN)  
NEUTRAL     → No clear direction, avoid trading
```
**What to do**: 
- LONG → Look to BUY
- SHORT → Look to SHORT/sell
- NEUTRAL → Skip this stock

#### **Confidence Score: 87.5/100**
This is THE MOST IMPORTANT NUMBER!

```
90-100  → Extremely strong signals ⭐⭐⭐⭐⭐
80-89   → Very strong signals     ⭐⭐⭐⭐
70-79   → Strong signals          ⭐⭐⭐
60-69   → Moderate signals        ⭐⭐
50-59   → Weak signals            ⭐
< 50    → Very weak, avoid        ❌
```

**What it means**:
- Higher = More indicators agree on direction
- 87.5 = Very strong, 7+ indicators aligned
- Only trade when >70% for beginners

**How it's calculated**:
```
Combines these signals:
├─ RSI position        (15% weight)
├─ MACD signals        (20% weight)
├─ Bollinger Bands     (10% weight)
├─ VWAP relationship   (20% weight)
├─ Moving averages     (15% weight)
├─ Volume activity     (10% weight)
└─ Price momentum      (10% weight)

Bonuses:
├─ All signals agree   (+20%)
└─ BB squeeze detected (+10%)
```

#### **Predicted Move: +2.34%**
```
+2.34%  → Expected price increase by end of day
-1.50%  → Expected price decrease by end of day
```

**What it means**:
- Based on current volatility (ATR) and signal strength
- If current price is $145.32 and predicted +2.34%:
  - Target price = $145.32 × 1.0234 = $148.72
  - Potential profit per share = $3.40

**How to use it**:
```python
Entry Price:     $145.32
Target Price:    $148.72 (+2.34%)
Stop Loss:       $142.41 (-2%)

Risk/Reward:     $2.91 risk / $3.40 reward = 1.17:1
```

#### **Risk Level: MEDIUM**
```
LOW     → Stable, low volatility, safer for beginners
MEDIUM  → Moderate volatility, requires attention
HIGH    → High volatility, tight stops needed
```

**What it means**:
- **LOW**: Stock moves slowly, predictable, good for learning
- **MEDIUM**: Normal day trading risk, typical volatility
- **HIGH**: Stock can move fast, experienced traders only

**How to use it**:
```
LOW Risk:
├─ Position size: Up to 20% of portfolio
├─ Stop loss: 2% below entry
└─ Best for: Beginners, large positions

MEDIUM Risk:
├─ Position size: 10-15% of portfolio
├─ Stop loss: 1.5-2% below entry
└─ Best for: Intermediate traders

HIGH Risk:
├─ Position size: 5-10% of portfolio
├─ Stop loss: 1% below entry
└─ Best for: Experienced traders only
```

#### **Day Change: +1.23%**
```
+1.23%  → Stock is UP 1.23% since market open
-0.87%  → Stock is DOWN 0.87% since market open
```

**What it means**:
- Shows current momentum for the day
- Positive = bullish day, negative = bearish day

#### **RSI: 45.2**
```
< 30    → Oversold (might bounce up) 🔵 Bullish signal
30-70   → Neutral zone
> 70    → Overbought (might pull back) 🔴 Bearish signal
```

**What it means for NVDA at 45.2**:
- Neutral territory
- Not oversold or overbought
- Room to move in either direction
- Combined with other indicators showing LONG

#### **Volume Ratio: 1.87x**
```
< 1.0   → Below average volume (weak signal)
1.0-1.5 → Average to above average
> 1.5   → High volume (strong confirmation) ✅
> 2.0   → Very high volume (major move)
```

**What it means for NVDA at 1.87x**:
- Volume is 87% higher than normal
- Strong confirmation of the move
- Institutions are trading it
- Signal is more reliable

---

## 🎚️ How to Set Indicators {#setting-indicators}

### Option 1: Using config.py (Recommended)

Open `config.py` and you'll see all settings:

```python
# =============================================================================
# FILTERING CRITERIA
# =============================================================================

MIN_PRICE = 5.0          # Only scan stocks $5 or higher
MAX_PRICE = 500.0        # Only scan stocks $500 or lower
MIN_VOLUME = 1_000_000   # Only scan if 1M+ daily volume

# =============================================================================
# TECHNICAL INDICATORS
# =============================================================================

# RSI settings
RSI_PERIOD = 14          # How many periods to calculate RSI
RSI_OVERSOLD = 30        # Below this = oversold
RSI_OVERBOUGHT = 70      # Above this = overbought

# MACD settings
MACD_FAST = 12          # Fast EMA period
MACD_SLOW = 26          # Slow EMA period
MACD_SIGNAL = 9         # Signal line period

# Bollinger Bands
BB_PERIOD = 20          # SMA period
BB_STD_DEV = 2          # Standard deviations

# Moving Averages
SMA_SHORT = 9           # Short SMA
SMA_LONG = 20           # Long SMA
EMA_SHORT = 9           # Short EMA
EMA_LONG = 20           # Long EMA

# Volume
VOLUME_PERIOD = 20              # Average volume period
HIGH_VOLUME_THRESHOLD = 1.5     # 1.5x average = high volume
```

### Common Customizations

#### **For Penny Stocks**
```python
MIN_PRICE = 1.0          # Lower to $1
MAX_PRICE = 10.0         # Cap at $10
MIN_VOLUME = 5_000_000   # Need higher volume for liquidity
```

#### **For Blue Chips Only**
```python
MIN_PRICE = 50.0         # Higher quality stocks
MAX_PRICE = 1000.0       # Include expensive stocks
MIN_VOLUME = 5_000_000   # Ensure liquidity
```

#### **For Faster Signals (Scalping)**
```python
RSI_PERIOD = 7           # Faster RSI
MACD_FAST = 6            # Faster MACD
MACD_SLOW = 13
MACD_SIGNAL = 5
SMA_SHORT = 5            # Faster MAs
EMA_SHORT = 5
```

#### **For Slower Signals (Swing)**
```python
RSI_PERIOD = 21          # Slower RSI
MACD_FAST = 18           # Slower MACD
MACD_SLOW = 39
MACD_SIGNAL = 12
SMA_SHORT = 20           # Slower MAs
EMA_SHORT = 20
```

### Adjusting Confidence Weights

Want to emphasize certain indicators?

```python
# =============================================================================
# CONFIDENCE SCORE WEIGHTS (must sum to ~1.0)
# =============================================================================

CONFIDENCE_WEIGHTS = {
    'rsi_signal': 0.15,      # 15% of confidence from RSI
    'macd_signal': 0.20,     # 20% from MACD
    'bb_signal': 0.10,       # 10% from Bollinger Bands
    'vwap_signal': 0.20,     # 20% from VWAP
    'ma_signal': 0.15,       # 15% from Moving Averages
    'volume_signal': 0.10,   # 10% from Volume
    'momentum_signal': 0.10  # 10% from Momentum
}
```

**Example: Emphasize VWAP and Volume**
```python
CONFIDENCE_WEIGHTS = {
    'rsi_signal': 0.10,      # Reduced
    'macd_signal': 0.15,     # Reduced
    'bb_signal': 0.05,       # Reduced
    'vwap_signal': 0.30,     # Increased! ⬆️
    'ma_signal': 0.10,       # Reduced
    'volume_signal': 0.20,   # Increased! ⬆️
    'momentum_signal': 0.10  # Same
}
```

### Option 2: Quick In-Code Changes

If you want to quickly test settings without editing config.py:

```python
from day_trading_screener import DayTradingScreener

# Initialize with custom settings
screener = DayTradingScreener(
    min_price=10.0,      # Only stocks $10+
    max_price=200.0,     # Max $200
    min_volume=2000000   # 2M+ volume
)

# Run scan
results = screener.scan_all_stocks(top_n=10)
```

---

## 📋 Step-by-Step Daily Workflow {#daily-workflow}

### Morning Routine (30 minutes before market)

#### **Step 1: Run Pre-Market Scan (8:30 AM)**
```bash
python day_trading_screener.py
```

#### **Step 2: Review Output**
Look for:
- ✅ Confidence Score >70%
- ✅ Clear Direction (LONG or SHORT)
- ✅ Volume Ratio >1.2x
- ✅ Risk Level you're comfortable with

#### **Step 3: Create Watchlist**
From the output, categorize stocks:

```
Tier 1 (High Priority):
├─ Confidence 80-100%
├─ Strong volume (>1.5x)
└─ Clear direction
Example: NVDA, TSLA, AMD

Tier 2 (Medium Priority):
├─ Confidence 70-79%
├─ Good volume (>1.2x)
└─ Clear direction
Example: AAPL, MSFT

Tier 3 (Watch Only):
├─ Confidence 60-69%
└─ Monitor for improvement
```

#### **Step 4: Analyze Your Top 3-5 Picks**

For each top pick, ask yourself:

```
1. Does the overall market (SPY/QQQ) support this direction?
   ├─ If market is bullish → LONG trades easier
   └─ If market is bearish → SHORT trades easier

2. Do I understand WHY it's moving?
   ├─ Check news
   ├─ Check sector
   └─ Check earnings calendar

3. What's my plan?
   ├─ Entry price
   ├─ Target price (use predicted move)
   ├─ Stop loss (typically 2% below)
   └─ Position size
```

#### **Step 5: Set Up Your Trading Platform**
```
For each Tier 1 stock:
├─ Open chart
├─ Set price alert at current level
├─ Set alert for target price
├─ Prepare order entry
└─ Ready to execute at 9:30 AM
```

### During Market Hours

#### **9:30 AM: Market Opens**
```
1. Watch your Tier 1 stocks
2. Wait for your entry signal:
   ├─ Price confirms direction
   ├─ Volume confirms (>1.5x)
   └─ You feel confident

3. Enter trade with plan:
   ├─ Buy/Short at planned price
   ├─ Set stop loss immediately
   ├─ Set profit target
```

#### **10:30 AM: Re-Scan**
```bash
python day_trading_screener.py
```
- Check if signals still hold
- Look for new opportunities
- Adjust stops to breakeven if profitable

#### **2:30 PM: Afternoon Scan**
```bash
python day_trading_screener.py
```
- Find power hour setups
- Plan exits for existing positions
- Look for end-of-day opportunities

#### **4:00 PM: Review**
- Document what worked
- Note what didn't
- Adjust strategy

---

## 🎨 Customizing for Your Style {#customization}

### For Scalpers (Quick In/Out)

**Goal**: Many small profits, fast execution

**Settings in config.py**:
```python
# Faster indicators
RSI_PERIOD = 7
MACD_FAST = 6
MACD_SLOW = 13
MACD_SIGNAL = 5

# Higher confidence needed
MIN_CONFIDENCE_SCORE = 75

# High volume required
HIGH_VOLUME_THRESHOLD = 2.0

# Emphasis on momentum
CONFIDENCE_WEIGHTS = {
    'rsi_signal': 0.10,
    'macd_signal': 0.15,
    'bb_signal': 0.05,
    'vwap_signal': 0.25,      # VWAP important for scalping
    'ma_signal': 0.10,
    'volume_signal': 0.20,     # Volume critical
    'momentum_signal': 0.15    # Momentum critical
}
```

**When to scan**: Every 30 minutes
**Target moves**: 0.5-1%
**Hold time**: Minutes to hours

### For Day Traders (Standard)

**Goal**: Capture intraday swings

**Settings in config.py** (defaults are good):
```python
# Standard indicators
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26

# Moderate confidence
MIN_CONFIDENCE_SCORE = 65

# Standard volume
HIGH_VOLUME_THRESHOLD = 1.5
```

**When to scan**: 2-3 times per day
**Target moves**: 1-3%
**Hold time**: Hours

### For Swing Traders (Longer Holds)

**Goal**: Multi-day moves

**Settings in config.py**:
```python
# Slower indicators
RSI_PERIOD = 21
MACD_FAST = 18
MACD_SLOW = 39
MACD_SIGNAL = 12

# Lower confidence OK
MIN_CONFIDENCE_SCORE = 60

# Less emphasis on volume
HIGH_VOLUME_THRESHOLD = 1.2

# Emphasis on trend
CONFIDENCE_WEIGHTS = {
    'rsi_signal': 0.15,
    'macd_signal': 0.25,      # MACD important for trend
    'bb_signal': 0.10,
    'vwap_signal': 0.10,      # VWAP less important
    'ma_signal': 0.25,        # MAs important for trend
    'volume_signal': 0.05,    # Volume less critical
    'momentum_signal': 0.10
}
```

**When to scan**: Once per day
**Target moves**: 3-10%
**Hold time**: 1-5 days

### For Conservative Traders

**Goal**: Lower risk, steady gains

**Settings in config.py**:
```python
# Higher quality only
MIN_PRICE = 20.0
MIN_VOLUME = 5_000_000

# High confidence required
MIN_CONFIDENCE_SCORE = 75

# Lower volatility preferred
LOW_VOLATILITY = 1.5
HIGH_VOLATILITY = 3.0

# Focus on established stocks
CUSTOM_UNIVERSE = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN',
    'JPM', 'BAC', 'WMT', 'JNJ', 'PG'
]
USE_CUSTOM_UNIVERSE = True
```

**Risk management**:
- Only trade LOW risk stocks
- Smaller position sizes (5-10%)
- Wider stops (2-3%)

### For Aggressive Traders

**Goal**: High risk, high reward

**Settings in config.py**:
```python
# Include volatile stocks
MIN_PRICE = 5.0
MAX_PRICE = 1000.0

# Lower confidence OK (trust your analysis)
MIN_CONFIDENCE_SCORE = 60

# Look for high volatility
# Focus on stocks with HIGH risk level

# Include volatile universe
CUSTOM_UNIVERSE = [
    'TSLA', 'NVDA', 'AMD', 'PLTR', 'COIN',
    'RIVN', 'LCID', 'GME', 'AMC'
]
```

**Risk management**:
- Trade HIGH risk stocks
- Tighter stops (1%)
- Smaller positions (5%)
- Higher targets (3-5%)

---

## 💼 Practical Examples {#practical-examples}

### Example 1: Beginner's First Trade

**Scenario**: You ran the screener and got this:

```
#1. AAPL - $178.50
   Direction: LONG
   Confidence Score: 82.0/100
   Predicted Move: +1.50%
   Risk Level: LOW
   RSI: 42.0
   Volume Ratio: 1.65x
```

**Your Analysis**:
```
✅ High confidence (82%)
✅ Clear direction (LONG)
✅ Good volume (1.65x)
✅ LOW risk (perfect for beginner)
✅ RSI neutral (room to move up)
✅ Reasonable target (+1.50%)
```

**Your Trade Plan**:
```python
Entry Price:     $178.50
Target Price:    $181.18 (+1.50% = $2.68 profit)
Stop Loss:       $174.93 (-2% = $3.57 risk)
Risk/Reward:     $3.57 / $2.68 = 1.33:1 (acceptable)

Position Size:
Account Size:    $10,000
Risk Per Trade:  2% = $200
Risk Per Share:  $3.57
Shares to Buy:   $200 / $3.57 = 56 shares

Investment:      56 shares × $178.50 = $9,996
Potential Gain:  56 shares × $2.68 = $150.08
Potential Loss:  $200 (max)
```

**Execution**:
1. At 9:30 AM, wait for AAPL to confirm move up
2. Enter at $178.50 or better
3. Set stop loss at $174.93 immediately
4. Set alert for target at $181.18
5. Exit at target or if stopped out

### Example 2: Intermediate Trading

**You run scan and get 20 results. You filter:**

```python
# Option 1: Manually filter
results_df = screener.scan_all_stocks(top_n=50)

# Show only HIGH confidence LONGs
high_conf_longs = results_df[
    (results_df['confidence_score'] > 75) &
    (results_df['trade_direction'] == 'LONG') &
    (results_df['volume_ratio'] > 1.5)
]

print(high_conf_longs)
```

**Result**:
```
3 stocks meet criteria:
├─ NVDA: 87% confidence, +2.3% predicted
├─ AMD:  81% confidence, +1.8% predicted  
└─ TSLA: 76% confidence, +2.5% predicted
```

**Your Strategy**:
- Trade all 3 with 10% position each
- Diversified across tech sector
- Set stops on all 3
- Monitor throughout day

### Example 3: Combining with Sentiment

```python
from day_trading_screener import DayTradingScreener

# Your screener
screener = DayTradingScreener()
results = screener.scan_all_stocks(top_n=20)

# Enhance with your sentiment (example)
for index, row in results.iterrows():
    ticker = row['ticker']
    technical_score = row['confidence_score']
    
    # Your sentiment code would go here
    # sentiment_score = your_sentiment_agent.analyze(ticker)
    # For example purposes:
    sentiment_score = 75  # placeholder
    
    # Combined score
    combined = (technical_score * 0.7) + (sentiment_score * 0.3)
    
    print(f"{ticker}:")
    print(f"  Technical: {technical_score}")
    print(f"  Sentiment: {sentiment_score}")
    print(f"  Combined:  {combined}")
    
    if combined > 80:
        print(f"  ⭐ STRONG OPPORTUNITY!")
```

---

## ❓ Common Questions (FAQ) {#faq}

### Q: How many stocks should I trade at once?
**A**: 
- Beginner: 1-2 stocks max
- Intermediate: 2-4 stocks
- Advanced: 4-6 stocks
Never spread yourself too thin!

### Q: What confidence score do I need?
**A**:
- Beginner: >75% only
- Intermediate: >70%
- Advanced: >65% with good volume

### Q: When do I exit a trade?
**A**:
```
Exit when:
├─ Hit target price ✅
├─ Hit stop loss ❌
├─ Signal reverses (re-scan shows opposite direction)
├─ Volume dies (ratio drops below 1.0)
├─ End of day (if day trading)
└─ You feel uncomfortable (trust your gut)
```

### Q: What if I lose money?
**A**:
- Losses are part of trading
- Stick to 2% risk per trade
- Review what went wrong
- Adjust strategy
- Never revenge trade

### Q: How often should I run the screener?
**A**:
```
Scalping:    Every 30-60 minutes
Day Trading: 2-3 times per day
Swing:       Once per day
```

### Q: Stock not in default universe?
**A**:
```python
# Create custom list
screener = DayTradingScreener()
custom_tickers = ['YOUR', 'STOCKS', 'HERE']
results = screener.scan_all_stocks(custom_tickers=custom_tickers)
```

### Q: How do I save results?
**A**: They're automatically saved! Look for:
```
day_trading_opportunities_20251114_093000.csv
```

### Q: Can I paper trade first?
**A**: ABSOLUTELY! Use these signals in a paper trading account first. Test for at least 2-4 weeks before using real money.

### Q: The predicted move seems small (1-2%). Is that normal?
**A**: Yes! Day trading is about small, consistent gains:
- 1% per day = 250% per year (if consistent)
- 2% per day = 500%+ per year
- Small gains add up fast!

### Q: What if direction says NEUTRAL?
**A**: Skip it! Only trade when direction is clear (LONG or SHORT).

### Q: Does market direction matter?
**A**: YES!
```
If SPY/QQQ trending up:
└─ LONG trades easier, SHORT trades harder

If SPY/QQQ trending down:
└─ SHORT trades easier, LONG trades harder

Always check overall market first!
```

---

## 🎓 Your Learning Path

### Week 1: Learn the Basics
- [ ] Run screener daily
- [ ] Read all output
- [ ] Don't trade yet, just watch
- [ ] Note which predictions come true

### Week 2: Paper Trade
- [ ] Trade the signals in paper account
- [ ] Track results
- [ ] Adjust confidence threshold
- [ ] Find your style

### Week 3: Customize
- [ ] Adjust config.py for your style
- [ ] Test different indicators
- [ ] Find best time of day for you
- [ ] Refine universe

### Week 4: Go Live (Small)
- [ ] Start with tiny positions
- [ ] Only highest confidence (>80%)
- [ ] Strict stop losses
- [ ] Review every trade

---

## 📝 Quick Reference Card

```
═══════════════════════════════════════════════════════════
                    QUICK REFERENCE
═══════════════════════════════════════════════════════════

RUN SCREENER:
  python day_trading_screener.py

CONFIDENCE SCORE:
  90-100: Extremely strong ⭐⭐⭐⭐⭐
  80-89:  Very strong     ⭐⭐⭐⭐
  70-79:  Strong          ⭐⭐⭐
  < 70:   Be careful      ⚠️

DIRECTION:
  LONG:    Buy opportunity
  SHORT:   Short opportunity
  NEUTRAL: Skip!

RISK LEVEL:
  LOW:    Good for beginners
  MEDIUM: Standard risk
  HIGH:   Experienced only

VOLUME RATIO:
  > 1.5x: Strong confirmation ✅
  < 1.0x: Weak signal ❌

WHEN TO TRADE:
  Best:  9:30-11:00 AM ET
  Good:  2:00-4:00 PM ET
  Avoid: 11:00 AM-2:00 PM ET

POSITION SIZING:
  Risk per trade:  2% of account
  Max per stock:   20% of account
  Stop loss:       2% below entry

═══════════════════════════════════════════════════════════
```

---

## 🚀 You're Ready!

You now know:
✅ When to run the screener
✅ How to read every piece of output
✅ How to set and adjust indicators
✅ Your complete daily workflow
✅ How to customize for your style

**Next Step**: Run the screener tomorrow morning and practice identifying opportunities!

Remember: Start small, trade smart, and never stop learning! 📈
