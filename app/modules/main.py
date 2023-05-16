from . import (
    specification_parser,
    sensitive_data_exposure,
    cors,
    path_traversal,
    security_headers,
    sqli,
)


def runTests(file_path, type, scan_id):
    spec_parser = specification_parser.SpecificationParser(
        file_path=file_path, type=type
    )
    openapi_spec = spec_parser.parse()

    paths = openapi_spec.get('paths', {})
    base_url = openapi_spec.get('servers')[0]['url']

    security_headers.run(base_url, scan_id)
    print("----------------1")
    sensitive_data_exposure.run(base_url, scan_id, paths)
    print("----------------2")
    cors.run(base_url, scan_id)
    print("----------------3")
    path_traversal.run(base_url, scan_id)
    print("----------------4")

    # sqli.run(base_url, scan_id, paths)

    return 1
