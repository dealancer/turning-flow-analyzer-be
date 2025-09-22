# Turning Flow Analyzer BE

A Python serverless API that downloads webpages, extracts article content, and provides comprehensive AI-powered text analysis with entity recognition. Built with AWS SAM (Serverless Application Model) for deployment as Lambda functions.

## Features

- RESTful API endpoints for web content analysis
- Downloads webpage content from any URL
- Extracts main article content using Mozilla's Readability algorithm
- Removes navigation, sidebars, and other non-content elements
- **DynamoDB caching**: Results are cached for 1 week to improve performance and reduce API costs
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

4. **Start DynamoDB Local and create table:**
   ```bash
   # Start DynamoDB Local with docker-compose (recommended)
   docker-compose up -d

   # Create the DynamoDB table for local development
   ./scripts/create-local-table.sh

   # Start SAM with DynamoDB Local for full functionality including caching
   sam local start-api --docker-network sam-local --parameter-overrides 'DynamoDBEndpoint=http://dynamodb-local:8000'
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

## DynamoDB Local Development

When running locally with DynamoDB caching enabled, you can view and manage the cached data:

### View DynamoDB Contents
```bash
# List all tables
aws dynamodb list-tables --endpoint-url http://localhost:8000

# View all cached results (scan entire table)
aws dynamodb scan --table-name AnalysisResultsTable --endpoint-url http://localhost:8000

# Get specific URL result
aws dynamodb get-item --table-name AnalysisResultsTable \
  --key '{"url":{"S":"https://example.com"}}' \
  --endpoint-url http://localhost:8000

# View table schema and info
aws dynamodb describe-table --table-name AnalysisResultsTable --endpoint-url http://localhost:8000

# Count items in table
aws dynamodb scan --table-name AnalysisResultsTable --select "COUNT" --endpoint-url http://localhost:8000

# View only URLs and updated timestamps (projection)
aws dynamodb scan --table-name AnalysisResultsTable \
  --projection-expression "url, updated" \
  --endpoint-url http://localhost:8000
```

### DynamoDB Admin Web UI (Optional)
To view and manage DynamoDB data through a web interface:

```bash
# Install DynamoDB Admin globally
npm install -g dynamodb-admin

# Start DynamoDB Admin (make sure DynamoDB Local is running first)
# Option 1: Using environment variables
DYNAMO_ENDPOINT=http://localhost:8000 dynamodb-admin

# Option 2: Using command line options (if Option 1 doesn't work)
dynamodb-admin --host localhost --port 8000

# Visit the web interface
open http://localhost:8001
```

The web UI allows you to:
- Browse tables and data
- Create, edit, and delete items
- Execute queries and scans
- View table schemas and indexes

## Development Commands

```bash
# Validate SAM template
sam validate

# Build application
sam build

# Start DynamoDB Local and create table
docker-compose up -d
./scripts/create-local-table.sh

# Start local API with DynamoDB caching
sam local start-api --docker-network sam-local --parameter-overrides 'DynamoDBEndpoint=http://dynamodb-local:8000'

# Start local API without caching
sam local start-api

# Stop DynamoDB Local
docker-compose down

# Deploy to AWS
sam deploy --guided

# Delete stack
sam delete
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
