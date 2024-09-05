# library-repos
Stores a list of the repos that are included in the QIIME 2 library

# How to add a repo
Simply add a `my-repo-name.yml` file to the `repos` folder. This file must have the following `key: value` pairs:

```
owner: <repo-owner>
name: <repo-name>
branch: <target-branch>
```

# Requirements for added repos
Repos added to the QIIME 2 Library are required to have a `.qiime2` folder at the top level of the repo. This folder must contain an `info.yml` file. This file must have the following `key: value` pairs:

```
short_description: Ideally 300 character or less description of what the plugin is and does
long_description_path: A path relative to the root of the repo to a MarkDown formatted file describing the plugin in more depth. This can simply be the repo's README if you want, or you can write your own new MarkDown file specifically for library and put it in the `.qiime2` folder.
user_docs_link: A link to the user docs for this plugin
```

Additionally, all repos in the QIIME 2 library must have conda environment .yml files for each supported distro and epoch with the following naming scheme `<repo-name>-qiime2-<distro>-<epoch>.yml`. These files must be located in an `environments` folder that may either be under the `.qiime2` directory or the top level of the repo. The path under `.qiime2` is checked first and then we fall back to the top level.

Note: The environments folder containing the QIIME 2 environment files must contain ONLY the properly formatted and named QIIME 2 conda environment `.yml` files.