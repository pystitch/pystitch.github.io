This is the repo to generate the [comparison site](https://pystitch.github.io).

# Building the Page

You'll need to install [stitch](https://github.com/pystitch/stitch) (only
available on Github at the moment).

To make the page, use

```
make index.html
```

This will call `stitch` on `src/usage.md`. The included script will then
walk through the markdown and HTML documents, weaving the two together.
