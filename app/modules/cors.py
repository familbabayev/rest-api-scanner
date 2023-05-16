import requests
from ..models import ScanDetail
from .utils import create_response_text


def run(url, scan_id):
    response = requests.options(url)
    response_text = create_response_text(response)

    if 'Access-Control-Allow-Origin' in response.headers:
        allowed_origins = response.headers['Access-Control-Allow-Origin']
        if allowed_origins == '*':
            ScanDetail.objects.create(
                vulnerability_id=7,
                scan_id=scan_id,
                issue=f"Vulnerable CORS policy in {url} - All origins are allowed",
                response=response_text,
                url=url,
            )

    return 1
