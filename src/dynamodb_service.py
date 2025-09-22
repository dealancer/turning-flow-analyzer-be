import boto3
import json
import os
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from botocore.exceptions import ClientError


class DynamoDBService:
    def __init__(self):
        # Check if we have a custom endpoint (for local development)
        endpoint_url = os.environ.get('DYNAMODB_ENDPOINT')
        if endpoint_url:
            self.dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url)
        else:
            self.dynamodb = boto3.resource('dynamodb')

        self.table_name = os.environ.get('DYNAMODB_TABLE', 'analysis-results')
        self.table = self.dynamodb.Table(self.table_name)

    def get_analysis_result(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve analysis result from DynamoDB by URL

        Args:
            url: The URL to look up

        Returns:
            Dictionary containing the analysis result or None if not found
        """
        try:
            response = self.table.get_item(
                Key={'url': url}
            )

            if 'Item' in response:
                item = response['Item']
                # Return the result field which contains the JSON analysis data
                return {
                    'result': item.get('result'),
                    'updated': item.get('updated')
                }

            return None

        except ClientError as e:
            print(f"Error retrieving from DynamoDB: {e}")
            return None

    def save_analysis_result(self, url: str, result: Dict[str, Any]) -> bool:
        """
        Save analysis result to DynamoDB

        Args:
            url: The URL that was analyzed
            result: The analysis result to store

        Returns:
            True if successful, False otherwise
        """
        try:
            # Convert result to JSON string for storage
            result_json = json.dumps(result) if isinstance(result, dict) else result

            # Get current timestamp
            updated = datetime.now(timezone.utc).isoformat()

            self.table.put_item(
                Item={
                    'url': url,
                    'result': result_json,
                    'updated': updated
                }
            )

            return True

        except ClientError as e:
            print(f"Error saving to DynamoDB: {e}")
            return False