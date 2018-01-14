# Stitch (modified version)

This is a slightly modified version of [Stitch](README.rst).

## 1. Contents

-   [Stitch (modified version)](#stitch-modified-version)
    -   [1. Contents](#1-contents)
    -   [2. Installation](#2-installation)
-   [Differences from original
    Stitch:](#differences-from-original-stitch)
    -   [1. New code chunks options](#1-new-code-chunks-options)
        -   [1.1 Results Pandoc chunk option](#11-results-pandoc-chunk-option)
    -   [2. New document options](#2-new-document-options)
        -   [2.1 Default eval value](#21-default-eval-value)
        -   [2.2 Disabled code chunks prompt
            prefixes](#22-disabled-code-chunks-prompt-prefixes)
        -   [2.3 Languages / Kernels / Styles mappings in YAML
            metadata](#23-languages-kernels-styles-mappings-in-yaml-metadata)
    -   [3. API description](#3-api-description)
    -   [4. Known issues](#4-known-issues)
        -   [4.1 Fixed installation from GitHub](#41-fixed-installation-from-github)
        -   [4.2 No new line after Jupyter output](#42-no-new-line-after-jupyter-output)
        -   [4.3 Pandoc-crossref labels move to the new line](#43-pandoc-crossref-labels-move-to-the-new-line)

## 2. Installation

Installation:
```
pip install git+https://github.com/kiwi0fruit/stitch.git#egg=knotr
```
Installation in details:

Recommended installation via conda. I assume that you have `conda`, `pip` and `activate` commands available from the command line. This is the case when you install Anaconda or Miniconda with default settings or you know what you are doing. Example installation:

First create `myenv` environment from **yml** file `my_env.yml`:

```
conda env create -f "my_env.yml"
```

`my_env.yml` file:

```yaml
name: myenv
channels:
  - defaults
  - conda-forge
dependencies:
  - python=3
  # knotr:
  - jupyter_core
  - traitlets
  - ipython
  - jupyter_client
  - nbconvert
  - pandocfilters
  - click
  # knotr@conda-forge:
  - pypandoc
```
Then activate `myenv` environment and install modified Stitch:
```
activate myenv
pip install git+https://github.com/kiwi0fruit/stitch.git#egg=knotr
```
You need to have installed [**Git**](https://git-scm.com/downloads) available from command prompt.

Also Stitch needs installed [**Pandoc**](https://github.com/jgm/pandoc/releases). It needs Pandoc to be available from command prompt. Check: `pandoc --help`. It should work. Here is useful [Pandoc manual](http://pandoc.org/MANUAL.html).

# Differences from original Stitch:

## 1. New code chunks options

See code chunks options [**here**](https://pystitch.github.io/api.html#chunk-options).

### 1.1 Results Pandoc chunk option

`results` code chunk option was modified:

* default is `results=default` (same as in the original Stitch),
* `results=pandoc`: same as `default` but some Jupyter output is parsed as markdown: if the output is a stdout message that is not warning/error or if it has `text/plain` key. For example python `print()` output.
* `results=hide`: evaluate chunk but hide results (same as in the original Stitch).

## 2. New document options

### 2.1 Default eval value

Default `eval` value for each code cell can be set in metadata section:

```yaml
---
eval_default: False
...
```

Default `eval_default` value is `True`.

### 2.2 Disabled code chunks prompt prefixes

Now code chunk prefixes are disabled by default. To enable them use `--use-prompt` command line option or set it in the metadata section:

```yaml
---
use_prompt: True
...
```

If you specify `prompt` option for a code chunk then it would have a prompt even if it's disabled.

### 2.3 Languages / Kernels / Styles mappings in YAML metadata

Mappings to markdown YAML metadata are added:

* from **language names** to **Jupyter kernels names**
* from **language names** to **CSS classes names**
* **language names** are used in Stitch code blocks settings

For example:

```yaml
---
kernels-map:
  r: ir
  py2: python2
styles-map:
  py2: py
...
```

## 3. API description

`stitch.Stitch` class API description should be changed a bit:

```py
class Stitch(HasTraits):
    ...

    def __init__(self, name: str, to: str='html',
                 standalone: bool=True,
                 self_contained: bool=True,
                 warning: bool=True,
                 error: str='continue',
                 prompt: str=None,
                 use_prompt: bool=False,
                 pandoc_extra_args: list=None):
        """
        Parameters
        ----------
        name : str
            controls the directory for supporting files
        to : str, default ``'html'``
            output format
        standalone : bool, default True
            whether to make a standalone document
        self_contained: bool, default True
        warning : bool, default True
            whether to include warnings (stderr) in the ouput.
        error : ``{"continue", "raise"}``
            how to handle errors in the code being executed.
        prompt : str, default None
        use_prompt : bool, default False
            Whether to use prompt prefixes in code chunks
        pandoc_extra_args : list of str, default None
            Pandoc extra args for converting text from markdown
            to JSON AST.
        """
        ...

    def stitch_ast(self, ast: dict) -> dict:
        """
        Main method for converting a document.

        Parameters
        ----------
        ast : dict
            Loaded Pandoc json AST

        Returns
        -------
        doc : dict
            These should be compatible with pando's JSON AST
            It's a dict with keys
              - pandoc-api-version
              - meta
              - blocks
        """
    ...
```

## 4. Known issues

### 4.1 Fixed installation from GitHub

In order to get installation from GitHub work I had to re-add a submodule via:

```
git submodule add https://github.com/pystitch/pystitch.github.io pystitch.github.io
```

### 4.2 No new line after Jupyter output

Sometimes R language output does not have new line after it (or may be other languages as well). So it might interfere with the next text. Adding

```html
<b></b>
```

below the code chunk fixes the problem.

### 4.3 Pandoc-crossref labels move to the new line

When you add formula labels for **pandoc-crossref** you should place them right after the formula (like `$$x=y+z$${#eq:1}` – no spaces). Otherwise when stitching from markdown to markdown labels would move to the next line and stop working.
