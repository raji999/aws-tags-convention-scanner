##
# Author: Daniel Hajduk
##
import yaml
import os
import click

from aws_resources.AutoScalingGroup import AutoScalingGroup
from aws_resources.EC2Instance import EC2Instance
from aws_resources.KinesisStream import KinesisStream
from aws_resources.Lambda import Lambda
from generators.LinesReportGenerator import LinesReportGenerator
from generators.TableReportGenerator import TableReportGenerator


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
    if 'report_format' not in config:
        raise Exception('Missing "report_format" property of config')
    for scan_entry in config['scan']:
        if 'resource' not in scan_entry or 'grouping_tag' not in scan_entry or 'tags' not in scan_entry:
            raise Exception('Missing scan entry properties (resource, grouping_tag or tags)')


def initialize_retrievers() -> dict:
    return {
        'EC2Instance': EC2Instance(),
        'AutoScalingGroup': AutoScalingGroup(),
        'KinesisStream': KinesisStream(),
        'Lambda': Lambda()
    }


def initialize_report_generators() -> dict:
    return {
        'table': TableReportGenerator(),
        'lines': LinesReportGenerator()
    }


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
        generators = initialize_report_generators()
        generator = generators[config['report_format']]

        for scan_entry in config['scan']:
            aws_resource = scan_entry['resource']
            grouping_tag = scan_entry['grouping_tag']
            major_tags = scan_entry['tags']
            retrieved_tags_map = retrievers[aws_resource].retrieve_tags_map(config['region'], major_tags)
            generator.generate_report(aws_resource, grouping_tag, major_tags, retrieved_tags_map)
    except Exception as e:
        print(e)
        print('Time to OIL UP!!!')


if __name__ == '__main__':
    main()
