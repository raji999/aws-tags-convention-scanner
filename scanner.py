##
# Author: Daniel Hajduk
##
import yaml
import os
import click

from aws_resources.AutoScalingGroup import AutoScalingGroup
from aws_resources.EC2Instance import EC2Instance


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
        "EC2Instance": EC2Instance(),
        "AutoScalingGroup": AutoScalingGroup()
    }


def generate_resource_report(aws_resource, grouping_tag, major_tags, retrieved_tags_map):
    # Removing duplication of grouping_tag in major_tags
    major_tags.remove(grouping_tag)

    # TODO add grouping by grouping_id before and itarate over groups

    with open(os.path.join(os.path.dirname(__file__), 'Report_' + aws_resource + '.csv'), 'w+') as report_file:
        # Build header
        header = ['\\']
        tags_map_tmp = []
        for resource_name in retrieved_tags_map:
            header.append(resource_name)
            tags_map_tmp.append(retrieved_tags_map[resource_name])
        report_file.write(','.join(header) + '\n')
        # Build grouping_tag record line
        grouping_tag_record_line = [grouping_tag]
        for retrieved_tags in tags_map_tmp:
            if grouping_tag in retrieved_tags:
                grouping_tag_record_line.append(retrieved_tags[grouping_tag])
            else:
                grouping_tag_record_line.append('Missing')
        report_file.write(','.join(grouping_tag_record_line) + '\n')
        # Build major_tags record lines
        for major_tag in major_tags:
            record_line = [major_tag]
            for retrieved_tags in tags_map_tmp:
                if major_tag in retrieved_tags:
                    record_line.append(retrieved_tags[major_tag])
                else:
                    record_line.append('Missing')
            report_file.write(','.join(record_line) + '\n')


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