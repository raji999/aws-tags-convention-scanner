##
# Author: Daniel Hajduk
##
from aws_resources.AWSResource import AWSResource


class EC2Instance(AWSResource):

    # TODO
    def retrieve_tags_map(self, region, major_tags) -> dict:
        return {}
