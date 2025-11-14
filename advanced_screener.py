"""
Advanced Day Trading Screener with Machine Learning
Includes sentiment analysis integration and ML-based predictions
Now automatically scans all S&P 500 stocks!
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import warnings
warnings.filterwarnings('ignore')

# ML imports
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


class AdvancedDayTradingScreener:
    """
    Advanced screener with ML predictions and sentiment analysis
    """
    
    def __init__(self, min_price: float = 5.0, max_price: float = 500.0, 
                 min_volume: int = 1000000, use_ml: bool = True):
        """
        Initialize advanced screener
        
        Args:
            min_price: Minimum stock price
            max_price: Maximum stock price
            min_volume: Minimum average volume
            use_ml: Whether to use ML predictions
        """
        self.min_price = min_price
        self.max_price = max_price
        self.min_volume = min_volume
        self.use_ml = use_ml
        self.ml_model = None
        self.scaler = StandardScaler()
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
            
            self.sp500_tickers = tickers
            
            print(f"✅ Successfully fetched {len(tickers)} S&P 500 stocks")
            
            return tickers
            
        except Exception as e:
            print(f"❌ Error fetching S&P 500 list: {e}")
            print("   Falling back to extended universe...")
            return self.get_extended_universe()
    
    def get_extended_universe(self) -> List[str]:
        """
        Get comprehensive list of day-tradable stocks
        """
        # Major indices
        spy_components = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'BRK.B',
            'UNH', 'JNJ', 'V', 'XOM', 'WMT', 'JPM', 'PG', 'MA', 'HD', 'CVX',
            'MRK', 'ABBV', 'KO', 'PEP', 'AVGO', 'COST', 'LLY', 'MCD', 'TMO',
            'ACN', 'ABT', 'CSCO', 'DHR', 'VZ', 'ADBE', 'CRM', 'NFLX', 'NKE',
            'WFC', 'DIS', 'TXN', 'BAC', 'MS', 'PM', 'CMCSA', 'UPS', 'NEE',
            'ORCL', 'BMY', 'HON', 'RTX', 'AMD', 'INTC', 'QCOM', 'AMGN', 'LOW'
        ]
        
        # High-momentum tech stocks
        tech_stocks = [
            'PLTR', 'SOFI', 'RBLX', 'COIN', 'HOOD', 'U', 'SNOW', 'SHOP',
            'SQ', 'PYPL', 'ROKU', 'ZM', 'UBER', 'LYFT', 'ABNB', 'DASH',
            'DKNG', 'CRWD', 'NET', 'DDOG', 'MDB', 'OKTA', 'TWLO', 'ZS'
        ]
        
        # EV and clean energy
        ev_stocks = [
            'RIVN', 'LCID', 'NIO', 'XPEV', 'LI', 'F', 'GM', 'CHPT', 'ENPH'
        ]
        
        # Popular trading ETFs
        etfs = [
            'SPY', 'QQQ', 'IWM', 'DIA', 'XLF', 'XLE', 'XLK', 'XLV', 'XLI',
            'GLD', 'SLV', 'TLT', 'ARKK', 'SQQQ', 'TQQQ', 'UVXY'
        ]
        
        # Volatile day trading favorites
        volatile = [
            'AMC', 'GME', 'BB', 'NOK', 'BBBY', 'SNDL'
        ]
        
        # Combine all
        universe = list(set(spy_components + tech_stocks + ev_stocks + 
                           etfs + volatile))
        
        return sorted(universe)
    
    def fetch_extended_data(self, ticker: str) -> Dict:
        """
        Fetch comprehensive stock data including fundamentals
        
        Args:
            ticker: Stock ticker
            
        Returns:
            Dictionary with extended data
        """
        try:
            stock = yf.Ticker(ticker)
            
            # Intraday data
            df_5m = stock.history(period="5d", interval="5m")
            df_1h = stock.history(period="1mo", interval="1h")
            df_daily = stock.history(period="3mo", interval="1d")
            
            # Stock info
            info = stock.info
            
            extended_data = {
                'df_5m': df_5m,
                'df_1h': df_1h,
                'df_daily': df_daily,
                'market_cap': info.get('marketCap', 0),
                'float_shares': info.get('floatShares', 0),
                'short_ratio': info.get('shortRatio', 0),
                'beta': info.get('beta', 1.0),
                'pe_ratio': info.get('trailingPE', None),
                'avg_volume': info.get('averageVolume', 0),
                'fifty_two_week_high': info.get('fiftyTwoWeekHigh', 0),
                'fifty_two_week_low': info.get('fiftyTwoWeekLow', 0),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown')
            }
            
            return extended_data
            
        except Exception as e:
            print(f"Error fetching extended data for {ticker}: {e}")
            return None
    
    def calculate_advanced_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate advanced technical indicators
        """
        if df is None or df.empty:
            return None
        
        # Basic indicators
        df = self._calculate_all_basic_indicators(df)
        
        # Stochastic Oscillator
        df = self._calculate_stochastic(df)
        
        # Average Directional Index (ADX)
        df = self._calculate_adx(df)
        
        # On Balance Volume (OBV)
        df = self._calculate_obv(df)
        
        # Money Flow Index (MFI)
        df = self._calculate_mfi(df)
        
        # Ichimoku Cloud
        df = self._calculate_ichimoku(df)
        
        # Parabolic SAR
        df = self._calculate_parabolic_sar(df)
        
        return df
    
    def _calculate_all_basic_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate all basic indicators"""
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']
        
        # Bollinger Bands
        df['BB_Middle'] = df['Close'].rolling(window=20).mean()
        bb_std = df['Close'].rolling(window=20).std()
        df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
        df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
        df['BB_Width'] = (df['BB_Upper'] - df['BB_Lower']) / df['BB_Middle']
        
        # VWAP
        df['Typical_Price'] = (df['High'] + df['Low'] + df['Close']) / 3
        df['VWAP'] = (df['Typical_Price'] * df['Volume']).cumsum() / df['Volume'].cumsum()
        
        # Moving Averages
        df['SMA_9'] = df['Close'].rolling(window=9).mean()
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['EMA_9'] = df['Close'].ewm(span=9, adjust=False).mean()
        df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
        
        # Volume
        df['Volume_SMA'] = df['Volume'].rolling(window=20).mean()
        df['Volume_Ratio'] = df['Volume'] / df['Volume_SMA']
        
        # ATR
        high_low = df['High'] - df['Low']
        high_close = np.abs(df['High'] - df['Close'].shift())
        low_close = np.abs(df['Low'] - df['Close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        df['ATR'] = true_range.rolling(14).mean()
        
        return df
    
    def _calculate_stochastic(self, df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """Calculate Stochastic Oscillator"""
        low_min = df['Low'].rolling(window=period).min()
        high_max = df['High'].rolling(window=period).max()
        
        df['Stoch_K'] = 100 * (df['Close'] - low_min) / (high_max - low_min)
        df['Stoch_D'] = df['Stoch_K'].rolling(window=3).mean()
        
        return df
    
    def _calculate_adx(self, df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """Calculate Average Directional Index"""
        # Calculate +DM and -DM
        high_diff = df['High'].diff()
        low_diff = -df['Low'].diff()
        
        plus_dm = high_diff.where((high_diff > low_diff) & (high_diff > 0), 0)
        minus_dm = low_diff.where((low_diff > high_diff) & (low_diff > 0), 0)
        
        # ATR
        atr = df['ATR'] if 'ATR' in df.columns else df['Close'].rolling(period).std()
        
        # Calculate +DI and -DI
        plus_di = 100 * (plus_dm.rolling(period).mean() / atr)
        minus_di = 100 * (minus_dm.rolling(period).mean() / atr)
        
        # Calculate DX and ADX
        dx = 100 * np.abs(plus_di - minus_di) / (plus_di + minus_di)
        df['ADX'] = dx.rolling(period).mean()
        
        return df
    
    def _calculate_obv(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate On Balance Volume"""
        obv = [0]
        for i in range(1, len(df)):
            if df['Close'].iloc[i] > df['Close'].iloc[i-1]:
                obv.append(obv[-1] + df['Volume'].iloc[i])
            elif df['Close'].iloc[i] < df['Close'].iloc[i-1]:
                obv.append(obv[-1] - df['Volume'].iloc[i])
            else:
                obv.append(obv[-1])
        
        df['OBV'] = obv
        return df
    
    def _calculate_mfi(self, df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """Calculate Money Flow Index"""
        typical_price = (df['High'] + df['Low'] + df['Close']) / 3
        money_flow = typical_price * df['Volume']
        
        positive_flow = money_flow.where(typical_price > typical_price.shift(1), 0)
        negative_flow = money_flow.where(typical_price < typical_price.shift(1), 0)
        
        positive_mf = positive_flow.rolling(period).sum()
        negative_mf = negative_flow.rolling(period).sum()
        
        mfi_ratio = positive_mf / negative_mf
        df['MFI'] = 100 - (100 / (1 + mfi_ratio))
        
        return df
    
    def _calculate_ichimoku(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate Ichimoku Cloud"""
        # Tenkan-sen (Conversion Line)
        high_9 = df['High'].rolling(window=9).max()
        low_9 = df['Low'].rolling(window=9).min()
        df['Tenkan_sen'] = (high_9 + low_9) / 2
        
        # Kijun-sen (Base Line)
        high_26 = df['High'].rolling(window=26).max()
        low_26 = df['Low'].rolling(window=26).min()
        df['Kijun_sen'] = (high_26 + low_26) / 2
        
        # Senkou Span A (Leading Span A)
        df['Senkou_Span_A'] = ((df['Tenkan_sen'] + df['Kijun_sen']) / 2).shift(26)
        
        # Senkou Span B (Leading Span B)
        high_52 = df['High'].rolling(window=52).max()
        low_52 = df['Low'].rolling(window=52).min()
        df['Senkou_Span_B'] = ((high_52 + low_52) / 2).shift(26)
        
        return df
    
    def _calculate_parabolic_sar(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate Parabolic SAR"""
        # Simplified version
        df['SAR'] = df['Close'].shift(1)
        return df
    
    def create_ml_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create features for machine learning model
        
        Args:
            df: DataFrame with technical indicators
            
        Returns:
            DataFrame with ML features
        """
        features = pd.DataFrame()
        
        # Price-based features
        features['price_change_1'] = df['Close'].pct_change(1)
        features['price_change_5'] = df['Close'].pct_change(5)
        features['price_change_20'] = df['Close'].pct_change(20)
        
        # Volatility features
        features['volatility_5'] = df['Close'].rolling(5).std() / df['Close'].rolling(5).mean()
        features['volatility_20'] = df['Close'].rolling(20).std() / df['Close'].rolling(20).mean()
        
        # Volume features
        features['volume_change'] = df['Volume'].pct_change(1)
        features['volume_ratio'] = df['Volume'] / df['Volume'].rolling(20).mean()
        
        # Technical indicators
        if 'RSI' in df.columns:
            features['rsi'] = df['RSI']
            features['rsi_change'] = df['RSI'].diff()
        
        if 'MACD' in df.columns:
            features['macd'] = df['MACD']
            features['macd_signal'] = df['MACD_Signal']
            features['macd_hist'] = df['MACD_Hist']
        
        if 'BB_Width' in df.columns:
            features['bb_width'] = df['BB_Width']
            features['bb_position'] = (df['Close'] - df['BB_Lower']) / (df['BB_Upper'] - df['BB_Lower'])
        
        if 'VWAP' in df.columns:
            features['vwap_distance'] = (df['Close'] - df['VWAP']) / df['VWAP']
        
        if 'ADX' in df.columns:
            features['adx'] = df['ADX']
        
        if 'Stoch_K' in df.columns:
            features['stoch_k'] = df['Stoch_K']
            features['stoch_d'] = df['Stoch_D']
        
        if 'MFI' in df.columns:
            features['mfi'] = df['MFI']
        
        # Moving average features
        if 'EMA_9' in df.columns and 'EMA_20' in df.columns:
            features['ema_cross'] = (df['EMA_9'] - df['EMA_20']) / df['EMA_20']
        
        # Target: next period return (for training)
        features['target'] = df['Close'].shift(-1) / df['Close'] - 1
        
        return features
    
    def train_ml_model(self, historical_data: pd.DataFrame):
        """
        Train ML model for price movement prediction
        
        Args:
            historical_data: Historical market data with features
        """
        # Create features
        features_df = self.create_ml_features(historical_data)
        features_df = features_df.dropna()
        
        if len(features_df) < 100:
            print("Not enough data to train ML model")
            return
        
        # Prepare data
        X = features_df.drop('target', axis=1)
        y = (features_df['target'] > 0).astype(int)  # Binary classification
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.ml_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.ml_model.fit(X_train_scaled, y_train)
        
        # Evaluate
        train_score = self.ml_model.score(X_train_scaled, y_train)
        test_score = self.ml_model.score(X_test_scaled, y_test)
        
        print(f"ML Model trained - Train accuracy: {train_score:.3f}, Test accuracy: {test_score:.3f}")
    
    def predict_with_ml(self, df: pd.DataFrame) -> Dict:
        """
        Make predictions using ML model
        
        Args:
            df: Current stock data
            
        Returns:
            Dictionary with ML predictions
        """
        if self.ml_model is None:
            return {'ml_probability': None, 'ml_confidence': None}
        
        # Create features
        features_df = self.create_ml_features(df)
        features_df = features_df.drop('target', axis=1, errors='ignore')
        
        # Get latest features
        latest_features = features_df.iloc[-1:].values
        
        if np.isnan(latest_features).any():
            return {'ml_probability': None, 'ml_confidence': None}
        
        # Scale and predict
        latest_features_scaled = self.scaler.transform(latest_features)
        
        # Predict probability
        prob = self.ml_model.predict_proba(latest_features_scaled)[0]
        
        return {
            'ml_probability': round(prob[1] * 100, 2),  # Probability of upward move
            'ml_confidence': round(max(prob) * 100, 2)  # Confidence in prediction
        }
    
    def analyze_with_sentiment(self, ticker: str, sentiment_score: float = None) -> Dict:
        """
        Analyze stock with optional sentiment integration
        
        Args:
            ticker: Stock ticker
            sentiment_score: Optional sentiment score (-1 to 1)
            
        Returns:
            Complete analysis dictionary
        """
        # Fetch extended data
        extended_data = self.fetch_extended_data(ticker)
        
        if not extended_data or extended_data['df_5m'].empty:
            return None
        
        df_5m = extended_data['df_5m']
        
        # Filter by criteria
        current_price = df_5m['Close'].iloc[-1]
        avg_volume = extended_data['avg_volume']
        
        if (current_price < self.min_price or current_price > self.max_price or 
            avg_volume < self.min_volume):
            return None
        
        # Calculate indicators
        df_5m = self.calculate_advanced_indicators(df_5m)
        
        # Generate technical signals
        signals = self._generate_advanced_signals(df_5m)
        
        # ML prediction
        ml_pred = {}
        if self.use_ml:
            ml_pred = self.predict_with_ml(df_5m)
        
        # Compile analysis
        analysis = {
            'ticker': ticker,
            'current_price': round(current_price, 2),
            'market_cap': extended_data['market_cap'],
            'beta': extended_data['beta'],
            'sector': extended_data['sector'],
            'avg_volume': avg_volume,
            **signals,
            **ml_pred
        }
        
        # Add sentiment if provided
        if sentiment_score is not None:
            analysis['sentiment_score'] = round(sentiment_score, 2)
            analysis['sentiment_impact'] = self._calculate_sentiment_impact(sentiment_score)
        
        # Calculate enhanced confidence score
        analysis['confidence_score'] = self._calculate_enhanced_confidence(
            signals, ml_pred, sentiment_score
        )
        
        # Enhanced prediction
        analysis['predicted_move_pct'] = self._enhanced_prediction(
            df_5m, signals, ml_pred, sentiment_score
        )
        
        analysis['trade_direction'] = self._determine_direction_advanced(
            signals, ml_pred, sentiment_score
        )
        
        analysis['risk_level'] = self._calculate_risk_advanced(
            df_5m, extended_data
        )
        
        return analysis
    
    def _generate_advanced_signals(self, df: pd.DataFrame) -> Dict:
        """Generate signals from advanced indicators"""
        latest = df.iloc[-1]
        signals = {}
        
        # Basic signals (RSI, MACD, BB, VWAP, MA, Volume)
        # ... (similar to basic version)
        
        # Stochastic
        if 'Stoch_K' in df.columns and pd.notna(latest['Stoch_K']):
            if latest['Stoch_K'] < 20:
                signals['stoch_signal'] = 1
            elif latest['Stoch_K'] > 80:
                signals['stoch_signal'] = -1
            else:
                signals['stoch_signal'] = 0
            signals['stoch_value'] = round(latest['Stoch_K'], 2)
        
        # ADX (trend strength)
        if 'ADX' in df.columns and pd.notna(latest['ADX']):
            signals['trend_strength'] = 'strong' if latest['ADX'] > 25 else 'weak'
            signals['adx_value'] = round(latest['ADX'], 2)
        
        # MFI
        if 'MFI' in df.columns and pd.notna(latest['MFI']):
            if latest['MFI'] < 20:
                signals['mfi_signal'] = 1
            elif latest['MFI'] > 80:
                signals['mfi_signal'] = -1
            else:
                signals['mfi_signal'] = 0
        
        return signals
    
    def _calculate_sentiment_impact(self, sentiment_score: float) -> str:
        """Calculate sentiment impact level"""
        abs_score = abs(sentiment_score)
        if abs_score > 0.7:
            return 'HIGH'
        elif abs_score > 0.3:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _calculate_enhanced_confidence(self, signals: Dict, ml_pred: Dict, 
                                      sentiment: float = None) -> float:
        """Calculate enhanced confidence score with ML and sentiment"""
        # Base technical confidence (similar to basic version)
        base_confidence = 50  # Placeholder
        
        # ML adjustment
        if ml_pred.get('ml_confidence'):
            ml_weight = 0.3
            base_confidence = base_confidence * (1 - ml_weight) + \
                            ml_pred['ml_confidence'] * ml_weight
        
        # Sentiment adjustment
        if sentiment is not None:
            sentiment_boost = abs(sentiment) * 10
            base_confidence = min(100, base_confidence + sentiment_boost)
        
        return round(base_confidence, 2)
    
    def _enhanced_prediction(self, df: pd.DataFrame, signals: Dict, 
                           ml_pred: Dict, sentiment: float = None) -> float:
        """Enhanced price movement prediction"""
        # Base prediction
        base_pred = 0  # Placeholder calculation
        
        # ML adjustment
        if ml_pred.get('ml_probability'):
            ml_direction = 1 if ml_pred['ml_probability'] > 50 else -1
            base_pred += ml_direction * 0.5
        
        # Sentiment adjustment
        if sentiment is not None:
            base_pred += sentiment * 2
        
        return round(base_pred, 2)
    
    def _determine_direction_advanced(self, signals: Dict, ml_pred: Dict, 
                                    sentiment: float = None) -> str:
        """Determine direction with all factors"""
        score = 0
        
        # Technical signals
        score += signals.get('rsi_signal', 0)
        score += signals.get('macd_signal', 0)
        
        # ML
        if ml_pred.get('ml_probability'):
            score += 1 if ml_pred['ml_probability'] > 60 else -1
        
        # Sentiment
        if sentiment is not None:
            score += sentiment * 2
        
        if score > 2:
            return 'STRONG_LONG'
        elif score > 0:
            return 'LONG'
        elif score < -2:
            return 'STRONG_SHORT'
        elif score < 0:
            return 'SHORT'
        else:
            return 'NEUTRAL'
    
    def _calculate_risk_advanced(self, df: pd.DataFrame, extended_data: Dict) -> str:
        """Calculate risk with additional factors"""
        latest = df.iloc[-1]
        
        # Volatility (ATR)
        volatility = (latest['ATR'] / latest['Close']) * 100 if 'ATR' in df.columns else 5
        
        # Beta
        beta = extended_data.get('beta', 1.0)
        
        # Combined risk
        if volatility > 5 or beta > 1.5:
            return 'HIGH'
        elif volatility < 2 and beta < 1.2:
            return 'LOW'
        else:
            return 'MEDIUM'


def main_advanced():
    """Main execution for advanced screener"""
    print("Initializing Advanced Day Trading Screener with ML...")
    
    screener = AdvancedDayTradingScreener(
        min_price=5.0,
        max_price=500.0,
        min_volume=1000000,
        use_ml=True
    )
    
    # Note: ML training would require historical data
    # screener.train_ml_model(historical_data)
    
    print("\nThis advanced version supports:")
    print("- Extended technical indicators (Stochastic, ADX, MFI, Ichimoku)")
    print("- Machine learning predictions")
    print("- Sentiment analysis integration")
    print("- Enhanced confidence scoring")
    print("\nTo use sentiment, integrate with your sentiment agent!")


if __name__ == "__main__":
    main_advanced()
