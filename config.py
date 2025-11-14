"""
Configuration file for Day Trading Screener
Customize these settings to match your trading style
"""

# =============================================================================
# FILTERING CRITERIA
# =============================================================================

# Price range for stocks to scan
MIN_PRICE = 5.0          # Minimum stock price ($)
MAX_PRICE = 500.0        # Maximum stock price ($)

# Volume requirements
MIN_VOLUME = 1_000_000   # Minimum average daily volume

# Minimum confidence score to report (0-100)
MIN_CONFIDENCE_SCORE = 50

# =============================================================================
# DATA FETCHING
# =============================================================================

# Time periods for data fetching
DATA_PERIOD = "5d"       # Options: "1d", "5d", "1mo"
DATA_INTERVAL = "5m"     # Options: "1m", "5m", "15m", "30m", "1h"

# Number of top stocks to return
TOP_N_STOCKS = 20

# =============================================================================
# TECHNICAL INDICATORS
# =============================================================================

# RSI settings
RSI_PERIOD = 14
RSI_OVERSOLD = 30        # Buy signal threshold
RSI_OVERBOUGHT = 70      # Sell signal threshold

# MACD settings
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# Bollinger Bands settings
BB_PERIOD = 20
BB_STD_DEV = 2

# Moving averages
SMA_SHORT = 9
SMA_LONG = 20
EMA_SHORT = 9
EMA_LONG = 20

# ATR settings
ATR_PERIOD = 14

# Volume settings
VOLUME_PERIOD = 20
HIGH_VOLUME_THRESHOLD = 1.5  # Multiple of average volume

# Stochastic Oscillator (Advanced)
STOCH_PERIOD = 14
STOCH_OVERSOLD = 20
STOCH_OVERBOUGHT = 80

# ADX settings (Advanced)
ADX_PERIOD = 14
ADX_STRONG_TREND = 25    # Threshold for strong trend

# MFI settings (Advanced)
MFI_PERIOD = 14
MFI_OVERSOLD = 20
MFI_OVERBOUGHT = 80

# =============================================================================
# CONFIDENCE SCORE WEIGHTS
# =============================================================================

# Adjust these weights to emphasize certain indicators (must sum to ~1.0)
CONFIDENCE_WEIGHTS = {
    'rsi_signal': 0.15,
    'macd_signal': 0.20,
    'bb_signal': 0.10,
    'vwap_signal': 0.20,
    'ma_signal': 0.15,
    'volume_signal': 0.10,
    'momentum_signal': 0.10
}

# Bonus multipliers
BB_SQUEEZE_BONUS = 1.10      # 10% bonus for BB squeeze
SIGNAL_ALIGNMENT_BONUS = 1.20  # 20% bonus when signals align

# =============================================================================
# RISK ASSESSMENT
# =============================================================================

# Volatility thresholds (% based on ATR/Close)
LOW_VOLATILITY = 2.0
HIGH_VOLATILITY = 5.0

# Volume thresholds
LOW_VOLUME_RATIO = 1.2
HIGH_VOLUME_RATIO = 2.5

# Beta thresholds
LOW_BETA = 1.2
HIGH_BETA = 1.5

# =============================================================================
# STOCK UNIVERSE
# =============================================================================

# Use default universe or custom list
USE_CUSTOM_UNIVERSE = False

# Custom stock universe (only used if USE_CUSTOM_UNIVERSE = True)
CUSTOM_UNIVERSE = [
    # Add your preferred stocks here
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA',
    'TSLA', 'META', 'AMD', 'INTC', 'NFLX'
]

# =============================================================================
# MACHINE LEARNING SETTINGS (Advanced)
# =============================================================================

USE_ML = False           # Enable/disable ML predictions
ML_MIN_TRAINING_SAMPLES = 100

# ML model parameters
ML_N_ESTIMATORS = 100
ML_MAX_DEPTH = 10
ML_TEST_SIZE = 0.2
ML_RANDOM_STATE = 42

# ML weight in final confidence score
ML_WEIGHT = 0.3

# =============================================================================
# OUTPUT SETTINGS
# =============================================================================

# File output
SAVE_TO_CSV = True
OUTPUT_DIRECTORY = "."
OUTPUT_FILENAME_PREFIX = "day_trading_opportunities"

# Console output
SHOW_PROGRESS = True
VERBOSE = True

# Report format
INCLUDE_TECHNICAL_DETAILS = True
INCLUDE_DISCLAIMER = True

# =============================================================================
# TRADING RULES (Educational - Not Implemented)
# =============================================================================

