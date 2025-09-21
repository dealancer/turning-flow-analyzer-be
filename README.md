# Turning Flow Analyzer API

A Python serverless API that downloads webpages, extracts article content, and provides comprehensive AI-powered text analysis with entity recognition. Built with AWS SAM (Serverless Application Model) for deployment as Lambda functions.

## Features

- RESTful API endpoints for web content analysis
- Downloads webpage content from any URL
- Extracts main article content using Mozilla's Readability algorithm
- Removes navigation, sidebars, and other non-content elements
- AI-powered analysis (supports OpenAI or Anthropic API):
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

## API Endpoints

- `POST /analyze` - Analyze webpage content from URL
- `GET /health` - Health check endpoint

### Example Request
```bash
curl -X POST http://localhost:3000/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/article", "verbose": false}'
```

### Example Response
```json
{
  "url": "https://example.com/article",
  "success": true,
  "analysis": {
    "author": "Author Name",
    "topic": "Main Topic",
    "summary": "Brief summary of the article content.",
    "reading_difficulty": "medium",
    "estimated_reading_time_minutes": 5,
    "entities": [
      {
        "entity": "Entity Name",
        "entity_type": "person",
        "sentiment": "positive"
      }
    ]
  }
}
```

## Prerequisites

- [AWS CLI](https://aws.amazon.com/cli/) configured
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) installed
- [Docker](https://www.docker.com/) installed (for local testing)
- Python 3.9+

## Local Development

1. **Clone and setup the project:**
   ```bash
   git clone <repository-url>
   cd turning-flow-analyzer-lambda
   ```

2. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```bash
   # For Anthropic Claude (recommended)
   ANTHROPIC_API_KEY="your_anthropic_api_key"

   # Or for OpenAI GPT
   OPENAI_API_KEY="your_openai_api_key"
   ```

3. **Build the application:**
   ```bash
   sam build
   ```

4. **Start the local API:**
   ```bash
   sam local start-api --port 3000
   ```

5. **Test the API:**
   ```bash
   # Health check
   curl http://localhost:3000/health

   # Analyze a webpage
   curl -X POST http://localhost:3000/analyze \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com/article"}'
   ```

## Deployment

1. **Deploy to AWS:**
   ```bash
   sam deploy --guided
   ```

2. **Set API keys as parameters:**
   During deployment, you'll be prompted to provide:
   - `AnthropicApiKey` (optional)
   - `OpenAiApiKey` (optional)

3. **Get the API Gateway URL:**
   After deployment, the API Gateway URL will be displayed in the outputs.


## Development Commands

```bash
# Validate SAM template
sam validate

# Build application
sam build

# Start local API
sam local start-api

# Deploy to AWS
sam deploy --guided

# Delete stack
sam delete
```
