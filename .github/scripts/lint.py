import os
import re
import sys
import yaml
import requests


KEY_SET = set(['owner', 'name', 'branch', 'docs'])


ENV_FILE_REGEX = '.*-qiime2-.*-20[0-9][0-9]\.([1-9]|1[0-2])\.yml'
env_urls = []


def lint(yml):
    # Assert corrrect keys
    assert set(yml.keys()) == KEY_SET

    # Get the docs URL assert 200
    response = requests.get(yml['docs'])
    assert response.status_code == 200

    # Put together the owner/name:branch
    # ...Do something with it
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

    response = requests.get(url, headers=headers, params=query_params)
    envs = response.json()

    for env in envs:
        if re.search(ENV_FILE_REGEX, env.name) is not None:
            env_urls.append(env['download_url'])


if __name__ == "__main__":
    files = sys.argv[1:]

    for file in files:
        with open(file, 'r') as fh:
            yml = yaml.safe_load(fh)
            lint(yml)
