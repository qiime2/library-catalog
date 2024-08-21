# library-repos
Stores a list of the repos that are included in the QIIME 2 library

# How to add a repo
Simply add the owner of the repo, the name of the repo, and the branch you want to target to `repos.yaml`

# Requirements for added repos
Repos added to the QIIME 2 Library are required to have a .qiime2 folder at the top level of the repo. This folder must contain two files.

## info.md
A markdown file giving a detailed description of the plugin including links to user documentation, install instructions, etc.

## short-description.txt
A plain text file containing a short unformatted blurb about your plugin. Try to keep this under ~300 characters or so.
