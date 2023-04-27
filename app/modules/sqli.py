import requests
import sqlmap

import subprocess


def run(url):
    sqlmap_cmd = 'sqlmap -u {url} --risk {risk_level} --level {level}'

    cmd = sqlmap_cmd.format(url=url, risk_level=3, level=5)

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
