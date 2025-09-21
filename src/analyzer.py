import requests
from bs4 import BeautifulSoup
from readability import Document
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
    except requests.exceptions.RequestException:
        return None


def extract_article_content(html_content):
    """Extract main article content from HTML using readability."""
    try:
        doc = Document(html_content)
        article_html = doc.summary()

        soup = BeautifulSoup(article_html, 'html.parser')
        text = soup.get_text(strip=True, separator=' ')

        return text
    except Exception:
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
    except Exception:
        return None