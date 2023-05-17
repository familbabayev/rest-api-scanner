import requests


def create_response_text(response):
    return (
        f"Status code: {response.status_code}<br>"
        f"URL: {response.url}<br>"
        f"Encoding: {response.encoding}<br>"
        f"Time elapsed: {response.elapsed}<br>"
        f"Headers: {response.headers}<br>"
        f"Text content: {response.text}<br>"
    )


def make_request(url, method, auth_detail=False, body=None):
    headers = {}
    if auth_detail:
        headers = {"Authorization": auth_detail}

    if method.upper() == "GET":
        auth_request = requests.get(
            url,
            headers=headers,
            allow_redirects=False,
            verify=False,
            timeout=10,
        )
    elif method.upper() == "POST":
        auth_request = requests.post(
            url,
            headers=headers,
            data=body,
            allow_redirects=False,
            verify=False,
            timeout=10,
        )
    elif method.upper() == "PUT":
        auth_request = requests.put(
            url,
            headers=headers,
            data=body,
            allow_redirects=False,
            verify=False,
            timeout=10,
        )
    elif method.upper() == "OPTIONS":
        auth_request = requests.options(
            url, headers=headers, verify=False, timeout=10
        )
    return auth_request
