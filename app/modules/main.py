from . import (
    specification_parser,
    sensitive_data_exposure,
    cors,
    path_traversal,
    security_headers,
    sqli,
)


def runTests(file_path, scan):
    spec_parser = specification_parser.SpecificationParser(file_path=file_path)
    openapi_spec = spec_parser.parse()

    paths = openapi_spec.get('paths', {})
    base_url = openapi_spec.get('servers')[0]['url']

    if scan.scan_type == "Quick":
        security_headers.run(base_url, scan)
        sensitive_data_exposure.run(base_url, scan, paths)
        cors.run(base_url, scan)
        path_traversal.run(base_url, scan)

    else:
        security_headers.run(base_url, scan)
        sensitive_data_exposure.run(base_url, scan, paths)
        cors.run(base_url, scan)
        path_traversal.run(base_url, scan)
        sqli.run(base_url, scan, paths)

    return 1
