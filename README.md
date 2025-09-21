# Turning Flow CMD

A Python project that downloads webpages, extracts article content, and provides comprehensive AI-powered text analysis with entity recognition.

## Features

- Downloads webpage content from any URL
- Extracts main article content using Mozilla's Readability algorithm
- Removes navigation, sidebars, and other non-content elements
- AI-powered analysis (requires OpenAI or Anthropic API):
  - Author detection (when mentioned)
  - Content summary (2-3 sentences)
  - Topic identification
  - Reading difficulty assessment (easy/medium/hard)
  - Estimated reading time calculation
  - Entity recognition and sentiment analysis for:
    - People, companies, countries, cities, organizations
    - Books, movies, songs, albums, brands, products
    - Technologies, programming languages, frameworks, tools
    - Currencies, cryptocurrencies, events, concepts
    - Universities, government agencies, political parties
    - And more entity types with individual sentiment scoring

## Installation

1. Install pipenv if you haven't already:
   ```bash
   pip install pipenv
   ```

2. Install dependencies:
   ```bash
   pipenv install
   ```

3. Activate shell:
   ```bash
   pipenv shell
   ```

4. Add `.env` file with one of these environment variables for AI analysis:

```bash
# For Anthropic Claude
ANTHROPIC_API_KEY="your_anthropic_api_key"

# Or for OpenAI GPT
OPENAI_API_KEY="your_openai_api_key"
```

## Usage

Basic usage:
```bash
python src/turning-flow.py <URL>
```

With verbose output (shows extracted text):
```bash
python src/turning-flow.py <URL> --verbose
```
