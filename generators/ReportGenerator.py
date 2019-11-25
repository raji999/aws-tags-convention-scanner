##
# Author: Daniel Hajduk
##
from abc import abstractmethod, ABC


class ReportGenerator(ABC):

    @abstractmethod
    def generate_report(self, aws_resource, grouping_tag, major_tags, retrieved_tags_map):
        print('generated')
