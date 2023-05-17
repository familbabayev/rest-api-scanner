from ..models import ScanDetail
from .utils import make_request, create_response_text


def run(url, scan):
    response = make_request(url, "OPTIONS", scan.auth_detail)
    response_text = create_response_text(response)

    if 'Access-Control-Allow-Origin' in response.headers:
        allowed_origins = response.headers['Access-Control-Allow-Origin']
        if allowed_origins == '*':
            ScanDetail.objects.create(
                vulnerability_id=7,
                scan_id=scan.id,
                issue=f"Vulnerable CORS policy in {url} - All origins are allowed",
                response=response_text,
                url=url,
            )

    return 1
