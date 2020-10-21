import argparse
import os
import subprocess
import sys
import ssl
import urllib.request
import tarfile

parser = argparse.ArgumentParser()

parser.add_argument(
    '--name',
    required=True,
)

parser.add_argument(
    '--url',
    required=True,
)

parser.add_argument(
    '--token',
    required=True,
)

args = parser.parse_args()

name = args.name
url = args.url
token = args.token

actions_runner_path = f"./actions-runner-{name}"

def actions_runner_install(actions_runner_path):
    os.mkdir(actions_runner_path)
    tf = f"./{actions_runner_path}/actions-runner-linux-x64-2.273.5.tar.gz"
    ssl._create_default_https_context = ssl._create_unverified_context
    urllib.request.urlretrieve(
        "https://github.com/actions/runner/releases/download/v2.273.5/actions-runner-linux-x64-2.273.5.tar.gz",
        tf
    )

    with tarfile.open(tf) as f:
        f.extractall(actions_runner_path)

def actions_runner_config(actions_runner_path, url, token):
    return subprocess.call([
        f"{actions_runner_path}/config.sh",
        "--url", url,
        "--token", token
    ])

if not os.path.isdir(actions_runner_path):
    actions_runner_install(actions_runner_path)

if os.path.isdir(actions_runner_path + ".runner"):
    raise FileExistsError(
        "`.runner` config file already present, if you want to start a runner"
        "then use the `run` app."
    )

exit_code = actions_runner_config(actions_runner_path, url, token)

sys.exit(exit_code)
