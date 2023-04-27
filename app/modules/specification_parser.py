import json
import os


class SpecificationParser:
    def __init__(self, file_path, type=None):
        self.file_path = file_path
        self.type = type
        self.format = format

    def parse_json(self):
        with open(self.file_path, 'r') as file:
            openapi_spec = json.load(file)
            return openapi_spec

    def parse_yaml(self):
        pass

    def parse_postman(self):
        pass

    def parse(self):
        if self.type == 'openapi':
            _, file_extension = os.path.splitext(self.file_path)
            if file_extension == '.json':
                return self.parse_json()
            if file_extension == '.yaml':
                return self.parse_yaml()
        elif self.type == 'postman':
            self.parse_postman()
        else:
            return ''
