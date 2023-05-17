from ..models import ScanDetail
from .utils import make_request, create_response_text
from urllib.parse import urljoin


def run(url, scan):
    files_to_access = [
        "../../../../etc/passwd",
        "../../../../var/www/html/index.html",
        "../../../../etc/hosts",
    ]

    for file in files_to_access:
        # Create the final URL
        final_url = urljoin(url, file)

        try:
            response = make_request(final_url, "GET", scan.auth_detail)
            response.raise_for_status()
        except Exception:
            continue

        response_text = create_response_text(response)
        if response.status_code == 200:
            # If we got a 200 response, check for some common file contents
            if (
                "/root" in response.text
                or "<html" in response.text
                or "localhost" in response.text
            ):
                ScanDetail.objects.create(
                    vulnerability_id=8,
                    scan_id=scan.id,
                    issue=f"Potential Directory Traversal vulnerability found at {final_url}",
                    response=response_text,
                    url=final_url,
                )

    return 1
