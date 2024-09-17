# Library-repos
Stores a list of the repos that are included in the QIIME 2 library.

# How to add a repo
Simply open a PR adding a `<my-repo-name>.yml` file to the `repos` folder. This file must have the following `key: value` pairs:

```
owner: <repo-owner>
name: <repo-name>
branch: <target-branch>
```

# Requirements for added repos

Repos added to the QIIME 2 library are required to contain the following directory structure.

```
/.qiime2/library/
                |_info.yml
                |_/environments/
                               |_<repo-name>-qiime2-<distro>-<epoch>.yml
                               |_...
```

The top level of the repo must contain a `.qiime2` folder which must contain a `library` folder. The library folder must contain an `info.yml` file and an `environments` folder.

## info.yml

This file must have the following `key: value` pairs:

```yaml
short_description: Ideally 300 character or less description of what the plugin is and does.
long_description_path: A path relative to the root of the repo to a MarkDown formatted file describing the plugin in more depth. This can simply be the repo's README if you want, or you can write your own new MarkDown file specifically for library and put it in the `.qiime2/library` folder or anywhere else in the repo.
user_docs_link: A link to the user docs for this plugin.
additional_install_steps: true or false, does your plugin require additional install steps adter installing the conda environment?
```

__Note:__ If your plugin does require additional install steps, then you must supply install instructions in your long description.

## environments/

Additionally, all repos in the QIIME 2 library must have conda environment.yml files for each supported QIIME 2 release with the following naming scheme `<repo-name>-qiime2-<distro>-<epoch>.yml`. These files must be located in the `/.qiime2/library/environments/` folder.