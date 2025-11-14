"""
Example usage scripts for the Day Trading Screener
"""

from day_trading_screener import DayTradingScreener
from datetime import datetime
import pandas as pd


def example_1_basic_scan():
    """Example 1: Basic scan of default universe"""
    print("=" * 80)
    print("EXAMPLE 1: Basic Stock Scan")
    print("=" * 80)
    
    screener = DayTradingScreener(
        min_price=5.0,
        max_price=500.0,
        min_volume=1000000
    )
    
    # Scan top 15 opportunities
    results = screener.scan_all_stocks(top_n=15)
    
    # Generate report
    report = screener.generate_report(results)
    print(report)
    
    # Save to CSV
    filename = f"scan_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    results.to_csv(filename, index=False)
    print(f"\n✅ Results saved to {filename}")


def example_2_custom_tickers():
    """Example 2: Analyze specific stocks"""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Custom Ticker Analysis")
    print("=" * 80)
    
    screener = DayTradingScreener()
    
    # Your watchlist
    watchlist = ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'TSLA', 'AMD', 'META']
    
    print(f"\nAnalyzing watchlist: {', '.join(watchlist)}\n")
    
    results = screener.scan_all_stocks(custom_tickers=watchlist, top_n=10)
    
    # Display results
    if not results.empty:
        print(f"\n{'Ticker':<8} {'Price':<10} {'Direction':<12} {'Confidence':<12} {'Pred. Move':<12} {'Risk'}")
        print("-" * 80)
        
        for _, row in results.iterrows():
            print(f"{row['ticker']:<8} ${row['current_price']:<9.2f} {row['trade_direction']:<12} "
                  f"{row['confidence_score']:<11.1f}% {row['predicted_move_pct']:>+6.2f}%      "
                  f"{row['risk_level']}")


def example_3_single_stock_analysis():
    """Example 3: Detailed single stock analysis"""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Detailed Single Stock Analysis")
    print("=" * 80)
    
    screener = DayTradingScreener()
    
    ticker = 'NVDA'
    print(f"\nAnalyzing {ticker} in detail...\n")
    
    analysis = screener.analyze_stock(ticker)
    
    if analysis:
        print(f"🎯 {analysis['ticker']} - ${analysis['current_price']:.2f}")
        print("-" * 60)
        print(f"Trade Direction:    {analysis['trade_direction']}")
        print(f"Confidence Score:   {analysis['confidence_score']:.1f}/100")
        print(f"Predicted Move:     {analysis['predicted_move_pct']:+.2f}%")
        print(f"Risk Level:         {analysis['risk_level']}")
        print(f"Day Change:         {analysis['price_change_pct']:+.2f}%")
        print()
        print("Technical Indicators:")
        print(f"  RSI:              {analysis.get('rsi_value', 'N/A')}")
        print(f"  VWAP Distance:    {analysis.get('vwap_distance', 'N/A')}%")
        print(f"  Volume Ratio:     {analysis.get('volume_ratio', 'N/A')}x")
        print(f"  Momentum:         {analysis.get('momentum_pct', 'N/A')}%")
        
        # Trading suggestion
        print("\n💡 Trading Suggestion:")
        if analysis['trade_direction'] == 'LONG' and analysis['confidence_score'] > 70:
            print(f"   Strong buy signal detected!")
            print(f"   Entry: ${analysis['current_price']:.2f}")
            print(f"   Target: ${analysis['current_price'] * (1 + analysis['predicted_move_pct']/100):.2f}")
            print(f"   Stop Loss: ${analysis['current_price'] * 0.98:.2f} (2% below)")
        elif analysis['trade_direction'] == 'SHORT' and analysis['confidence_score'] > 70:
            print(f"   Strong short signal detected!")
            print(f"   Entry: ${analysis['current_price']:.2f}")
            print(f"   Target: ${analysis['current_price'] * (1 + analysis['predicted_move_pct']/100):.2f}")
            print(f"   Stop Loss: ${analysis['current_price'] * 1.02:.2f} (2% above)")
        else:
            print(f"   Signals are not strong enough. Consider waiting for better setup.")


def example_4_filter_by_criteria():
    """Example 4: Custom filtering"""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Advanced Filtering")
    print("=" * 80)
    
    screener = DayTradingScreener()
    
    # Scan all
    results = screener.scan_all_stocks(top_n=50)
    
    if results.empty:
        print("No results found")
        return
    
    # Filter 1: High confidence LONG opportunities
    print("\n🎯 High Confidence LONG Opportunities (>75%):")
    print("-" * 60)
    long_ops = results[
        (results['trade_direction'] == 'LONG') & 
        (results['confidence_score'] > 75)
    ]
    
    if not long_ops.empty:
        for _, row in long_ops.head(5).iterrows():
            print(f"{row['ticker']:<6} ${row['current_price']:<8.2f} "
                  f"Confidence: {row['confidence_score']:.1f}%  "
                  f"Predicted: {row['predicted_move_pct']:+.2f}%")
    else:
        print("None found")
    
    # Filter 2: Low risk opportunities
    print("\n🛡️  Low Risk Opportunities:")
    print("-" * 60)
    low_risk = results[results['risk_level'] == 'LOW']
    
    if not low_risk.empty:
        for _, row in low_risk.head(5).iterrows():
            print(f"{row['ticker']:<6} ${row['current_price']:<8.2f} "
                  f"{row['trade_direction']:<8} "
                  f"Confidence: {row['confidence_score']:.1f}%")
    else:
        print("None found")
    
    # Filter 3: High volume breakouts
    print("\n📊 High Volume Opportunities (>1.5x):")
    print("-" * 60)
    high_vol = results[results['volume_ratio'] > 1.5].sort_values('volume_ratio', ascending=False)
    
    if not high_vol.empty:
        for _, row in high_vol.head(5).iterrows():
            print(f"{row['ticker']:<6} ${row['current_price']:<8.2f} "
                  f"Volume: {row['volume_ratio']:.2f}x  "
                  f"Confidence: {row['confidence_score']:.1f}%")
    else:
        print("None found")


