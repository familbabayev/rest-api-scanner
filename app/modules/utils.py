def create_response_text(response):
    return (
        f"Status code: {response.status_code}<br>"
        f"URL: {response.url}<br>"
        f"Encoding: {response.encoding}<br>"
        f"Time elapsed: {response.elapsed}<br>"
        f"Headers: {response.headers}<br>"
        f"Text content: {response.text}<br>"
    )
