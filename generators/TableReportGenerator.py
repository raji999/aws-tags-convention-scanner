##
# Author: Daniel Hajduk
##
import collections
import os

from generators.ReportGenerator import ReportGenerator


class TableReportGenerator(ReportGenerator):

    def generate_report(self, aws_resource, grouping_tag, major_tags, retrieved_tags_map):
        major_tags.remove(grouping_tag)
        grouped_tags = self.prepare_grouped_tags(grouping_tag, retrieved_tags_map)
        with open(os.path.join(os.path.dirname(__file__), 'Report_' + aws_resource + '.csv'), 'w+') as report_file:
            for gtag, tags in grouped_tags.items():
                # Build headers record line
                headers = self.prepare_headers(tags)
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

    @staticmethod
    def prepare_headers(tags) -> list:
        headers = ['\\']
        for tag in tags:
            headers.append(tag['Name'])
        return headers

    @staticmethod
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
