import json
import asyncio
from typing import Optional
from analyzer import download_webpage, extract_article_content, ai_analyze_text


def lambda_handler(event, context):
    """
    AWS Lambda handler for the Turning Flow Analyzer API
    """

    # Handle health check
    if event.get('httpMethod') == 'GET' and event.get('path') == '/health':
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'status': 'healthy',
                'message': 'Turning Flow Analyzer API is running'
            })
        }

    # Handle analysis request
    if event.get('httpMethod') == 'POST' and event.get('path') == '/analyze':
        try:
            # Parse request body
            body = event.get('body', '{}')
            if isinstance(body, str):
                request_data = json.loads(body)
            else:
                request_data = body

            url = request_data.get('url')
            if not url:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({
                        'error': 'Missing required field: url'
                    })
                }

            verbose = request_data.get('verbose', False)

            # Process the request
            result = asyncio.run(analyze_url_async(url, verbose))

            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps(result)
            }

        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Invalid JSON in request body'
                })
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': f'Internal server error: {str(e)}'
                })
            }

    # Handle unsupported methods/paths
    return {
        'statusCode': 404,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'error': 'Not found'
        })
    }


async def analyze_url_async(url: str, verbose: bool = False) -> dict:
    """
    Analyze a URL and return structured results
    """
    result = {
        'url': url,
        'success': False,
        'error': None,
        'extracted_text': None,
        'analysis': None
    }

    try:
        # Download webpage
        html_content = download_webpage(url)
        if not html_content:
            result['error'] = 'Failed to download webpage'
            return result

        # Extract article content
        article_text = extract_article_content(html_content)
        if not article_text:
            result['error'] = 'Failed to extract article content'
            return result

        if verbose:
            result['extracted_text'] = article_text

        # AI analysis
        ai_analysis = await ai_analyze_text(article_text)
        if ai_analysis:
            result['analysis'] = {
                'author': ai_analysis.author,
                'topic': ai_analysis.topic,
                'summary': ai_analysis.summary,
                'reading_difficulty': ai_analysis.reading_difficulty,
                'estimated_reading_time_minutes': ai_analysis.estimated_reading_time_minutes,
                'entities': [
                    {
                        'entity': entity.entity,
                        'entity_type': entity.entity_type,
                        'sentiment': entity.sentiment
                    }
                    for entity in ai_analysis.subjects
                ] if ai_analysis.subjects else []
            }
        else:
            result['analysis'] = None
            result['error'] = 'AI analysis not available - check API keys'

        result['success'] = True

    except Exception as e:
        result['error'] = str(e)

    return result