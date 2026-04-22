import json
import os
import re
import sys
from pathlib import Path
from urllib.request import urlopen

import yaml


PACKAGES_CHANNEL_RE = re.compile(
    r'^https://packages\.qiime2\.org/qiime2/'
    r'(?P<epoch>20[0-9]{2}\.[0-9]+)/'
    r'(?P<distro>[^/]+)/'
    r'(?P<stage>staged|passed|released)/?$'
)

PLATFORM_CONFIGS = (
    {
        'platform_label': 'linux-64',
        'runner_label': 'ubuntu-latest',
        'conda_architecture': 'x64',
        'patterns': (
            'rachis-{distro}-linux-64-conda.yml',
            'qiime2-{distro}-ubuntu-latest-conda.yml',
        ),
    },
    {
        'platform_label': 'osx-64',
        'runner_label': 'macos-15-intel',
        'conda_architecture': 'x64',
        'patterns': (
            'rachis-{distro}-osx-64-conda.yml',
            'qiime2-{distro}-macos-latest-conda.yml',
        ),
    },
    {
        'platform_label': 'osx-arm64',
        'runner_label': 'macos-15',
        'conda_architecture': 'arm64',
        'patterns': (
            'rachis-{distro}-osx-arm64-conda.yml',
        ),
    },
)


def _load_env(url):
    with urlopen(url) as response:
        return yaml.safe_load(response.read())


def _get_packages_channel(env, url):
    for channel in env.get('channels', []):
        if not isinstance(channel, str):
            continue

        match = PACKAGES_CHANNEL_RE.match(channel.rstrip('/'))
        if match is not None:
            return match.groupdict()

    raise ValueError(
        f"Could not determine distro channel from environment file: {url}"
    )


def _get_platforms(url, distributions_root):
    env = _load_env(url)
    channel = _get_packages_channel(env, url)
    epoch = channel['epoch']
    distro = channel['distro']
    stage = channel['stage']

    distro_dir = distributions_root / epoch / distro / stage
    if not distro_dir.exists():
        raise ValueError(
            f"Expected distro directory '{distro_dir}' for environment file "
            f"'{url}', but it does not exist."
        )

    matrix_entries = []
    for config in PLATFORM_CONFIGS:
        for pattern in config['patterns']:
            filename = pattern.format(distro=distro)
            if (distro_dir / filename).exists():
                matrix_entries.append({
                    'url': url,
                    'epoch': epoch,
                    'distro': distro,
                    'stage': stage,
                    'platform_label': config['platform_label'],
                    'runner_label': config['runner_label'],
                    'conda_architecture': config['conda_architecture'],
                })
                break

    if not matrix_entries:
        raise ValueError(
            f"No supported released environment files were found in "
            f"'{distro_dir}' for environment file '{url}'."
        )

    return matrix_entries


def main(urls_json, distributions_root):
    urls = json.loads(urls_json)
    distributions_root = Path(distributions_root)

    include = []
    seen = set()

    for url in urls:
        for entry in _get_platforms(url, distributions_root):
            key = (entry['url'], entry['platform_label'])
            if key in seen:
                continue
            seen.add(key)
            include.append(entry)

    if not include:
        raise ValueError('No environment files were found to test.')

    include.sort(
        key=lambda entry: (
            entry['distro'],
            entry['epoch'],
            entry['url'],
            entry['platform_label'],
        )
    )

    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        fh.write(f"matrix={json.dumps({'include': include})}\n")


if __name__ == '__main__':
    main(*sys.argv[1:])
