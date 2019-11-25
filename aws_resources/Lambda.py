##
# Author: Daniel Hajduk
##
from aws_resources.AWSResource import AWSResource
import boto3


class Lambda(AWSResource):

    DEFAULT_PAGE_SIZE = 25

    def retrieve_tags_map(self, region, major_tags) -> dict:
        retrieved_tags_map = {}
        marker = None
        while True:
            marker, partial_tags_map = Lambda.get_functions_with_tags(marker, region, major_tags)
            retrieved_tags_map.update(partial_tags_map)
            if marker is None:
                break

        return retrieved_tags_map

    @staticmethod
    def get_functions_with_tags(marker, region, major_tags):
        client = boto3.client('lambda', region_name=region)
        if marker is not None:
            response = client.list_functions(
                #MasterRegion=region,
                Marker=marker,
                MaxItems=Lambda.DEFAULT_PAGE_SIZE
            )
        else:
            response = client.list_functions(
               # MasterRegion=region,
                MaxItems=Lambda.DEFAULT_PAGE_SIZE
            )
        partial_tags_map = {}
        for function in response['Functions']:
            response_t = client.list_tags(
                Resource=function['FunctionArn']
            )
            partial_tags_map[function['FunctionName']] = Lambda.normalize_lambda_tags(response_t['Tags'], major_tags)

        if 'NextMarker' in response:
            return response['NextMarker'], partial_tags_map
        return None, partial_tags_map

    @staticmethod
    def normalize_lambda_tags(tags, major_tags):
        normalized_tags = {}
        for tag in tags:
            if tag in major_tags:
                normalized_tags[tag] = tags[tag]
        return normalized_tags
