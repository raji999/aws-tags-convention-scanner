from abc import abstractmethod, ABC


class AWSResource(ABC):

    @abstractmethod
    def retrieve_tags_map(self, region, major_tags) -> dict:
        return {}

    @staticmethod
    def normalize_tags(tags, major_tags) -> dict:
        normalized_tags = {}
        for tag in tags:
            if tag['Key'] in major_tags:
                normalized_tags[tag['Key']] = tag['Value']
        return normalized_tags
