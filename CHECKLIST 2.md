# Day Trading Screener - Quick Reference Checklist

## 📋 Setup Checklist (5 minutes)

- [ ] Python 3.8+ installed
- [ ] Download all project files
- [ ] Run: `pip install -r requirements.txt`
- [ ] Test: `python config.py` (should show config without errors)
- [ ] Test run: `python day_trading_screener.py`

## 🎯 Daily Trading Checklist

### Pre-Market (Before 9:30 AM ET)

- [ ] Run market scan: `python day_trading_screener.py`
- [ ] Review top 15-20 opportunities
- [ ] Check confidence scores (focus on >70%)
- [ ] Run sentiment analysis on top picks (your agent)
- [ ] Create tiered watchlist:
  - [ ] Tier 1: Confidence >80%
  - [ ] Tier 2: Confidence 60-79%
  - [ ] Tier 3: Watch only
- [ ] Set up charts for Tier 1 stocks
- [ ] Prepare entry/exit plans
- [ ] Set price alerts

### During Market Hours

- [ ] 9:30 AM: Monitor market open
- [ ] 10:00 AM: Re-scan watchlist
- [ ] 11:00 AM: Check signals (best time window closing)
- [ ] 12:00 PM: Mid-day review
- [ ] 2:00 PM: Afternoon session scan
- [ ] 3:30 PM: Final hour positioning
- [ ] 4:00 PM: Market close review

### Post-Market

- [ ] Review executed trades
- [ ] Update trading journal
- [ ] Note what worked/didn't work
- [ ] Adjust config if needed
- [ ] Prepare for next day

## ⚙️ Configuration Checklist

Before first use, verify in `config.py`:

- [ ] MIN_PRICE appropriate for your capital
- [ ] MAX_PRICE set correctly
- [ ] MIN_VOLUME matches your liquidity needs
- [ ] RSI_PERIOD (default 14 is good)
- [ ] Confidence weights match your style
- [ ] Risk thresholds appropriate
- [ ] Stock universe suitable

## 🔍 Analysis Checklist (Per Stock)

When analyzing a stock opportunity:

- [ ] Confidence score >70%
- [ ] Clear direction (LONG or SHORT, not NEUTRAL)
- [ ] Volume ratio >1.2x
- [ ] Risk level acceptable for position size
- [ ] RSI not extreme (avoid >85 or <15)
- [ ] MACD aligned with direction
- [ ] Price position vs VWAP makes sense
- [ ] Recent momentum supports direction
- [ ] Sentiment confirms (if available)
- [ ] Overall market trend aligned

## 💰 Risk Management Checklist

Before entering any trade:

- [ ] Position size calculated (max 20% portfolio)
- [ ] Stop loss set (typically 2% below entry)
- [ ] Risk amount acceptable (max 2% account)
- [ ] Risk/reward ratio >1.5:1
- [ ] Don't have too many correlated positions
- [ ] Haven't hit daily loss limit
- [ ] Haven't exceeded max daily trades
- [ ] Have clear exit plan

## 🚨 Warning Signs Checklist

Skip the trade if:

- [ ] Confidence <60%
- [ ] Direction is NEUTRAL
- [ ] Volume ratio <1.0 (low activity)
- [ ] Risk level is HIGH (unless you're experienced)
- [ ] Signals are conflicting
- [ ] Going against market trend
- [ ] Stock news you're unaware of
- [ ] Your sentiment shows opposite direction
- [ ] You're unsure or uncomfortable
- [ ] You're trading emotionally

## 📊 Integration Checklist (with Sentiment Agent)

For each opportunity:

- [ ] Get technical score from screener
- [ ] Get sentiment score from your agent
- [ ] Combine: `(technical * 0.7) + (sentiment * 0.3)`
- [ ] Verify scores align (both positive or both negative)
- [ ] If conflicting, dig deeper or skip
- [ ] Higher combined score = higher confidence
- [ ] Document reasoning

## 🛠️ Troubleshooting Checklist

If something's wrong:

- [ ] Check internet connection
- [ ] Verify yfinance is working: `python -c "import yfinance"`
- [ ] Check if market is open
- [ ] Verify ticker symbols are correct
- [ ] Check rate limits not exceeded
- [ ] Lower volume threshold if no results
- [ ] Try smaller stock universe for testing
- [ ] Check config.py has no errors
- [ ] Update dependencies: `pip install -r requirements.txt --upgrade`
- [ ] Review error messages carefully

## 📈 Performance Tracking Checklist

Weekly review:

- [ ] Win rate % (target: >50%)
- [ ] Average R:R (target: >1.5)
- [ ] Best performing confidence levels
- [ ] Best performing indicators
- [ ] Best performing timeframes
- [ ] Risk level vs success rate
- [ ] Types of stocks that work best
- [ ] Adjust config based on learnings

## 🎓 Learning Checklist

Continuous improvement:

- [ ] Read README.md completely
- [ ] Try all examples in examples.py
- [ ] Understand each indicator's purpose
- [ ] Paper trade before real money
- [ ] Keep trading journal
- [ ] Review winners and losers
- [ ] Adjust strategy based on results
- [ ] Stay updated on market conditions
- [ ] Learn from mistakes
- [ ] Never stop improving

## 📝 Quick Commands Reference

```bash
# Basic scan
python day_trading_screener.py

# Interactive examples
python examples.py

# Check configuration
python config.py

# Analyze specific stocks (edit examples.py)
# watchlist = ['AAPL', 'TSLA', 'NVDA']

# Update dependencies
pip install -r requirements.txt --upgrade
```

## 🎯 Success Metrics

Your trading should show:

- [ ] Positive win rate (>50%)
- [ ] Positive profit factor
- [ ] Controlled drawdowns (<10%)
- [ ] Consistent execution
- [ ] Emotional discipline
- [ ] Continuous learning

## ⚠️ Red Flags - Stop Trading If:

- [ ] Emotions taking over
- [ ] Revenge trading after loss
- [ ] Ignoring stop losses
- [ ] Over-leveraging
- [ ] Trading without plan
- [ ] Hitting daily loss limit
- [ ] Not understanding the trade
- [ ] Chasing moves
- [ ] Fighting the trend
- [ ] Fatigue or stress

## 💡 Best Practices

Always:

- [ ] Use stop losses
- [ ] Size positions appropriately
- [ ] Trade with the trend
- [ ] Wait for high-confidence setups
- [ ] Keep emotions in check
- [ ] Document all trades
- [ ] Review and learn
- [ ] Stay disciplined
- [ ] Manage risk first
- [ ] Focus on process, not profits

---

## Quick Start Command

```bash
python day_trading_screener.py
```

## Files to Know

- `QUICKSTART.md` - Get started in 5 minutes
- `README.md` - Complete documentation
- `ARCHITECTURE.md` - How it works
- `examples.py` - Usage examples
- `config.py` - Customize settings

---

**Remember**: Consistency beats complexity. Master the basics before adding advanced features!

Good luck! 🚀
