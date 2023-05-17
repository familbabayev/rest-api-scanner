from ..models import ScanDetail
from .utils import make_request, create_response_text


def run(url, scan):
    security_headers = [
        (1, "X-XSS-Protection"),
        (2, "X-Content-Type-Options"),
        (3, "X-Frame-Options"),
        (4, "Content-Security-Policy"),
        (5, "Strict-Transport-Security"),
    ]

    response = make_request(url, "GET", scan.auth_detail)
    response_text = create_response_text(response)

    for id, header in security_headers:
        if header not in response.headers:
            ScanDetail.objects.create(
                vulnerability_id=id,
                scan_id=scan.id,
                issue=f"{header} header is missing",
                response=response_text,
                url=url,
            )

    if 'Server' in response.headers:
        ScanDetail.objects.create(
            vulnerability_id=9,
            scan_id=scan.id,
            issue=f"Server version disclosed: {response.headers['Server']}",
            response=response_text,
            url=url,
        )

    return 1
