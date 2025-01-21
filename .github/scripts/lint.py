import os
import sys
import yaml
import requests


DIR = 'plugins'
FILE_START = 'q2-'
FILE_EXT = '.yml'

KEY_SET = set(['owner', 'name', 'branch', 'docs'])

GITHUB_TOKEN = sys.argv[1]


def lint(yml):
    # Assert corrrect keys
    assert set(yml.keys()) == KEY_SET

    # Get the docs URL assert 200
    response = requests.get(yml['docs'])
    assert response.status_code == 200

    # Put together the owner/name:branch
    # ...Do something with it
    base_url = "https://api.github.com"

    def create_repo(access_token, repo_name, repo_descr=None):
        url = f"{base_url}/user/repos"

        headers = {
            "Authorization": f"token {access_token}",
        }

        # create json data to send using the post request
        data = {
            "name": repo_name,
            "description": repo_descr,
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 201:
            repo_data = response.json()
            return repo_data
        else:
            return None


    access_token = "YOUR ACCESS TOKEN"
    repo_name = "apify_testing"
    repo_descr = "New repo created using the Python GitHub API."

    new_repo = create_repo(access_token, repo_name, repo_descr)

    if new_repo:
        print(f"New public repo created successfully!")
    else:
        print("Failed to create a new repo.")


if __name__ == "__main__":
    files = sys.argv[2:]

    for file in files:
        head, tail = os.path.split(file)
        file_name, file_ext = os.path.splitext(tail)

        # We only care about files added to the plugins dir
        if head == DIR:
            if file_name[0:3] != FILE_START or file_ext != FILE_EXT:
                raise ValueError('File name must conform to q2-*.yml')

            with open(file, 'r') as fh:
                yml = yaml.safe_load(fh)
                lint(yml)
