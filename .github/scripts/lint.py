import os
import sys
import yaml
import requests


DIR = 'plugins'
FILE_START = 'q2-'
FILE_EXT = '.yml'

KEY_SET = set(['owner', 'name', 'branch', 'docs'])


def lint(yml):
    # Assert corrrect keys
    assert set(yml.keys()) == KEY_SET

    # Get the docs URL assert 200
    response = requests.get(yml['docs'])
    assert response.status_code == 200

    # Put together the owner/name:branch
    # ...Do something with it


if __name__ == "__main__":
    files = sys.argv[1:]

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
