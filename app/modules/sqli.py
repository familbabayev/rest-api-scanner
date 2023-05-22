import requests
import subprocess

from ..models import ScanDetail
from .utils import create_response_text


def run(url, scan, paths):
    sqlmap_cmd = 'sqlmap -u {url} --batch -o'

    for path, path_item in paths.items():
        full_url = f"{url}{path}"

        response = requests.get(full_url)
        response_text = create_response_text(response)

        cmd = sqlmap_cmd.format(url=full_url)

        # Execute the SQLMap command using the subprocess module
        # output = subprocess.check_output(cmd.split())
        proc = subprocess.Popen(
            cmd.split(),
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Wait for the process to finish and capture its output
        output, error = proc.communicate()
        for line in output.decode("utf-8").split("\n"):
            if "vulnerab" in line:
                ScanDetail.objects.create(
                    vulnerability_id=10,
                    scan_id=scan.id,
                    issue=f"SQL Injection found: {line}",
                    response=response_text,
                    url=full_url,
                )

    return 1
