##
# Author: Daniel Hajduk
##
from aws_resources.AWSResource import AWSResource
import boto3


class KinesisStream(AWSResource):
    DEFAULT_STREAMS_LIMIT = 200
    DEFAULT_STREAMS_TAG_LIMIT = 10

    def retrieve_tags_map(self, region, major_tags) -> dict:
        return self.list_streams_with_tags(region, major_tags)

    @staticmethod
    def list_streams_with_tags(region, major_tags) -> dict:
        client = boto3.client('kinesis', region_name=region)
        response = client.list_streams(
            Limit=KinesisStream.DEFAULT_STREAMS_LIMIT
        )
        streams_with_tags = {}
        for stream_name in response['StreamNames']:
            response_t = client.list_tags_for_stream(
                StreamName=stream_name,
                Limit=KinesisStream.DEFAULT_STREAMS_TAG_LIMIT
            )
            streams_with_tags[stream_name] = AWSResource.normalize_tags(response_t['Tags'], major_tags)
        return streams_with_tags
