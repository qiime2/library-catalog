import os
import sys
import yaml
import requests


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

        # We only care about files added to the plugins dir
        if head == 'plugins':
            if tail[0:3] != 'q2-' or tail[-4:] != '.yml':
                raise ValueError('File name must conform to q2-*.yml')

            with open(file, 'r') as fh:
                yml = yaml.safe_load(fh)
                lint(yml)
