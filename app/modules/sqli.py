import requests
import sqlmap
import subprocess

from ..models import ScanDetail
from .utils import create_response_text


def run(url, scan_id, paths):
    sqlmap_cmd = 'sqlmap -u {url} --batch -o'

    for path, path_item in paths.items():
        full_url = f"{url}{path}"
        print(full_url)
        # response = requests.get(full_url)
        # response_text = create_response_text(response)

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
        vulnerabilities = []
        for line in output.decode("utf-8").split("\n"):
            # if "Vulnerability found:" in line:
            if "vulnerab" in line:
                # vulnerability_type = line.split(":")[1].strip()
                # vulnerabilities.append(vulnerability_type)
                vulnerabilities.append(line)

    return vulnerabilities
