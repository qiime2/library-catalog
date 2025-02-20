import os
import re
import sys
import yaml
import requests


DIR = 'plugins'

KEY_SET = set(['owner', 'name', 'branch', 'docs'])
ENV_FILE_REGEX = r'.*-qiime2-.*-20[0-9][0-9]\.([1-9]|1[0-2])\.yml'
GITHUB_BASE_URL = "https://api.github.com"

GITHUB_TOKEN = sys.argv[1]
GITHUB_BASE_URL = 'https://api.github.com'
GITHUB_HEADERS = {
    'Authorization': f'token: {GITHUB_TOKEN}',
    'X-GitHub-Api-Version': '2022-11-28'
}

# TODO:
# 1. Yell if there is no description
# 2. Yell if there is no README
# 3. Yell if there are no env files X
def lint(yml):
    plugin_env_urls = []

    # Assert corrrect keys
    assert set(yml.keys()) == KEY_SET

    # Get the docs URL assert 200
    response = requests.get(yml['docs'])
    assert response.status_code == 200

    # Used for all requests for this repo
    base_url = f'{GITHUB_BASE_URL}/repos/{yml['owner']}/{yml['name']}'

    # Get env files
    env_files_url = f'{base_url}/contents/environment-files'
    env_files_query_params = {
        'owner': yml['owner'],
        'repo': yml['name'],
        'ref': yml['branch'],
        'path': '/environment-files/'
    }

    # Get all files in the /environment-files/ folder
    response = requests.get(env_files_url, headers=GITHUB_HEADERS, params=env_files_query_params)
    if response.ok:
        envs = response.json()

        # If the file matches the regex to be a QIIME 2 environment-file then keep
        # track of its download URL
        for env in envs:
            if re.search(ENV_FILE_REGEX, env['name']) is not None:
                plugin_env_urls.append(env['download_url'])

        if plugin_env_urls == []:
            raise ValueError(f'No QIIME 2 environment files found for repo: {yml["owner"]}:{yml["name"]}.')
    else:
        raise ValueError(f'No environment-files directory found in repo: {yml["owner"]}:{yml["name"]}.\nGot response {response.json()}')

    return plugin_env_urls


if __name__ == "__main__":
    GITHUB_TOKEN = sys.argv[1]
    files = sys.argv[2:]

    all_env_urls = []

    # There will be at least one of these because we only run the action if the
    # PR did something to plugins/**.yml
    for file in files:
        head, tail = os.path.split(file)
        file_name, file_ext = os.path.splitext(tail)

        # We only care about files added to the plugins dir
        if head == DIR:
            with open(file, 'r') as fh:
                yml = yaml.safe_load(fh)
                all_env_urls.extend(lint(yml))

    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        fh.write(f'ENV_FILES={all_env_urls}\n')
