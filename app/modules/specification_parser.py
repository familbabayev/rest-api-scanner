import json
import yaml


class SpecificationParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.format = format

    def parse_json(self):
        with open(self.file_path, 'r') as file:
            openapi_spec = json.load(file)
            return openapi_spec

    def parse_yaml(self):
        with open(self.file_path, 'r') as file:
            openapi_spec = yaml.safe_load(file)
            return openapi_spec

    def parse(self):
        if self.file_path.endswith('.json'):
            return self.parse_json()
        elif self.file_path.endswith('.yaml') or self.file_path.endswith(
            '.yml'
        ):
            return self.parse_yaml()
        else:
            raise ValueError('Unsupported file type')
