"""
Advanced Day Trading Screener - S&P 500 Scanner
Scans all 503 S&P 500 stocks with advanced indicators
"""

from advanced_screener import AdvancedDayTradingScreener
from datetime import datetime
import pandas as pd

def main():
    print("=" * 80)
    print("ADVANCED DAY TRADING SCREENER - S&P 500 SCAN")
    print("=" * 80)
    print()
    
    # Initialize the screener
    print("Initializing Advanced Screener...")
    screener = AdvancedDayTradingScreener(
        min_price=5.0,
        max_price=500.0,
        min_volume=1000000,
        use_ml=False  # Set to False (no ML training needed)
    )
    print("✅ Screener initialized!\n")
    
    # Fetch S&P 500 list
    print("Fetching S&P 500 stock list...")
    sp500_tickers = screener.fetch_sp500_tickers()
    
    print(f"\n{'=' * 80}")
    print(f"🔍 SCANNING {len(sp500_tickers)} S&P 500 STOCKS")
    print(f"{'=' * 80}")
    print(f"\n⏱️  Estimated time: 25-30 minutes")
    print(f"☕ Grab a coffee and relax...\n")
    
    results = []
    total = len(sp500_tickers)
    start_time = datetime.now()
    
    for i, ticker in enumerate(sp500_tickers, 1):
        # Progress updates every 25 stocks
        if i % 25 == 0 or i == 1:
            elapsed = (datetime.now() - start_time).seconds
            stocks_per_sec = i / max(elapsed, 1)
            remaining = (total - i) / max(stocks_per_sec, 0.1)
            
            print(f"Progress: {i}/{total} stocks ({i/total*100:.1f}%) - "
                  f"~{int(remaining/60)}min {int(remaining%60)}sec remaining")
        
        try:
            analysis = screener.analyze_with_sentiment(
                ticker=ticker,
                sentiment_score=None  # No sentiment for now
            )
            
            if analysis:
                results.append(analysis)
        
        except Exception as e:
            # Silently continue on errors (some stocks may have insufficient data)
            pass
    
    elapsed_time = (datetime.now() - start_time).seconds
    
    print(f"\n{'=' * 80}")
    print(f"✅ SCAN COMPLETE!")
    print(f"{'=' * 80}")
    print(f"   Total time: {int(elapsed_time/60)}min {elapsed_time%60}sec")
    print(f"   Stocks analyzed: {total}")
    print(f"   Viable opportunities: {len(results)}")
    print(f"{'=' * 80}\n")
    
    if not results:
        print("⚠️  No trading opportunities found matching criteria.")
        print("   Try adjusting filters in the screener initialization.")
        return
    
    # Convert to DataFrame and sort
    df = pd.DataFrame(results)
    df = df.sort_values('confidence_score', ascending=False)
    
    # Display top 20
    print("=" * 80)
    print("TOP 20 OPPORTUNITIES")
    print("=" * 80)
    print()
    
    for i, (idx, stock) in enumerate(df.head(20).iterrows(), 1):
        print(f"#{i}. {stock['ticker']} - ${stock['current_price']:.2f}")
        print(f"   Direction: {stock['trade_direction']}")
        print(f"   Confidence: {stock['confidence_score']:.1f}/100")
        print(f"   Predicted Move: {stock['predicted_move_pct']:+.2f}%")
        print(f"   Risk Level: {stock['risk_level']}")
        
        # Advanced features
        if 'market_cap' in stock and stock['market_cap']:
            market_cap_b = stock['market_cap'] / 1e9
            print(f"   Market Cap: ${market_cap_b:.1f}B")
        
        if 'beta' in stock and stock['beta']:
            print(f"   Beta: {stock['beta']:.2f}")
        
        if 'sector' in stock and stock['sector']:
            print(f"   Sector: {stock['sector']}")
        
        print()
    
    # Save full results
    output_file = f"sp500_advanced_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(output_file, index=False)
    
    print("=" * 80)
    print(f"💾 Full results saved to: {output_file}")
    print("=" * 80)
    print()
    
    # Summary statistics
    print("SUMMARY STATISTICS")
    print("-" * 80)
    print(f"Total opportunities: {len(results)}")
    print(f"High confidence (>80%): {len(df[df['confidence_score'] > 80])}")
    print(f"Medium confidence (70-80%): {len(df[(df['confidence_score'] >= 70) & (df['confidence_score'] <= 80)])}")
    print(f"LONG signals: {len(df[df['trade_direction'].str.contains('LONG', na=False)])}")
    print(f"SHORT signals: {len(df[df['trade_direction'].str.contains('SHORT', na=False)])}")
    print(f"LOW risk: {len(df[df['risk_level'] == 'LOW'])}")
    print(f"MEDIUM risk: {len(df[df['risk_level'] == 'MEDIUM'])}")
    print(f"HIGH risk: {len(df[df['risk_level'] == 'HIGH'])}")
    print()
    
    # Sector breakdown if available
    if 'sector' in df.columns:
        print("TOP SECTORS")
        print("-" * 80)
        sector_counts = df['sector'].value_counts().head(5)
        for sector, count in sector_counts.items():
            print(f"  {sector}: {count} stocks")
        print()
    
    print("=" * 80)
    print("NEXT STEPS:")
    print("=" * 80)
    print(f"""
1. Review the CSV file: {output_file}
2. Focus on high confidence stocks (>80%)
3. Check news for your top picks
4. Create your watchlist for the day
5. Set up charts and alerts

For sentiment integration:
  - Add your sentiment agent
  - Pass sentiment_score to analyze_with_sentiment()
  
For machine learning:
  - Set use_ml=True in initialization
  - Train model with historical data first
""")


# Quick scan function for testing (10 stocks only)
def quick_scan():
    """Quick scan of 10 popular stocks for testing"""
    print("=" * 80)
    print("QUICK SCAN - 10 Popular Stocks")
    print("=" * 80)
    print()
    
    screener = AdvancedDayTradingScreener(use_ml=False)
    
    popular_stocks = [
        'AAPL', 'MSFT', 'GOOGL', 'NVDA', 'TSLA',
        'AMD', 'META', 'AMZN', 'NFLX', 'JPM'
    ]
    
    results = []
    for ticker in popular_stocks:
        try:
            analysis = screener.analyze_with_sentiment(ticker)
            if analysis:
                results.append(analysis)
                print(f"{ticker}: {analysis['confidence_score']:.1f}% - {analysis['trade_direction']}")
        except:
            print(f"{ticker}: Error")
    
    if results:
        df = pd.DataFrame(results).sort_values('confidence_score', ascending=False)
        print(f"\nTop pick: {df.iloc[0]['ticker']} with {df.iloc[0]['confidence_score']:.1f}% confidence")


if __name__ == "__main__":
    import sys
    
    # Check if user wants quick scan
    if len(sys.argv) > 1 and sys.argv[1] == '--quick':
        quick_scan()
    else:
        main()
