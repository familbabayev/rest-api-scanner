from . import ssrf
from . import sqli
from .specification_parser import SpecificationParser


def runTests(file_path, type):
    spec_parser = SpecificationParser(file_path=file_path, type=type)
    openapi_spec = spec_parser.parse()

    paths = openapi_spec.get('paths', {})
    base_url = openapi_spec.get('servers')[0]['url']
    # print(paths)
    # print(base_url)

    temp = []
    for path, path_item in paths.items():
        print(f"Path: {path}")
        url = f"{base_url}{path}"
        temp = sqli.run(url)

    return temp
