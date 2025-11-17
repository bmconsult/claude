#!/usr/bin/env python3
"""
Alternative News Aggregator
Synthesizes news from alternative sources and highlights what mainstream media isn't covering
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
import subprocess
import time


@dataclass
class NewsStory:
    """Represents a news story"""
    headline: str
    summary: str
    source: str
    url: str
    importance_score: float  # 0-10
    uniqueness_score: float  # 0-10 (how unique vs mainstream)
    category: str
    timestamp: str

    @property
    def total_score(self) -> float:
        """Combined score for ranking"""
        return (self.importance_score * 0.6) + (self.uniqueness_score * 0.4)


class AlternativeNewsAggregator:
    """Main aggregator class"""

    # Alternative news sources to monitor
    ALTERNATIVE_SOURCES = [
        # Independent/Substack
        "Matt Taibbi", "Glenn Greenwald", "Bari Weiss",
        # International
        "Al Jazeera", "BBC World", "RT", "SCMP",
        # Alternative US
        "The Intercept", "ProPublica", "The Grayzone",
        # Various perspectives
        "Common Dreams", "Reason", "The American Conservative",
        # Citizen journalism
        "Substack independent journalists",
    ]

    # Mainstream sources for comparison
    MAINSTREAM_SOURCES = [
        "CNN", "Fox News", "MSNBC", "New York Times",
        "Washington Post", "Wall Street Journal"
    ]

    def __init__(self, max_stories: int = 20):
        self.max_stories = max_stories
        self.stories: List[NewsStory] = []
        self.mainstream_topics: List[str] = []

    def fetch_alternative_news(self) -> List[Dict]:
        """
        Fetch news from alternative sources
        In a real implementation, this would use web scraping or APIs
        For now, we'll use web search to find recent alternative news
        """
        print("🔍 Fetching alternative news from diverse sources...")

        # Search queries to find alternative news
        search_queries = [
            "alternative news today important stories",
            "independent journalism latest news",
            "what mainstream media isn't covering",
            "underreported news stories today",
            "Substack journalists breaking news",
            "international perspective US news",
        ]

        # Placeholder for fetched articles
        # In production, this would actually fetch from sources
        articles = []

        print(f"✓ Found {len(articles)} articles from alternative sources")
        return articles

    def fetch_mainstream_topics(self) -> List[str]:
        """
        Fetch what mainstream media is currently covering
        This helps identify gaps
        """
        print("📰 Checking mainstream media coverage...")

        # In production, scrape front pages of major outlets
        # For now, placeholder
        topics = []

        print(f"✓ Identified {len(topics)} mainstream topics")
        return topics

    def analyze_story_importance(self, story_data: Dict) -> float:
        """
        Analyze how important/significant a story is
        Factors: impact, timeliness, relevance, credibility
        """
        # In production, use AI/LLM to analyze
        # For demo, return placeholder
        return 7.5

    def calculate_uniqueness(self, story_data: Dict) -> float:
        """
        Calculate how unique this story is vs mainstream coverage
        Higher score = not being covered by mainstream
        """
        # In production, compare against mainstream topics
        # For demo, return placeholder
        return 8.0

    def categorize_story(self, story_data: Dict) -> str:
        """Categorize the story"""
        categories = [
            "Politics", "Economics", "International",
            "Technology", "Health", "Environment",
            "Civil Liberties", "Corruption", "Media Criticism"
        ]
        # In production, use AI to categorize
        return "Politics"

    def generate_summary(self, article_text: str) -> str:
        """Generate a concise summary of the article"""
        # In production, use AI to summarize
        return "Summary placeholder"

    def process_stories(self, articles: List[Dict]) -> List[NewsStory]:
        """Process raw articles into NewsStory objects with scores"""
        stories = []

        for article in articles:
            story = NewsStory(
                headline=article.get('headline', ''),
                summary=article.get('summary', ''),
                source=article.get('source', ''),
                url=article.get('url', ''),
                importance_score=self.analyze_story_importance(article),
                uniqueness_score=self.calculate_uniqueness(article),
                category=self.categorize_story(article),
                timestamp=datetime.now().isoformat()
            )
            stories.append(story)

        return stories

    def rank_stories(self, stories: List[NewsStory]) -> List[NewsStory]:
        """Rank stories by total score"""
        return sorted(stories, key=lambda s: s.total_score, reverse=True)

    def filter_top_stories(self, stories: List[NewsStory]) -> List[NewsStory]:
        """Filter to top N most important/unique stories"""
        ranked = self.rank_stories(stories)
        return ranked[:self.max_stories]

    def aggregate(self) -> List[NewsStory]:
        """Main aggregation process"""
        print("\n🚀 Starting Alternative News Aggregation...")
        print("=" * 60)

        # Fetch mainstream topics for comparison
        self.mainstream_topics = self.fetch_mainstream_topics()

        # Fetch alternative news
        articles = self.fetch_alternative_news()

        # Process and score
        print("\n🤖 Analyzing and scoring stories...")
        self.stories = self.process_stories(articles)

        # Filter top stories
        print(f"\n⭐ Selecting top {self.max_stories} most important stories...")
        top_stories = self.filter_top_stories(self.stories)

        print(f"\n✨ Aggregation complete! Found {len(top_stories)} top stories")
        print("=" * 60)

        return top_stories

    def save_data(self, stories: List[NewsStory], filepath: str):
        """Save stories to JSON for the HTML generator"""
        data = {
            'generated_at': datetime.now().isoformat(),
            'story_count': len(stories),
            'stories': [asdict(story) for story in stories]
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Data saved to {filepath}")


class DemoDataGenerator:
    """Generate realistic demo data for testing"""

    DEMO_STORIES = [
        {
            'headline': 'Unreported Federal Reserve Policy Shift Could Impact Global Markets',
            'summary': 'Alternative economists are highlighting a little-noticed change in Fed policy that mainstream media has largely overlooked. The shift could have significant implications for dollar stability and international trade.',
            'source': 'The Intercept',
            'url': 'https://theintercept.com/example-fed-policy',
            'category': 'Economics',
            'importance': 8.5,
            'uniqueness': 9.0
        },
        {
            'headline': 'Investigative Report Reveals Gaps in Official Narrative on Recent Foreign Policy Decision',
            'summary': 'Independent journalists have uncovered documents suggesting the mainstream narrative on recent diplomatic actions may be incomplete. Multiple international sources are reporting different perspectives.',
            'source': 'Matt Taibbi Substack',
            'url': 'https://example.com/taibbi-investigation',
            'category': 'International',
            'importance': 9.0,
            'uniqueness': 8.5
        },
        {
            'headline': 'Tech Censorship: New Data Shows Platform Bias Patterns',
            'summary': 'A comprehensive analysis by independent researchers reveals systematic patterns in content moderation across major platforms. The findings raise questions about selective enforcement of community guidelines.',
            'source': 'Glenn Greenwald',
            'url': 'https://greenwald.substack.com/example',
            'category': 'Technology',
            'importance': 7.5,
            'uniqueness': 9.5
        },
        {
            'headline': 'Mainstream Media Blackout on European Protests Over Energy Policies',
            'summary': 'Large-scale protests across multiple European countries over energy policies are receiving minimal US mainstream coverage despite significant participation. International sources like Al Jazeera and BBC provide extensive reporting.',
            'source': 'Al Jazeera',
            'url': 'https://aljazeera.com/example-protests',
            'category': 'International',
            'importance': 8.0,
            'uniqueness': 10.0
        },
        {
            'headline': 'Bipartisan Bill with Major Privacy Implications Advances Quietly',
            'summary': 'A bill that could significantly expand government surveillance capabilities is moving through Congress with little mainstream media attention. Civil liberties groups are raising alarms.',
            'source': 'Electronic Frontier Foundation',
            'url': 'https://eff.org/example-surveillance',
            'category': 'Civil Liberties',
            'importance': 9.5,
            'uniqueness': 8.0
        },
        {
            'headline': 'Corporate Media Consolidation Reaches New Milestone',
            'summary': 'The merger of two major media conglomerates, which reduces the number of companies controlling 90% of US media to just four, receives minimal coverage from the very outlets affected.',
            'source': 'Common Dreams',
            'url': 'https://commondreams.org/example',
            'category': 'Media Criticism',
            'importance': 8.5,
            'uniqueness': 9.0
        },
        {
            'headline': 'Independent Analysis Questions Official Economic Recovery Numbers',
            'summary': 'Alternative economists present data suggesting official employment and inflation figures may not capture the full economic picture. Their methodology and findings are gaining traction among financial analysts.',
            'source': 'ZeroHedge',
            'url': 'https://zerohedge.com/example',
            'category': 'Economics',
            'importance': 7.0,
            'uniqueness': 7.5
        },
        {
            'headline': 'Whistleblower Claims About Major Institution Go Underreported',
            'summary': 'A former insider at a major institution has made serious allegations backed by documentation, but mainstream outlets have given the story minimal coverage. Independent journalists are investigating.',
            'source': 'ProPublica',
            'url': 'https://propublica.org/example',
            'category': 'Corruption',
            'importance': 8.5,
            'uniqueness': 8.5
        },
        {
            'headline': 'Environmental Impact Study Results Contradicts Official Statements',
            'summary': 'An independent environmental assessment reveals findings that contradict official government statements about a major infrastructure project. The discrepancies raise questions about transparency.',
            'source': 'The Grayzone',
            'url': 'https://thegrayzone.com/example',
            'category': 'Environment',
            'importance': 7.5,
            'uniqueness': 8.0
        },
        {
            'headline': 'International Court Ruling Receives Minimal US Coverage',
            'summary': 'A significant ruling by an international court with potential implications for US policy gets minimal attention from mainstream US outlets, while international media provides extensive analysis.',
            'source': 'BBC World',
            'url': 'https://bbc.com/example',
            'category': 'International',
            'importance': 7.0,
            'uniqueness': 9.0
        }
    ]

    @staticmethod
    def generate_demo_stories() -> List[NewsStory]:
        """Generate demo stories for testing"""
        stories = []

        for data in DemoDataGenerator.DEMO_STORIES:
            story = NewsStory(
                headline=data['headline'],
                summary=data['summary'],
                source=data['source'],
                url=data['url'],
                importance_score=data['importance'],
                uniqueness_score=data['uniqueness'],
                category=data['category'],
                timestamp=datetime.now().isoformat()
            )
            stories.append(story)

        return stories


if __name__ == '__main__':
    print("\n" + "="*60)
    print("  ALTERNATIVE NEWS AGGREGATOR - DEMO MODE")
    print("="*60)

    # For demo, use generated stories
    print("\n📢 Running in DEMO mode with sample stories...")
    print("   (In production, this would fetch from real sources)\n")

    aggregator = AlternativeNewsAggregator(max_stories=10)
    demo_stories = DemoDataGenerator.generate_demo_stories()

    # Rank and filter
    top_stories = aggregator.rank_stories(demo_stories)[:10]

    # Save for HTML generation
    output_file = 'news_data.json'
    aggregator.save_data(top_stories, output_file)

    # Display summary
    print("\n📊 TOP STORIES:\n")
    for i, story in enumerate(top_stories, 1):
        print(f"{i}. {story.headline}")
        print(f"   Source: {story.source} | Score: {story.total_score:.1f}")
        print(f"   Importance: {story.importance_score}/10 | Uniqueness: {story.uniqueness_score}/10")
        print()

    print("✅ Run the HTML generator to create your news homepage!")
