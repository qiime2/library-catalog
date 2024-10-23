# Library-plugins
Stores a list of the plugins that are included in the QIIME 2 library.

# How to add a plugin
Your plugin must exist as a GitHub repo.

Simply open a PR adding a `<my-plugin-name>.yml` file to the `plugins` folder. This file must have the following `key: value` pairs:

```
owner: <repo-owner>
name: <repo-name>
branch: <target-branch>
docs: <latest-docs-url>
```

# Requirements for added plugins

As stated previously, plugins aded to QIIME 2 Library must exist as GitHub repos. This is because the QIIME 2 Library uses the GitHub REST API to retrieve information about your plugin. You need to ensure your plugin has the following.

## A GitHub about section

This will be used as the short description for your plugin in library. It should be 300 or so characters max and should describe what your plugin is.

## A top level README.md

This will be rendered as MarkDown on library, and should give a detailed description of your plugin and what it does.

NOTE: If your readme references any resources using paths relative to the root of your repository these resources WILL NOT LOAD on QIIME 2 Library. Only resources referenced with absolute URLs will load. This is because we are not cloning and rehosting your assets.

## A top level environment-files directory

Additionally, all repos in the QIIME 2 library must have conda environment.yml files for each supported QIIME 2 release with the following naming scheme `<plugin-name>-qiime2-<distro>-<epoch>.yml`. These files must be located in the `/environment-files` folder.

### Additional Requirements

1. Your plugin must be fully installable via these environment files with no extra steps required.
2. Your environment files must NOT contain a `name` field. The end user is expected to provide the name on the command line when they install.
