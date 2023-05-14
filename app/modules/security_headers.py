import requests
from ..models import ScanDetail


def run(url, scan_id):
    results = []

    security_headers = [
        (1, "X-XSS-Protection"),
        (2, "X-Content-Type-Options"),
        (3, "X-Frame-Options"),
        (4, "Content-Security-Policy"),
        (5, "Strict-Transport-Security"),
    ]

    response = requests.get(url)
    print("RESPONSE", response.text)

    for id, header in security_headers:
        if header not in response.headers:
            ScanDetail.objects.create(vulnerability_id=id, scan_id=scan_id)

            results.append(header)
            print(f"{header} header is missing")

    return results
