##
# Author: Daniel Hajduk
##
import os

from generators.ReportGenerator import ReportGenerator


class LinesReportGenerator(ReportGenerator):

    def generate_report(self, aws_resource, grouping_tag, major_tags, retrieved_tags_map):
        with open(os.path.join(os.path.dirname(__file__), 'Report_' + aws_resource + '.csv'), 'w+') as report_file:
            headers = ['Name']
            for tag in major_tags:
                headers.append(tag)
            report_file.write(','.join(headers) + '\n')
            for name in retrieved_tags_map:
                record = [name]
                for tag in major_tags:
                    if tag in retrieved_tags_map[name]:
                        record.append(retrieved_tags_map[name][tag])
                    else:
                        record.append('Missing')
                report_file.write(','.join(record) + '\n')
