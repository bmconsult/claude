#!/usr/bin/env python3
"""
Alternative News Aggregator - Main Runner
Run this to generate your daily news digest
"""

import os
import sys
import webbrowser
from aggregator import AlternativeNewsAggregator, DemoDataGenerator
from generate_html import NewsPageGenerator


def main():
    """Main execution"""
    print("\n" + "="*70)
    print("  🔍 ALTERNATIVE NEWS AGGREGATOR")
    print("  What Mainstream Media Isn't Covering")
    print("="*70 + "\n")

    # Step 1: Aggregate news
    print("Step 1: Aggregating news from alternative sources...")
    print("-" * 70)

    aggregator = AlternativeNewsAggregator(max_stories=10)

    # TODO: In production, fetch from real sources
    # For now, use demo data
    print("ℹ️  Currently using DEMO data")
    print("   (In production version, this would fetch from real sources)\n")

    demo_stories = DemoDataGenerator.generate_demo_stories()
    top_stories = aggregator.rank_stories(demo_stories)[:10]

    # Save data
    data_file = 'news_data.json'
    aggregator.save_data(top_stories, data_file)

    # Step 2: Generate HTML
    print("\nStep 2: Generating beautiful HTML news page...")
    print("-" * 70)

    generator = NewsPageGenerator()
    html_file = 'alternative_news.html'
    generator.generate_from_json(data_file, html_file)

    # Step 3: Open in browser
    print("\n" + "="*70)
    print("  ✅ SUCCESS!")
    print("="*70)
    print(f"\n📰 Your alternative news digest is ready!")
    print(f"📁 File: {os.path.abspath(html_file)}")
    print(f"📊 Stories: {len(top_stories)}")

    # Ask to open
    if '--open' in sys.argv or '-o' in sys.argv:
        print("\n🌐 Opening in browser...")
        webbrowser.open(f'file://{os.path.abspath(html_file)}')
    else:
        print(f"\n💡 To view: Open '{html_file}' in your browser")
        print(f"   Or run: python run.py --open")

    print("\n" + "="*70 + "\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
