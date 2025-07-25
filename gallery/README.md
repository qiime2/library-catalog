# Instructions for adding a visualization to the QIIME 2 View Gallery

Open a PR against this repo adding the following:

```
/gallery/
        |__<entry-name>/
                       |__info.json
                       |__thumb.png
```

## info.json contents

`info.json` must contain the following key: value pairs.

```
title: The name of your gallery entry
desc: A short description of your gallery entry
href: The URL of your visualization (This URL MUST have appropriate CORS headers set)
```

## thumb.png

The .png you wish to use as the thumbnail for your visualization in the gallery. This should be a screenshot of your visualization.

## /gallery/index.json

Edit `/gallery/index.json` adding `<entry-name>` to the end of the list. This must be the same as the name of the directory you added under `/gallery`.

## Example PR

An [example PR](https://github.com/qiime2/q2view-gallery/pull/8) showing the addition of an entry to the gallery in a single atomic commit.