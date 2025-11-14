"""
Day Trading Stock Screener
Analyzes US stocks and provides day trading recommendations with confidence scores
Now automatically scans all S&P 500 stocks!
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import warnings
warnings.filterwarnings('ignore')

# Try to import cached S&P 500 list
try:
    from sp500_cached_list import get_cached_sp500
    HAS_CACHED_SP500 = True
except ImportError:
    HAS_CACHED_SP500 = False

class DayTradingScreener:
    """
    Main class for screening stocks for day trading opportunities
    """
    
    def __init__(self, min_price: float = 5.0, max_price: float = 500.0, 
                 min_volume: int = 1000000):
        """
        Initialize the screener with filtering criteria
        
        Args:
            min_price: Minimum stock price to consider
            max_price: Maximum stock price to consider
            min_volume: Minimum average volume required
        """
        self.min_price = min_price
        self.max_price = max_price
        self.min_volume = min_volume
        self.sp500_tickers = None  # Cache S&P 500 list
        
    def fetch_sp500_tickers(self) -> List[str]:
        """
        Fetch current S&P 500 stock tickers from Wikipedia
        
        Returns:
            List of S&P 500 stock tickers
        """
        if self.sp500_tickers is not None:
            return self.sp500_tickers
            
        try:
            print("Fetching S&P 500 stock list from Wikipedia...")
            
            # Read S&P 500 list from Wikipedia
            url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
            tables = pd.read_html(url)
            
            # First table contains the S&P 500 companies
            sp500_table = tables[0]
            
            # Extract ticker symbols
            tickers = sp500_table['Symbol'].tolist()
            
            # Clean tickers (remove any newlines or extra characters)
            tickers = [ticker.replace('\n', '').strip() for ticker in tickers]
            
            # Some tickers may have class distinctions (like BRK.B, BF.B)
            # These are already in the correct format for yfinance
            
            self.sp500_tickers = tickers
            
            print(f"✅ Successfully fetched {len(tickers)} S&P 500 stocks")
            print(f"   Sample: {', '.join(tickers[:5])}...")
            
            return tickers
            
        except Exception as e:
            print(f"⚠️  Could not fetch from Wikipedia: {str(e)[:100]}")
            
            # Try cached list as first fallback
            if HAS_CACHED_SP500:
                try:
                    print("   Using cached S&P 500 list...")
                    tickers = get_cached_sp500()
                    self.sp500_tickers = tickers
                    print(f"✅ Loaded {len(tickers)} stocks from cached S&P 500 list")
                    return tickers
                except Exception as cache_error:
                    print(f"   Cache error: {cache_error}")
            
            # Final fallback to default universe
            print("   Falling back to default stock universe (60 stocks)...")
            return self._get_default_universe()
    
    def _get_default_universe(self) -> List[str]:
        """
        Fallback default stock universe if S&P 500 fetch fails
        
        Returns:
            List of default stock tickers
        """
        return [
            # Tech
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA', 'AMD', 'INTC',
            # Finance
            'JPM', 'BAC', 'WFC', 'GS', 'MS', 'C',
            # Energy
            'XOM', 'CVX', 'COP', 'SLB',
            # Consumer
            'WMT', 'HD', 'MCD', 'NKE', 'SBUX',
            # Healthcare
            'JNJ', 'PFE', 'UNH', 'ABBV', 'MRK',
            # Popular day trading stocks
            'SPY', 'QQQ', 'PLTR', 'SOFI', 'RIVN', 'LCID', 'F', 'GM',
            'BA', 'DIS', 'NFLX', 'PYPL', 'SQ', 'COIN', 'ROKU',
        ]
        
    def get_stock_universe(self, custom_tickers: List[str] = None) -> List[str]:
        """
        Get list of stocks to analyze
        
        Args:
            custom_tickers: Optional list of specific tickers to analyze
            
        Returns:
            List of stock tickers
        """
        if custom_tickers:
            print(f"Using custom stock list: {len(custom_tickers)} stocks")
            return custom_tickers
        
        # Default: Fetch all S&P 500 stocks
        return self.fetch_sp500_tickers()
    
    def fetch_stock_data(self, ticker: str, period: str = "5d", 
                        interval: str = "5m") -> pd.DataFrame:
        """
        Fetch intraday stock data
        
        Args:
            ticker: Stock ticker symbol
            period: Data period (1d, 5d, 1mo)
            interval: Data interval (1m, 5m, 15m, 1h)
            
        Returns:
            DataFrame with OHLCV data
        """
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period=period, interval=interval)
            
            if df.empty:
                return None
                
            return df
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return None
    
    def calculate_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate key technical indicators for day trading
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            DataFrame with added technical indicators
        """
        if df is None or df.empty:
            return None
        
        # RSI (Relative Strength Index)
        df = self._calculate_rsi(df, period=14)
        
        # MACD
        df = self._calculate_macd(df)
        
        # Bollinger Bands
        df = self._calculate_bollinger_bands(df, period=20)
        
        # VWAP (Volume Weighted Average Price)
        df = self._calculate_vwap(df)
        
        # Moving Averages
        df['SMA_9'] = df['Close'].rolling(window=9).mean()
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['EMA_9'] = df['Close'].ewm(span=9, adjust=False).mean()
        df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
        
        # Volume analysis
        df['Volume_SMA'] = df['Volume'].rolling(window=20).mean()
        df['Volume_Ratio'] = df['Volume'] / df['Volume_SMA']
        
        # Average True Range (ATR) for volatility
        df = self._calculate_atr(df, period=14)
        
        return df
    
    def _calculate_rsi(self, df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """Calculate RSI indicator"""
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        return df
    
    def _calculate_macd(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate MACD indicator"""
        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        
        df['MACD'] = exp1 - exp2
        df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']
        
        return df
    
    def _calculate_bollinger_bands(self, df: pd.DataFrame, 
                                   period: int = 20) -> pd.DataFrame:
        """Calculate Bollinger Bands"""
        df['BB_Middle'] = df['Close'].rolling(window=period).mean()
        bb_std = df['Close'].rolling(window=period).std()
        
        df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
        df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
        df['BB_Width'] = (df['BB_Upper'] - df['BB_Lower']) / df['BB_Middle']
        
        return df
    
    def _calculate_vwap(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate VWAP"""
        df['Typical_Price'] = (df['High'] + df['Low'] + df['Close']) / 3
        df['VWAP'] = (df['Typical_Price'] * df['Volume']).cumsum() / df['Volume'].cumsum()
        
        return df
    
    def _calculate_atr(self, df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """Calculate Average True Range"""
        high_low = df['High'] - df['Low']
        high_close = np.abs(df['High'] - df['Close'].shift())
        low_close = np.abs(df['Low'] - df['Close'].shift())
        
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        df['ATR'] = true_range.rolling(period).mean()
        
        return df
    
    def analyze_stock(self, ticker: str) -> Dict:
        """
        Perform complete analysis on a single stock
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Dictionary with analysis results
        """
        # Fetch data
        df = self.fetch_stock_data(ticker, period="5d", interval="5m")
        
        if df is None or df.empty or len(df) < 50:
            return None
        
        # Calculate indicators
        df = self.calculate_technical_indicators(df)
        
        if df is None:
            return None
        
        # Get latest values
        latest = df.iloc[-1]
        prev = df.iloc[-2] if len(df) > 1 else latest
        
        # Get current price and volume info
        current_price = latest['Close']
        current_volume = latest['Volume']
        avg_volume = df['Volume'].mean()
        
        # Filter by price and volume
        if current_price < self.min_price or current_price > self.max_price:
            return None
        
        if avg_volume < self.min_volume:
            return None
        
        # Calculate signals and scores
        analysis = {
            'ticker': ticker,
            'current_price': round(current_price, 2),
            'price_change_pct': round(((current_price - df.iloc[0]['Close']) / 
                                      df.iloc[0]['Close']) * 100, 2),
        }
        
        # Technical signals
        signals = self._generate_signals(df, latest, prev)
        analysis.update(signals)
        
        # Calculate confidence score and predicted move
        analysis['confidence_score'] = self._calculate_confidence_score(signals)
        analysis['predicted_move_pct'] = self._predict_price_move(df, signals)
        analysis['trade_direction'] = self._determine_direction(signals)
        analysis['risk_level'] = self._calculate_risk_level(df, latest)
        
        return analysis
    
    def _generate_signals(self, df: pd.DataFrame, latest: pd.Series, 
                         prev: pd.Series) -> Dict:
        """
        Generate trading signals from technical indicators
        
        Returns:
            Dictionary of signal scores
        """
        signals = {}
        
        # RSI signals
        if pd.notna(latest['RSI']):
            if latest['RSI'] < 30:
                signals['rsi_signal'] = 1  # Oversold - bullish
            elif latest['RSI'] > 70:
                signals['rsi_signal'] = -1  # Overbought - bearish
            else:
                signals['rsi_signal'] = 0  # Neutral
            signals['rsi_value'] = round(latest['RSI'], 2)
        else:
            signals['rsi_signal'] = 0
            signals['rsi_value'] = None
        
        # MACD signals
        if pd.notna(latest['MACD']) and pd.notna(latest['MACD_Signal']):
            if latest['MACD'] > latest['MACD_Signal'] and prev['MACD'] <= prev['MACD_Signal']:
                signals['macd_signal'] = 1  # Bullish crossover
            elif latest['MACD'] < latest['MACD_Signal'] and prev['MACD'] >= prev['MACD_Signal']:
                signals['macd_signal'] = -1  # Bearish crossover
            elif latest['MACD'] > latest['MACD_Signal']:
                signals['macd_signal'] = 0.5  # Bullish
            elif latest['MACD'] < latest['MACD_Signal']:
                signals['macd_signal'] = -0.5  # Bearish
            else:
                signals['macd_signal'] = 0
        else:
            signals['macd_signal'] = 0
        
        # Bollinger Bands signals
        if pd.notna(latest['BB_Upper']) and pd.notna(latest['BB_Lower']):
            if latest['Close'] <= latest['BB_Lower']:
                signals['bb_signal'] = 1  # At lower band - potential bounce
            elif latest['Close'] >= latest['BB_Upper']:
                signals['bb_signal'] = -1  # At upper band - potential pullback
            else:
                signals['bb_signal'] = 0
            
            # BB squeeze (low volatility - potential breakout)
            signals['bb_width'] = round(latest['BB_Width'], 4)
            if latest['BB_Width'] < df['BB_Width'].quantile(0.2):
                signals['bb_squeeze'] = True
            else:
                signals['bb_squeeze'] = False
        else:
            signals['bb_signal'] = 0
            signals['bb_squeeze'] = False
        
        # VWAP signals
        if pd.notna(latest['VWAP']):
            if latest['Close'] > latest['VWAP']:
                signals['vwap_signal'] = 1  # Above VWAP - bullish
            elif latest['Close'] < latest['VWAP']:
                signals['vwap_signal'] = -1  # Below VWAP - bearish
            else:
                signals['vwap_signal'] = 0
            signals['vwap_distance'] = round(((latest['Close'] - latest['VWAP']) / 
                                             latest['VWAP']) * 100, 2)
        else:
            signals['vwap_signal'] = 0
        
        # Moving average signals
        if pd.notna(latest['EMA_9']) and pd.notna(latest['EMA_20']):
            if latest['EMA_9'] > latest['EMA_20']:
                signals['ma_signal'] = 1  # Bullish trend
            elif latest['EMA_9'] < latest['EMA_20']:
                signals['ma_signal'] = -1  # Bearish trend
            else:
                signals['ma_signal'] = 0
        else:
            signals['ma_signal'] = 0
        
        # Volume signals
        if pd.notna(latest['Volume_Ratio']):
            if latest['Volume_Ratio'] > 1.5:
                signals['volume_signal'] = 1  # High volume
            elif latest['Volume_Ratio'] > 1.2:
                signals['volume_signal'] = 0.5  # Above average
            else:
                signals['volume_signal'] = 0
            signals['volume_ratio'] = round(latest['Volume_Ratio'], 2)
        else:
            signals['volume_signal'] = 0
        
        # Momentum (recent price action)
        recent_data = df.tail(20)
        if len(recent_data) >= 20:
            price_momentum = ((latest['Close'] - recent_data.iloc[0]['Close']) / 
                            recent_data.iloc[0]['Close']) * 100
            signals['momentum_pct'] = round(price_momentum, 2)
            
            if price_momentum > 2:
                signals['momentum_signal'] = 1
            elif price_momentum < -2:
                signals['momentum_signal'] = -1
            else:
                signals['momentum_signal'] = 0
        else:
            signals['momentum_signal'] = 0
        
        return signals
    
    def _calculate_confidence_score(self, signals: Dict) -> float:
        """
        Calculate overall confidence score (0-100)
        
        Args:
            signals: Dictionary of technical signals
            
        Returns:
            Confidence score
        """
        # Weighted signal scoring
        weights = {
            'rsi_signal': 0.15,
            'macd_signal': 0.20,
            'bb_signal': 0.10,
            'vwap_signal': 0.20,
            'ma_signal': 0.15,
            'volume_signal': 0.10,
            'momentum_signal': 0.10
        }
        
        # Calculate weighted sum of absolute signal values
        total_score = 0
        max_possible = 0
        
        for signal_name, weight in weights.items():
            if signal_name in signals:
                # Normalize signal to 0-1 range
                signal_value = abs(signals[signal_name])
                total_score += signal_value * weight
                max_possible += weight
        
        # Convert to 0-100 scale
        if max_possible > 0:
            confidence = (total_score / max_possible) * 100
        else:
            confidence = 0
        
        # Bonus for signal alignment (all pointing same direction)
        signal_values = [signals.get(k, 0) for k in weights.keys() if k in signals]
        if signal_values:
            if all(s > 0 for s in signal_values if s != 0) or \
               all(s < 0 for s in signal_values if s != 0):
                confidence = min(100, confidence * 1.2)  # 20% bonus
        
        # Bonus for BB squeeze (volatility expansion expected)
        if signals.get('bb_squeeze', False):
            confidence = min(100, confidence * 1.1)  # 10% bonus
        
        return round(confidence, 2)
    
    def _predict_price_move(self, df: pd.DataFrame, signals: Dict) -> float:
        """
        Predict potential price movement percentage
        
        Args:
            df: Historical data
            signals: Technical signals
            
        Returns:
            Predicted percentage move
        """
        latest = df.iloc[-1]
        
        # Base prediction on ATR (volatility)
        if pd.notna(latest['ATR']):
            atr_pct = (latest['ATR'] / latest['Close']) * 100
        else:
            # Fallback to recent volatility
            recent_volatility = df['Close'].tail(20).std() / df['Close'].tail(20).mean() * 100
            atr_pct = recent_volatility
        
        # Adjust based on signal strength
        signal_sum = sum([
            signals.get('rsi_signal', 0),
            signals.get('macd_signal', 0),
            signals.get('bb_signal', 0),
            signals.get('vwap_signal', 0),
            signals.get('ma_signal', 0),
            signals.get('momentum_signal', 0)
        ])
        
        # Scale prediction
        if signal_sum > 0:
            direction = 1
        elif signal_sum < 0:
            direction = -1
        else:
            direction = 0
        
        # Predicted move is ATR-based with signal strength multiplier
        signal_strength = abs(signal_sum) / 6  # Normalize to 0-1
        predicted_move = direction * atr_pct * (0.5 + signal_strength * 0.5)
        
        # Volume amplification
        if signals.get('volume_signal', 0) > 0:
            predicted_move *= 1.2
        
        return round(predicted_move, 2)
    
    def _determine_direction(self, signals: Dict) -> str:
        """Determine trade direction (LONG/SHORT/NEUTRAL)"""
        signal_sum = sum([
            signals.get('rsi_signal', 0),
            signals.get('macd_signal', 0),
            signals.get('bb_signal', 0),
            signals.get('vwap_signal', 0),
            signals.get('ma_signal', 0),
            signals.get('momentum_signal', 0)
        ])
        
        if signal_sum > 1:
            return 'LONG'
        elif signal_sum < -1:
            return 'SHORT'
        else:
            return 'NEUTRAL'
    
    def _calculate_risk_level(self, df: pd.DataFrame, latest: pd.Series) -> str:
        """Calculate risk level (LOW/MEDIUM/HIGH)"""
        # Based on volatility and volume
        if pd.notna(latest['ATR']):
            volatility = (latest['ATR'] / latest['Close']) * 100
        else:
            volatility = df['Close'].tail(20).std() / df['Close'].tail(20).mean() * 100
        
        volume_ratio = latest.get('Volume_Ratio', 1.0)
        
        # Combined risk score
        if volatility < 2 and volume_ratio < 1.5:
            return 'LOW'
        elif volatility > 5 or volume_ratio > 2.5:
            return 'HIGH'
        else:
            return 'MEDIUM'
    
    def scan_all_stocks(self, custom_tickers: List[str] = None, 
                       top_n: int = 20) -> pd.DataFrame:
        """
        Scan all stocks and return top opportunities
        
        Args:
            custom_tickers: Optional list of specific tickers
            top_n: Number of top stocks to return
            
        Returns:
            DataFrame with ranked opportunities
        """
        universe = self.get_stock_universe(custom_tickers)
        results = []
        
        total_stocks = len(universe)
        print(f"\n{'='*80}")
        print(f"🔍 SCANNING {total_stocks} STOCKS FOR DAY TRADING OPPORTUNITIES")
        print(f"{'='*80}\n")
        
        start_time = datetime.now()
        
        for i, ticker in enumerate(universe):
            # Progress indicator every 25 stocks
            if (i + 1) % 25 == 0 or i == 0:
                elapsed = (datetime.now() - start_time).seconds
                stocks_per_sec = (i + 1) / max(elapsed, 1)
                remaining = (total_stocks - i - 1) / max(stocks_per_sec, 0.1)
                print(f"Progress: {i + 1}/{total_stocks} stocks "
                      f"({((i+1)/total_stocks*100):.1f}%) - "
                      f"~{int(remaining/60)}min {int(remaining%60)}sec remaining")
            
            analysis = self.analyze_stock(ticker)
            
            if analysis:
                results.append(analysis)
        
        elapsed_time = (datetime.now() - start_time).seconds
        print(f"\n{'='*80}")
        print(f"✅ Scan Complete!")
        print(f"   Total time: {int(elapsed_time/60)}min {elapsed_time%60}sec")
        print(f"   Stocks analyzed: {total_stocks}")
        print(f"   Viable opportunities: {len(results)}")
        print(f"{'='*80}\n")
        
        if not results:
            print("⚠️  No trading opportunities found matching your criteria.")
            print("   Try adjusting filters in config.py (lower min_volume or min_price)")
            return pd.DataFrame()
        
        # Convert to DataFrame
        df = pd.DataFrame(results)
        
        # Sort by confidence score
        df = df.sort_values('confidence_score', ascending=False)
        
        # Return top N
        return df.head(top_n)
    
    def generate_report(self, results_df: pd.DataFrame) -> str:
        """
        Generate a formatted report of top opportunities
        
        Args:
            results_df: DataFrame with scan results
            
        Returns:
            Formatted report string
        """
        if results_df.empty:
            return "No trading opportunities found matching criteria."
        
        report = []
        report.append("=" * 80)
        report.append(f"DAY TRADING OPPORTUNITIES - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 80)
        report.append("")
        
        for idx, row in results_df.iterrows():
            report.append(f"#{idx + 1}. {row['ticker']} - ${row['current_price']}")
            report.append(f"   Direction: {row['trade_direction']}")
            report.append(f"   Confidence Score: {row['confidence_score']}/100")
            report.append(f"   Predicted Move: {row['predicted_move_pct']:+.2f}%")
            report.append(f"   Risk Level: {row['risk_level']}")
            report.append(f"   Day Change: {row['price_change_pct']:+.2f}%")
            
            if 'rsi_value' in row and pd.notna(row['rsi_value']):
                report.append(f"   RSI: {row['rsi_value']:.1f}")
            
            if 'volume_ratio' in row and pd.notna(row['volume_ratio']):
                report.append(f"   Volume Ratio: {row['volume_ratio']:.2f}x")
            
            report.append("")
        
        report.append("=" * 80)
        report.append("DISCLAIMER: This analysis is for informational purposes only.")
        report.append("Past performance does not guarantee future results.")
        report.append("=" * 80)
        
        return "\n".join(report)


def main():
    """Main execution function"""
    print("Initializing Day Trading Screener...")
    
    # Initialize screener
    screener = DayTradingScreener(
        min_price=5.0,
        max_price=500.0,
        min_volume=1000000
    )
    
    # You can specify custom tickers or use default universe
    # custom_tickers = ['AAPL', 'TSLA', 'NVDA', 'AMD', 'META']
    
    # Scan stocks
    results = screener.scan_all_stocks(custom_tickers=None, top_n=15)
    
    # Generate and print report
    if not results.empty:
        report = screener.generate_report(results)
        print(report)
        
        # Save to CSV
        output_file = f"day_trading_opportunities_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        results.to_csv(output_file, index=False)
        print(f"\nResults saved to: {output_file}")
    else:
        print("No trading opportunities found.")


if __name__ == "__main__":
    main()
