##
# Author: Daniel Hajduk
##
import boto3
from aws_resources.AWSResource import AWSResource


class AutoScalingGroup(AWSResource):

    DEFAULT_MAX_RECORDS = 25

    def retrieve_tags_map(self, region, major_tags) -> dict:
        retrieved_tags_map = {}
        next_token = None
        while True:
            next_token, partial_tags_map = AutoScalingGroup.describe_autoscaling_groups(region, next_token, major_tags)
            retrieved_tags_map.update(partial_tags_map)
            if next_token is None:
                break

        return retrieved_tags_map

    @staticmethod
    def describe_autoscaling_groups(region, next_token, major_tags):
        client = boto3.client('autoscaling', region_name=region)
        if next_token is not None:
            response = client.describe_auto_scaling_groups(
                NextToken=next_token,
                MaxRecords=AutoScalingGroup.DEFAULT_MAX_RECORDS
            )
        else:
            response = client.describe_auto_scaling_groups(
                MaxRecords=AutoScalingGroup.DEFAULT_MAX_RECORDS
            )
        partial_tags_map = {}
        for asg in response['AutoScalingGroups']:
            if 'DefaultVpc' not in asg['AutoScalingGroupName']:
                partial_tags_map[asg['AutoScalingGroupName']] = AutoScalingGroup.normalize_tags(asg['Tags'], major_tags)

        if 'NextToken' in response:
            return response['NextToken'], partial_tags_map
        return None, partial_tags_map
