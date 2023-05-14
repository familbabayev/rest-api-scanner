import requests
from ..models import ScanDetail


def run(url, scan_id):
    results = []

    security_headers = [
        "X-XSS-Protection",
        "X-Content-Type-Options",
        "X-Frame-Options",
        "Content-Security-Policy",
        "Strict-Transport-Security",
    ]

    response = requests.get(url)
    print("RESPONSE", response.text)

    for header in security_headers:
        if header not in response.headers:
            # vulnerability = Vulnerability.objects.get(title=header)
            ScanDetail.objects.create(vulnerability_id=1, scan_id=scan_id)

            results.append(header)
            print(f"{header} header is missing")

    return results
