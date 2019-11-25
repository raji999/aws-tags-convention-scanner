##
# Author: Daniel Hajduk
##
import yaml
import os
import click
import collections

from aws_resources.AutoScalingGroup import AutoScalingGroup
from aws_resources.EC2Instance import EC2Instance
from aws_resources.KinesisStream import KinesisStream


def load_config(file) -> dict:
    if os.path.sep in file:
        with open(file, 'r') as config:
            return yaml.full_load(config)
    else:
        with open(os.path.join(os.path.dirname(__file__), file), 'r') as config:
            return yaml.full_load(config)


def validate_config(config):
    if 'scan' not in config:
        raise Exception('Missing "scan" property of config')
    if 'region' not in config:
        raise Exception('Missing "region" property of config')
    for scan_entry in config['scan']:
        if 'resource' not in scan_entry or 'grouping_tag' not in scan_entry or 'tags' not in scan_entry:
            raise Exception('Missing scan entry properties (resource, grouping_tag or tags)')


def initialize_retrievers() -> dict:
    return {
        'EC2Instance': EC2Instance(),
        'AutoScalingGroup': AutoScalingGroup(),
        'KinesisStream': KinesisStream()
    }


def prepare_headers(tags) -> list:
    headers = ['\\']
    for tag in tags:
        headers.append(tag['Name'])
    return headers


def prepare_grouped_tags(grouping_tag, retrieved_tags_map) -> dict:
    tags_only = []
    for resource_name in retrieved_tags_map:
        tags = retrieved_tags_map[resource_name]
        if 'Name' not in tags:
            tags['Name'] = resource_name
        if grouping_tag not in tags:
            tags[grouping_tag] = 'Missing'
        tags_only.append(tags)
    grouped_tags = collections.defaultdict(list)
    for item in tags_only:
        grouped_tags[item[grouping_tag]].append(item)
    return grouped_tags


def generate_resource_report(aws_resource, grouping_tag, major_tags, retrieved_tags_map):
    major_tags.remove(grouping_tag)
    grouped_tags = prepare_grouped_tags(grouping_tag, retrieved_tags_map)
    with open(os.path.join(os.path.dirname(__file__), 'Report_' + aws_resource + '.csv'), 'w+') as report_file:
        for gtag, tags in grouped_tags.items():
            # Build headers record line
            headers = prepare_headers(tags)
            report_file.write(','.join(headers) + '\n')

            # Build grouping_tag record line
            # this is to ensure that grouping_tag will be always first on records table
            gtag_list = [grouping_tag]
            gtag_list.extend([sub[grouping_tag] for sub in tags])
            report_file.write(','.join(gtag_list) + '\n')

            # Build major_tags record lines
            for major_tag in major_tags:
                record_line = [major_tag]
                for retrieved_tags in tags:
                    if major_tag in retrieved_tags:
                        record_line.append(retrieved_tags[major_tag])
                    else:
                        record_line.append('Missing')
                report_file.write(','.join(record_line) + '\n')

            # this is to separate grouping_tag tables from each other
            report_file.write('\n\n')


@click.group()
def main():
    pass


@main.command()
@click.option('--config-file', required=False, default='scanner.cfg', help='Specify the file containing scanner configuration')
def main(config_file):
    try:
        config = load_config(config_file)
        validate_config(config)
        retrievers = initialize_retrievers()

        for scan_entry in config['scan']:
            aws_resource = scan_entry['resource']
            grouping_tag = scan_entry['grouping_tag']
            major_tags = scan_entry['tags']
            retrieved_tags_map = retrievers[aws_resource].retrieve_tags_map(config['region'], major_tags)
            generate_resource_report(aws_resource, grouping_tag, major_tags, retrieved_tags_map)
    except Exception as e:
        print(e)
        print('Time to OIL UP!!!')


if __name__ == '__main__':
    main()