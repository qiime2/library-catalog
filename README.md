# Library-plugins
Stores a list of the plugins that are included in the QIIME 2 library.

# How to add a plugin
Your plugin must exist as a GitHub repo.

Simply open a PR adding a `<my-plugin-name>.yml` file to the `plugins` folder. This file must have the following `key: value` pairs:

```
owner: <repo-owner>
name: <repo-name>
branch: <target-branch>
```

# Requirements for added plugins

As stated previously, plugins aded to QIIME 2 Library must exist as GitHub repos. In addtiong, plugins added to the QIIME 2 library are required to contain the following directory structure.

```
/.qiime2/library/
                |_info.yml
                |_/environments/
                               |_<plugin-name>-qiime2-<distro>-<epoch>.yml
                               |_...
```

The top level of the repo must contain a `.qiime2` folder which must contain a `library` folder. The library folder must contain an `info.yml` file and an `environments` folder.

## info.yml

This file must have the following `key: value` pairs:

```yaml
short_description: Ideally 300 character or less description of what the plugin is and does.
long_description_path: A path relative to the root of the repo to a MarkDown formatted file describing the plugin in more depth. This can simply be the repo's README if you want, or you can write your own new MarkDown file specifically for library and put it in the `.qiime2/library` folder or anywhere else in the repo.
user_docs_link: A link to the user docs for this plugin.
```

## environments/

Additionally, all repos in the QIIME 2 library must have conda environment.yml files for each supported QIIME 2 release with the following naming scheme `<plugin-name>-qiime2-<distro>-<epoch>.yml`. These files must be located in the `/.qiime2/library/environments/` folder.

### Additional Requirements

1. Your plugin must be fully installable via these environment files with no extra steps required.
2. Your enviornment files must NOT contain a `name` field. The end user is expected to provide the name on the command line when they install.
