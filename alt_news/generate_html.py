#!/usr/bin/env python3
"""
HTML Generator for Alternative News Aggregator
Creates a beautiful, modern news homepage
"""

import json
from datetime import datetime
from typing import List, Dict


class NewsPageGenerator:
    """Generates beautiful HTML news pages"""

    @staticmethod
    def generate_css() -> str:
        """Generate modern CSS styling"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px 0;
            margin-bottom: 40px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-align: center;
        }

        header .tagline {
            text-align: center;
            font-size: 1.1em;
            opacity: 0.9;
            margin-bottom: 5px;
        }

        header .timestamp {
            text-align: center;
            font-size: 0.9em;
            opacity: 0.8;
        }

        .alert-banner {
            background: #ff6b6b;
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 30px;
            text-align: center;
            font-weight: 600;
        }

        .hero-story {
            background: white;
            border-radius: 12px;
            padding: 40px;
            margin-bottom: 40px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            border-left: 5px solid #667eea;
        }

        .hero-story .category {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            margin-bottom: 15px;
            font-weight: 600;
        }

        .hero-story h2 {
            font-size: 2.2em;
            margin-bottom: 15px;
            color: #2c3e50;
            line-height: 1.3;
        }

        .hero-story .summary {
            font-size: 1.2em;
            color: #555;
            margin-bottom: 20px;
            line-height: 1.7;
        }

        .hero-story .meta {
            display: flex;
            align-items: center;
            gap: 20px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }

        .hero-story .source {
            font-weight: 600;
            color: #667eea;
        }

        .hero-story .score-badge {
            background: #f0f0f0;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.9em;
        }

        .hero-story .read-more {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 12px 30px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 600;
            transition: background 0.3s;
        }

        .hero-story .read-more:hover {
            background: #5568d3;
        }

        .section-title {
            font-size: 1.8em;
            margin-bottom: 25px;
            color: #2c3e50;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }

        .stories-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }

        .story-card {
            background: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            transition: transform 0.2s, box-shadow 0.2s;
            border-top: 4px solid #667eea;
        }

        .story-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }

        .story-card .category {
            display: inline-block;
            background: #f0f0f0;
            color: #667eea;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.8em;
            margin-bottom: 12px;
            font-weight: 600;
        }

        .story-card h3 {
            font-size: 1.3em;
            margin-bottom: 12px;
            color: #2c3e50;
            line-height: 1.4;
        }

        .story-card .summary {
            color: #666;
            margin-bottom: 15px;
            font-size: 0.95em;
            line-height: 1.6;
        }

        .story-card .meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.85em;
            color: #888;
            margin-bottom: 15px;
            flex-wrap: wrap;
            gap: 10px;
        }

        .story-card .source {
            font-weight: 600;
            color: #667eea;
        }

        .story-card .scores {
            display: flex;
            gap: 10px;
        }

        .story-card .score {
            background: #f0f0f0;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.85em;
        }

        .story-card a {
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.2s;
        }

        .story-card a:hover {
            color: #5568d3;
            text-decoration: underline;
        }

        .footer {
            text-align: center;
            padding: 40px 0;
            color: #888;
            font-size: 0.9em;
        }

        .uniqueness-badge {
            background: #ff6b6b;
            color: white;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: 600;
        }

        .importance-badge {
            background: #51cf66;
            color: white;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: 600;
        }

        @media (max-width: 768px) {
            .stories-grid {
                grid-template-columns: 1fr;
            }

            header h1 {
                font-size: 2em;
            }

            .hero-story h2 {
                font-size: 1.8em;
            }

            .hero-story .summary {
                font-size: 1.1em;
            }
        }
        """

    @staticmethod
    def generate_story_card(story: Dict, index: int) -> str:
        """Generate HTML for a single story card"""
        uniqueness_class = "uniqueness-badge" if story['uniqueness_score'] >= 8 else "score"
        importance_class = "importance-badge" if story['importance_score'] >= 8 else "score"

        return f"""
        <div class="story-card">
            <span class="category">{story['category']}</span>
            <h3>{story['headline']}</h3>
            <p class="summary">{story['summary']}</p>
            <div class="meta">
                <span class="source">{story['source']}</span>
                <div class="scores">
                    <span class="{uniqueness_class}">📍 {story['uniqueness_score']}/10</span>
                    <span class="{importance_class}">⭐ {story['importance_score']}/10</span>
                </div>
            </div>
            <a href="{story['url']}" target="_blank">Read Full Article →</a>
        </div>
        """

    @staticmethod
    def generate_hero_story(story: Dict) -> str:
        """Generate HTML for the hero story"""
        return f"""
        <div class="hero-story">
            <span class="category">{story['category']}</span>
            <h2>{story['headline']}</h2>
            <p class="summary">{story['summary']}</p>
            <div class="meta">
                <span class="source">📰 {story['source']}</span>
                <span class="score-badge">Uniqueness: {story['uniqueness_score']}/10</span>
                <span class="score-badge">Importance: {story['importance_score']}/10</span>
            </div>
            <a href="{story['url']}" class="read-more" target="_blank">Read Full Story</a>
        </div>
        """

    def generate_html(self, stories: List[Dict], generated_at: str) -> str:
        """Generate complete HTML page"""
        # Sort stories by score
        sorted_stories = sorted(
            stories,
            key=lambda s: (s['importance_score'] * 0.6) + (s['uniqueness_score'] * 0.4),
            reverse=True
        )

        # Hero story (top story)
        hero = sorted_stories[0] if sorted_stories else None
        remaining_stories = sorted_stories[1:] if len(sorted_stories) > 1 else []

        # Generate story cards
        story_cards = "\n".join([
            self.generate_story_card(story, i)
            for i, story in enumerate(remaining_stories, 1)
        ])

        # Format timestamp
        try:
            dt = datetime.fromisoformat(generated_at.replace('Z', '+00:00'))
            formatted_time = dt.strftime("%B %d, %Y at %I:%M %p")
        except:
            formatted_time = generated_at

        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Alternative News - What Mainstream Media Isn't Covering</title>
            <style>{self.generate_css()}</style>
        </head>
        <body>
            <header>
                <div class="container">
                    <h1>🔍 Alternative News Digest</h1>
                    <p class="tagline">What Mainstream Media Isn't Covering</p>
                    <p class="timestamp">Generated: {formatted_time}</p>
                </div>
            </header>

            <div class="container">
                <div class="alert-banner">
                    ⚠️ These stories are receiving minimal mainstream coverage but may have significant implications
                </div>

                {self.generate_hero_story(hero) if hero else ''}

                <h2 class="section-title">📰 More Important Stories</h2>
                <div class="stories-grid">
                    {story_cards}
                </div>

                <div class="footer">
                    <p><strong>Scoring System:</strong></p>
                    <p>📍 Uniqueness Score: How little coverage this gets from mainstream sources (higher = more underreported)</p>
                    <p>⭐ Importance Score: Potential significance and impact of the story</p>
                    <p style="margin-top: 20px; opacity: 0.7;">
                        This aggregator pulls from diverse alternative sources including independent journalists,
                        international media, and investigative outlets to highlight stories that deserve more attention.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

        return html

    def generate_from_json(self, json_file: str, output_file: str):
        """Generate HTML from JSON data file"""
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        html = self.generate_html(data['stories'], data['generated_at'])

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✅ HTML generated: {output_file}")
        return output_file


if __name__ == '__main__':
    import sys

    generator = NewsPageGenerator()

    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else 'news.html'
    else:
        input_file = 'news_data.json'
        output_file = 'news.html'

    try:
        generator.generate_from_json(input_file, output_file)
        print(f"\n🎉 Open {output_file} in your browser to view your news digest!")
    except FileNotFoundError:
        print(f"❌ Error: {input_file} not found. Run aggregator.py first!")
    except Exception as e:
        print(f"❌ Error: {e}")
