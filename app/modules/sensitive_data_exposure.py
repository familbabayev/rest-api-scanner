import requests, re
from ..models import ScanDetail
from .utils import create_response_text


def run(url, scan_id, paths):
    sensitive_data_patterns = [
        r'\d{3}-\d{2}-\d{4}',  # SSN
        r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z|a-z]{2,7}\b',  # Email
        r'\b4[0-9]{12}(?:[0-9]{3})?\b',  # Visa Card
        r'\b5[1-5][0-9]{14}\b',  # MasterCard
        r'\b3[47][0-9]{13}\b',  # American Express Card
        r'\b6(?:011|5[0-9]{2})[0-9]{12}\b',  # Discover Card
        r'\b35(?:2[89]|[3-8][0-9])[0-9]{12}\b',  # JCB Card
        r'\b(?:2131|1800|35\d{3})\d{11}\b',  # JCB Card
        r'\b[2-9][0-9]{3}-(0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9]|3[01])\b',  # Date of Birth
        r'\b(?:[0-9]{3}-){2}[0-9]{4}\b',  # Phone number (US format)
        r'([0-9]{1,3}(\.[0-9]{1,3}){3})',  # IP Address
        r'(\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}\b)',  # IP Address with port
        r'((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,})',  # Strong Password
    ]

    response = requests.get(url)
    response_text = create_response_text(response)

    if 'https' not in response.url:
        ScanDetail.objects.create(
            vulnerability_id=6,
            scan_id=scan_id,
            issue=f"Data might not be encrypted! HTTPS is not used. {response.url}",
            response=response_text,
            url=response.url,
        )

    for path, path_item in paths.items():
        full_url = f"{url}{path}"
        print(full_url)
        response = requests.get(full_url)
        response_text = create_response_text(response)

        for pattern in sensitive_data_patterns:
            if re.search(pattern, response.text):
                ScanDetail.objects.create(
                    vulnerability_id=6,
                    scan_id=scan_id,
                    issue=f"Sensitive data might be exposed! Found pattern: {pattern}",
                    response=response_text,
                    url=full_url,
                )

    return 1
