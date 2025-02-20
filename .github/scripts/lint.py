import os
import re
import sys
import yaml
import requests


DIR = 'plugins'

EXPECTED_KEY_SET = set(['owner', 'name', 'branch', 'docs'])
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
# 2. Yell if there is no README X
# 3. Yell if there are no env files X

# Load yml, lint it, return loaded yaml if it passes lint
def _lint_yml(file):
    with open(file, 'r') as fh:
        yml = yaml.safe_load(fh)

    key_set = set(yml.keys())

    if diff := EXPECTED_KEY_SET.difference(key_set):
        raise ValueError(
            f"File '{file}' is missing the following key(s): {diff}")

    if len(key_set) != len(yml.keys()):
        raise ValueError(
            f"File '{file}' contains one or more duplicate keys.")

    response = requests.get(yml['docs'])
    if not response.ok:
        raise ValueError(
            f"File '{file}' docs failed to fetch.\n"
            f"Got response {response.json()}")

    return yml


# Make sure the repo exists and has a description
def _check_description(base_url, base_query_params, repo_name):
    response = requests.get(
        base_url, header=GITHUB_HEADERS, params=base_query_params)

    if not response.ok:
        raise ValueError(f'Failed to get repo: {repo_name}.\n'
                         f'Got response {response.json()}')

    repo_overview = response.json()
    if repo_overview['data']['description'] == '':
        raise ValueError(f'No description found for repo: {repo_name}')


# Make sure the repo has a README
def _check_readme(base_url, base_query_params, repo_name):
    readme_url =f'{base_url}/readme'

    response = requests.get(
        readme_url, headers=GITHUB_HEADERS, params=base_query_params)
    if not response.ok:
        raise ValueError(
            f'Failed to get README for repo: {repo_name}.\n'
            f'Got response {response.json()}')


# Make sure the repo has env files and return a list of their download URLs
def _get_env_files(base_url, base_query_params, repo_name):
    plugin_env_urls = []

    env_files_url = f'{base_url}/contents/environment-files'
    env_files_query_params = {
        **base_query_params,
        'path': '/environment-files/'
    }

    # Get all files in the /environment-files/ folder
    response = requests.get(
        env_files_url, headers=GITHUB_HEADERS, params=env_files_query_params)
    if response.ok:
        envs = response.json()

        # If the file matches the regex to be a QIIME 2 environment-file then
        # keep track of its download URL
        for env in envs:
            if re.search(ENV_FILE_REGEX, env['name']) is not None:
                plugin_env_urls.append(env['download_url'])

        if plugin_env_urls == []:
            raise ValueError(
                f'No QIIME 2 environment files found for repo: {repo_name}.')
    else:
        raise ValueError(
            f'No environment-files directory found in repo: {repo_name}.\n'
            f'Got response {response.json()}')

    return plugin_env_urls


if __name__ == "__main__":
    GITHUB_TOKEN = sys.argv[1]
    files = sys.argv[2:]

    all_env_urls = []

    # There will be at least one of these because we only run the action if the
    # PR did something to plugins/**.yml
    for file in files:
        head, _ = os.path.split(file)

        # We only care about files added to the plugins dir
        if head == DIR:
            yml = _lint_yml(file)

            # Used for all requests for this repo
            repo_name = f'{yml['owner']}/{yml['name']}'
            base_url = f'{GITHUB_BASE_URL}/repos/{yml['owner']}/{yml['name']}'
            base_query_params = {
                'owner': yml['owner'],
                'repo': yml['name'],
                'ref': yml['branch'],
            }

            _check_description(base_url, base_query_params, repo_name)
            _check_readme(base_url, base_query_params, repo_name)
            plugin_env_urls = \
                _get_env_files(base_url, base_query_params, repo_name)
            all_env_urls.extend(plugin_env_urls)

    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        fh.write(f'ENV_FILES={all_env_urls}\n')
