import requests
import argparse
from bs4 import BeautifulSoup
from readability import Document
import re
import asyncio
import os
from typing import Optional
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic import BaseModel


def download_webpage(url):
    """Download webpage content from given URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error downloading webpage: {e}")
        return None


def extract_article_content(html_content):
    """Extract main article content from HTML using readability."""
    try:
        doc = Document(html_content)
        article_html = doc.summary()

        soup = BeautifulSoup(article_html, 'html.parser')
        text = soup.get_text(strip=True, separator=' ')

        return text
    except Exception as e:
        print(f"Error extracting article content: {e}")
        return None

class EntityAnalysis(BaseModel):
    entity_type: str
    entity: str
    sentiment: str

class TextAnalysis(BaseModel):
    author: Optional[str]
    topic: str
    summary: str
    reading_difficulty: str
    estimated_reading_time_minutes: int
    subjects: list[EntityAnalysis]

async def ai_analyze_text(text: str) -> Optional[TextAnalysis]:
    """Use AI to analyze text content for deeper insights."""
    if not text.strip():
        return None

    # Try to use available AI models
    model = None
    if os.getenv('ANTHROPIC_API_KEY'):
        model = AnthropicModel('claude-3-5-sonnet-20241022')
    elif os.getenv('OPENAI_API_KEY'):
        model = OpenAIChatModel('gpt-4o-mini')
    else:
        print("No AI API key found. Set ANTHROPIC_API_KEY or OPENAI_API_KEY environment variable for AI analysis.")
        return None

    agent = Agent(
        model,
        output_type=TextAnalysis,
        system_prompt=(
            "You are a text analysis expert. Analyze the provided text and extract:"
            "1. Author name if mentioned in the text (optional)"
            "2. The main topic/subject"
            "3. A concise summary (2-3 sentences)"
            "4. Reading difficulty (easy/medium/hard)"
            "5. Estimated reading time in minutes (assume 200 words per minute)"
            "6. Identify and analyze key entities mentioned in the text with their sentiment:"
            "   - Entity types can include: person, company, country, city, organization, "
            "     ticker_symbol, book, movie, song, album, brand, product, technology, "
            "     programming_language, framework, tool, currency, cryptocurrency, "
            "     event, concept, industry, university, government_agency, political_party"
            "   - For each entity, provide: entity_type, entity (name), and sentiment (positive/negative/neutral)"
            "   - Focus on the most significant entities (5-10 maximum)"
        )
    )

    try:
        result = await agent.run(f"Analyze this text: {text[:2000]}...")
        return result.output
    except Exception as e:
        print(f"AI analysis error: {e}")
        return None


async def main_async():
    parser = argparse.ArgumentParser(description='Download webpage, extract article content, and analyze with AI')
    parser.add_argument('url', help='URL of the webpage to analyze')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show extracted text content')

    args = parser.parse_args()

    print(f"Downloading webpage: {args.url}")
    html_content = download_webpage(args.url)

    if not html_content:
        print("Failed to download webpage")
        return

    print("Extracting article content...")
    article_text = extract_article_content(html_content)

    if not article_text:
        print("Failed to extract article content")
        return

    if args.verbose:
        print(f"\nExtracted text:\n{article_text}\n")

    print("Analyzing text with AI...")
    ai_analysis = await ai_analyze_text(article_text)
    if ai_analysis:
        print("\n--- AI Analysis Results ---")
        if ai_analysis.author:
            print(f"Author: {ai_analysis.author}")
        print(f"Topic: {ai_analysis.topic}")
        print(f"Summary: {ai_analysis.summary}")
        print(f"Reading difficulty: {ai_analysis.reading_difficulty}")
        print(f"Estimated reading time: {ai_analysis.estimated_reading_time_minutes} minutes")

        if ai_analysis.subjects:
            print("\n--- Entity Analysis ---")
            for entity in ai_analysis.subjects:
                print(f"* {entity.entity} ({entity.entity_type}) - {entity.sentiment}")
    else:
        print("AI analysis not available")


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()