def example_5_create_watchlist():
    """Example 5: Create a prioritized watchlist"""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Create Daily Watchlist")
    print("=" * 80)
    
    screener = DayTradingScreener()
    
    print("\nScanning market for best opportunities...\n")
    results = screener.scan_all_stocks(top_n=30)
    
    if results.empty:
        print("No opportunities found")
        return
    
    # Create tiered watchlist
    tier1 = results[results['confidence_score'] >= 80]
    tier2 = results[(results['confidence_score'] >= 60) & (results['confidence_score'] < 80)]
    tier3 = results[results['confidence_score'] < 60]
    
    print("📋 DAILY WATCHLIST")
    print("=" * 60)
    
    print(f"\n⭐ TIER 1 - High Priority ({len(tier1)} stocks)")
    print("   Confidence: 80-100%")
    if not tier1.empty:
        for _, row in tier1.iterrows():
            print(f"   • {row['ticker']} ({row['trade_direction']}) - "
                  f"${row['current_price']:.2f} | "
                  f"Conf: {row['confidence_score']:.0f}% | "
                  f"Move: {row['predicted_move_pct']:+.1f}%")
    
    print(f"\n✓ TIER 2 - Medium Priority ({len(tier2)} stocks)")
    print("   Confidence: 60-79%")
    if not tier2.empty:
        for _, row in tier2.head(5).iterrows():
            print(f"   • {row['ticker']} ({row['trade_direction']}) - "
                  f"${row['current_price']:.2f} | "
                  f"Conf: {row['confidence_score']:.0f}%")
    
    print(f"\n○ TIER 3 - Watch Only ({len(tier3)} stocks)")
    print("   Confidence: <60%")
    
    # Save watchlist
    watchlist_file = f"watchlist_{datetime.now().strftime('%Y%m%d')}.csv"
    results.to_csv(watchlist_file, index=False)
    print(f"\n✅ Watchlist saved to {watchlist_file}")


def example_6_compare_stocks():
    """Example 6: Compare multiple stocks side-by-side"""
    print("\n" + "=" * 80)
    print("EXAMPLE 6: Stock Comparison")
    print("=" * 80)
    
    screener = DayTradingScreener()
    
    # Stocks to compare
    comparison_list = ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'TSLA']
    
    print(f"\nComparing: {', '.join(comparison_list)}\n")
    
    results = []
    for ticker in comparison_list:
        analysis = screener.analyze_stock(ticker)
        if analysis:
            results.append(analysis)
    
    if results:
        df = pd.DataFrame(results)
        df = df.sort_values('confidence_score', ascending=False)
        
        print(f"{'Rank':<6} {'Ticker':<8} {'Price':<10} {'Confidence':<12} "
              f"{'Direction':<12} {'Pred. Move':<12} {'Risk'}")
        print("-" * 80)
        
        for i, (_, row) in enumerate(df.iterrows(), 1):
            print(f"{i:<6} {row['ticker']:<8} ${row['current_price']:<9.2f} "
                  f"{row['confidence_score']:<11.1f}% {row['trade_direction']:<12} "
                  f"{row['predicted_move_pct']:>+6.2f}%      {row['risk_level']}")
        
        # Best pick
        best = df.iloc[0]
        print(f"\n🏆 Best Pick: {best['ticker']} with {best['confidence_score']:.1f}% confidence")


def run_all_examples():
    """Run all examples"""
    examples = [
        example_1_basic_scan,
        example_2_custom_tickers,
        example_3_single_stock_analysis,
        example_4_filter_by_criteria,
        example_5_create_watchlist,
        example_6_compare_stocks
    ]
    
    for i, example in enumerate(examples, 1):
        try:
            example()
            if i < len(examples):
                input("\n\nPress Enter to continue to next example...")
        except Exception as e:
            print(f"\n❌ Error in example {i}: {e}")
            continue


if __name__ == "__main__":
    print("Day Trading Screener - Example Scripts")
    print("=" * 80)
    print("\nSelect an example to run:")
    print("1. Basic stock scan")
    print("2. Custom ticker analysis")
    print("3. Detailed single stock analysis")
    print("4. Advanced filtering")
    print("5. Create daily watchlist")
    print("6. Compare stocks")
    print("7. Run all examples")
    print("\n0. Exit")
    
    choice = input("\nEnter choice (0-7): ").strip()
    
    examples = {
        '1': example_1_basic_scan,
        '2': example_2_custom_tickers,
        '3': example_3_single_stock_analysis,
        '4': example_4_filter_by_criteria,
        '5': example_5_create_watchlist,
        '6': example_6_compare_stocks,
        '7': run_all_examples
    }
    
    if choice in examples:
        examples[choice]()
    elif choice == '0':
        print("Exiting...")
    else:
        print("Invalid choice!")
