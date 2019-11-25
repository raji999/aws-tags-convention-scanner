##
# Author: Daniel Hajduk
##
from aws_resources.AWSResource import AWSResource
import boto3


class Lambda(AWSResource):

    def retrieve_tags_map(self, region, major_tags) -> dict:
        return {}

