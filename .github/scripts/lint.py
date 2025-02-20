import os
import re
import sys
import yaml
import requests


DIR = 'plugins'

KEY_SET = set(['owner', 'name', 'branch', 'docs'])
ENV_FILE_REGEX = '.*-qiime2-.*-20[0-9][0-9]\.([1-9]|1[0-2])\.yml'
GITHUB_BASE_URL = "https://api.github.com"

env_urls = []

GITHUB_TOKEN = sys.argv[1]
GITHUB_BASE_URL = 'https://api.github.com'


def lint(yml):
    # Assert corrrect keys
    assert set(yml.keys()) == KEY_SET

    # Get the docs URL assert 200
    response = requests.get(yml['docs'])
    assert response.status_code == 200

    # Put together the owner/name:branch
    url = f'{GITHUB_BASE_URL}/repos/{yml['owner']}/{yml['name']}/contents/environment-files'
    headers = {
        'Authorization': f'token: {GITHUB_TOKEN}',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    query_params = {
        'owner': yml['owner'],
        'repo': yml['name'],
        'ref': yml['branch'],
        'path': '/environment-files/'
    }

    # Get all files in the /environment-files/ folder
    response = requests.get(url, headers=headers, params=query_params)
    envs = response.json()

    # If the file matches the regex to be a QIIME 2 environment-file then keep
    # track of its download URL
    for env in envs:
        if re.search(ENV_FILE_REGEX, env['name']) is not None:
            env_urls.append(env['download_url'])


if __name__ == "__main__":
    GITHUB_TOKEN = sys.argv[1]
    files = sys.argv[2:]

    for file in files:
        head, tail = os.path.split(file)
        file_name, file_ext = os.path.splitext(tail)

        # We only care about files added to the plugins dir
        if head == DIR:
            with open(file, 'r') as fh:
                yml = yaml.safe_load(fh)
                lint(yml)

    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        fh.write(f'ENV_FILES={env_urls}\n')