# These are reference values for your trading plan
MAX_POSITION_SIZE = 0.20     # Max 20% of portfolio per position
MAX_RISK_PER_TRADE = 0.02    # Max 2% risk per trade
STOP_LOSS_PERCENTAGE = 0.02  # 2% stop loss
MAX_DAILY_TRADES = 5         # Maximum trades per day
MAX_DAILY_LOSS = 0.06        # Stop trading at 6% daily loss

# =============================================================================
# TIME SETTINGS
# =============================================================================

# Market hours (ET)
MARKET_OPEN_HOUR = 9
MARKET_OPEN_MINUTE = 30
MARKET_CLOSE_HOUR = 16
MARKET_CLOSE_MINUTE = 0

# Best trading times (for reference)
BEST_TRADING_START = (9, 30)   # 9:30 AM ET
BEST_TRADING_END = (11, 0)     # 11:00 AM ET
AFTERNOON_START = (14, 0)      # 2:00 PM ET
AFTERNOON_END = (16, 0)        # 4:00 PM ET

# =============================================================================
# SENTIMENT ANALYSIS (Optional Integration)
# =============================================================================

USE_SENTIMENT = False
SENTIMENT_WEIGHT = 0.3       # Weight of sentiment in final score
SENTIMENT_API_KEY = None     # Add your API key if using sentiment

# =============================================================================
# ADVANCED FEATURES
# =============================================================================

# Multi-timeframe analysis
USE_MULTI_TIMEFRAME = False
TIMEFRAMES = ['5m', '15m', '1h']

# Pattern recognition
ENABLE_PATTERN_DETECTION = False

# Alert settings
ENABLE_ALERTS = False
ALERT_CONFIDENCE_THRESHOLD = 80
ALERT_METHOD = "console"     # Options: "console", "email", "discord", "slack"

# =============================================================================
# VALIDATION RULES
# =============================================================================

# Validate configuration values
def validate_config():
    """Validate configuration settings"""
    errors = []
    
    if MIN_PRICE < 0:
        errors.append("MIN_PRICE must be positive")
    
    if MIN_PRICE >= MAX_PRICE:
        errors.append("MIN_PRICE must be less than MAX_PRICE")
    
    if MIN_VOLUME < 0:
        errors.append("MIN_VOLUME must be positive")
    
    if not 0 <= MIN_CONFIDENCE_SCORE <= 100:
        errors.append("MIN_CONFIDENCE_SCORE must be between 0 and 100")
    
    weight_sum = sum(CONFIDENCE_WEIGHTS.values())
    if not 0.95 <= weight_sum <= 1.05:
        errors.append(f"CONFIDENCE_WEIGHTS must sum to ~1.0 (currently {weight_sum:.2f})")
    
    if DATA_INTERVAL not in ['1m', '5m', '15m', '30m', '1h']:
        errors.append(f"Invalid DATA_INTERVAL: {DATA_INTERVAL}")
    
    if errors:
        print("Configuration Errors:")
        for error in errors:
            print(f"  ❌ {error}")
        return False
    
    return True

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_config_summary():
    """Get a summary of current configuration"""
    summary = f"""
    Day Trading Screener Configuration
    ===================================
    
    Filtering:
      - Price Range: ${MIN_PRICE:.2f} - ${MAX_PRICE:.2f}
      - Min Volume: {MIN_VOLUME:,}
      - Min Confidence: {MIN_CONFIDENCE_SCORE}%
    
    Data:
      - Period: {DATA_PERIOD}
      - Interval: {DATA_INTERVAL}
      - Top N Stocks: {TOP_N_STOCKS}
    
    Technical Indicators:
      - RSI Period: {RSI_PERIOD} (Oversold: {RSI_OVERSOLD}, Overbought: {RSI_OVERBOUGHT})
      - MACD: {MACD_FAST}/{MACD_SLOW}/{MACD_SIGNAL}
      - Bollinger Bands: {BB_PERIOD} period, {BB_STD_DEV} std dev
    
    Features:
      - Machine Learning: {'Enabled' if USE_ML else 'Disabled'}
      - Sentiment Analysis: {'Enabled' if USE_SENTIMENT else 'Disabled'}
      - Multi-Timeframe: {'Enabled' if USE_MULTI_TIMEFRAME else 'Disabled'}
      - Custom Universe: {'Enabled' if USE_CUSTOM_UNIVERSE else 'Disabled'}
    
    Output:
      - Save to CSV: {'Yes' if SAVE_TO_CSV else 'No'}
      - Verbose: {'Yes' if VERBOSE else 'No'}
    """
    return summary

def print_config():
    """Print current configuration"""
    if validate_config():
        print(get_config_summary())
    else:
        print("\n⚠️  Configuration has errors. Please fix them before running.")

# =============================================================================
# USAGE
# =============================================================================

if __name__ == "__main__":
    print_config()
