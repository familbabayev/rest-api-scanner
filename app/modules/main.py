from . import ssrf
from . import sqli
from . import security_headers
from .specification_parser import SpecificationParser


def runTests(file_path, type, scan_id):
    results = []
    print('some')
    spec_parser = SpecificationParser(file_path=file_path, type=type)
    openapi_spec = spec_parser.parse()

    paths = openapi_spec.get('paths', {})
    base_url = openapi_spec.get('servers')[0]['url']
    # print(paths)
    print(base_url)

    res1 = security_headers.run(base_url, scan_id)
    results.extend(res1)
    # temp = []
    # for path, path_item in paths.items():
    #     print(f"Path: {path}")
    #     url = f"{base_url}{path}"
    #     temp = sqli.run(url)

    return results
