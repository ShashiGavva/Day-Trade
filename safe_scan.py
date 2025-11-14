"""
SAFE SCAN - Minimal Rate Limiting Risk
Use this to scan small watchlists safely
"""

from day_trading_screener import DayTradingScreener
import time
import pandas as pd
from datetime import datetime

def safe_scan():
    """
    Safe scanning with very conservative rate limiting
    Scans 10 stocks with 10 second delays
    """
    print("=" * 80)
    print("SAFE SCAN - CONSERVATIVE RATE LIMITING")
    print("=" * 80)
    print()
    print("⚠️  This scan is VERY slow to avoid rate limits")
    print("   Scanning 10 stocks will take ~2 minutes")
    print()
    
    # Your watchlist - EDIT THIS WITH YOUR STOCKS
    my_watchlist = [
        'AAPL',   # Apple
        'MSFT',   # Microsoft
        'GOOGL',  # Google
        'NVDA',   # Nvidia
        'TSLA',   # Tesla
        'AMD',    # AMD
        'META',   # Meta
        'AMZN',   # Amazon
        'JPM',    # JP Morgan
        'BAC',    # Bank of America
    ]
    
    print(f"Scanning {len(my_watchlist)} stocks:")
    print(f"  {', '.join(my_watchlist)}")
    print()
    
    # Initialize screener
    screener = DayTradingScreener()
    
    results = []
    errors = []
    
    for i, ticker in enumerate(my_watchlist, 1):
        print(f"[{i}/{len(my_watchlist)}] Analyzing {ticker}...", end=' ')
        
        try:
            # Analyze the stock
            analysis = screener.analyze_stock(ticker)
            
            if analysis:
                results.append(analysis)
                print(f"✅ {analysis['confidence_score']:.1f}% confidence - {analysis['trade_direction']}")
            else:
                print("⚠️  No data available")
                errors.append(ticker)
        
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "Too Many Requests" in error_msg:
                print("🚨 RATE LIMIT HIT!")
                print()
                print("=" * 80)
                print("PAUSING FOR 60 SECONDS...")
                print("=" * 80)
                print()
                time.sleep(60)
                
                # Retry this stock
                try:
                    analysis = screener.analyze_stock(ticker)
                    if analysis:
                        results.append(analysis)
                        print(f"✅ Retry successful - {analysis['confidence_score']:.1f}%")
                    else:
                        errors.append(ticker)
                except:
                    errors.append(ticker)
                    print(f"❌ Retry failed")
            else:
                print(f"❌ Error: {error_msg[:50]}")
                errors.append(ticker)
        
        # LONG DELAY between stocks (10 seconds)
        if i < len(my_watchlist):
            print(f"   Waiting 10 seconds before next stock...")
            time.sleep(10)
    
    print()
    print("=" * 80)
    print("SCAN COMPLETE")
    print("=" * 80)
    print(f"Successful: {len(results)}/{len(my_watchlist)}")
    print(f"Failed: {len(errors)}/{len(my_watchlist)}")
    
    if errors:
        print(f"Failed stocks: {', '.join(errors)}")
    print()
    
    if not results:
        print("⚠️  No results to display")
        print("   This likely means you're still rate limited.")
        print("   Wait longer and try again.")
        return
    
    # Sort by confidence
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('confidence_score', ascending=False)
    
    # Display results
    print("=" * 80)
    print("TOP OPPORTUNITIES")
    print("=" * 80)
    print()
    
    for i, (_, stock) in enumerate(results_df.iterrows(), 1):
        print(f"#{i}. {stock['ticker']} - ${stock['current_price']:.2f}")
        print(f"   Direction: {stock['trade_direction']}")
        print(f"   Confidence: {stock['confidence_score']:.1f}/100")
        print(f"   Predicted Move: {stock['predicted_move_pct']:+.2f}%")
        print(f"   Risk: {stock['risk_level']}")
        print()
    
    # Save results
    filename = f"safe_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    results_df.to_csv(filename, index=False)
    print(f"💾 Results saved to: {filename}")
    print()


def test_single_stock():
    """
    Test if API is working with a single stock
    Use this to check if rate limits have reset
    """
    print("=" * 80)
    print("API TEST - Single Stock")
    print("=" * 80)
    print()
    print("Testing if Yahoo Finance API is accessible...")
    print()
    
    screener = DayTradingScreener()
    
    try:
        result = screener.analyze_stock('AAPL')
        
        if result:
            print("✅ SUCCESS! API is working")
            print()
            print(f"AAPL Test Result:")
            print(f"  Price: ${result['current_price']:.2f}")
            print(f"  Confidence: {result['confidence_score']:.1f}%")
            print(f"  Direction: {result['trade_direction']}")
            print()
            print("🎉 You can now run safe_scan()!")
        else:
            print("⚠️  API responded but no data available")
            print("   This might be a data issue, not rate limiting")
            print("   Try another stock or wait longer")
    
    except Exception as e:
        error_msg = str(e)
        print("❌ FAILED")
        print()
        print(f"Error: {error_msg[:100]}")
        print()
        
        if "429" in error_msg or "Too Many Requests" in error_msg:
            print("🚨 Still rate limited!")
            print("   Wait longer (try again in 1-2 hours)")
        else:
            print("❓ Different error - check your internet connection")


if __name__ == "__main__":
    import sys
    
    print()
    print("=" * 80)
    print("SAFE SCANNER - RATE LIMIT PROTECTION")
    print("=" * 80)
    print()
    print("Choose an option:")
    print("  1. Test API (single stock)")
    print("  2. Safe scan (10 stocks, ~2 minutes)")
    print()
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        print()
        test_single_stock()
    elif choice == "2":
        print()
        print("⚠️  Make sure you've waited at least 2 hours since your last scan!")
        print()
        confirm = input("Have you waited? (yes/no): ").strip().lower()
        
        if confirm in ['yes', 'y']:
            print()
            safe_scan()
        else:
            print()
            print("Come back after waiting! ⏰")
    else:
        print("Invalid choice")
