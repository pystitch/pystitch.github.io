This is the repo to generate the [comparison site](https://pystitch.github.io).

# Building the Page

If you're modifying the markdown source, you'll need to install
[stitch](https://github.com/pystitch/stitch) (only available on Github at the moment).
If you're just altering the CSS, you shouldn't need `stitch`.

To make the page, use

```
make index.html
```

This will call `stitch` on `src/usage.md`. The included script will then
walk through the markdown and HTML documents, weaving the two together.
