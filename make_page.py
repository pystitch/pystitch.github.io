import bs4
from textwrap import dedent
from markdown import markdown
from itertools import takewhile, dropwhile
from toolz import partitionby
from jinja2 import Template


def rendered_pairs(src):
    with open(src) as f:
        soup = bs4.BeautifulSoup(f.read(), "lxml")

    pairs = []
    for head in soup.find_all('h2'):
        right = head.find_next('h2')
        nodes = (node for node in head.nextSiblingGenerator())
        selected = list(takewhile(lambda node: node != right, nodes))
        pairs.append({'head': head, 'rest': "\n".join(str(x) for x in selected)})
    return pairs


def source_pairs(src):
    with open(src) as f:
        doc = f.read()
    lines = doc.split("\n")
    lines = dropwhile(lambda line: not line.startswith("##"), lines)
    lines = list(partitionby(lambda x: x.startswith("##"), lines))
    headers, rest = lines[::2], lines[1::2]

    pairs = [{"head": h[0], "rest": '\n'.join(r)}
             for h, r in zip(headers, rest)]
    return pairs


def render(source, rendered):
    assert len(source) == len(rendered)
    pairs = [{"source": s, "rendered": r} for s, r in zip(source, rendered)]
    preamble = dedent('''\
    # Stitch

    Stitch is a small python library for writing reproducible reports in
    markdown.
    It's heavily inspired by (read: a python clone of) <a href="http://yihui.name/knitr/">knitr</a> and
    <a href="http://rmarkdown.rstudio.com">RMarkdown</a>.

    You might want to consider <a href="https://github.com/janschulz/knitpy">Knitpy</a> instead
    of stitch. It's been around longer is probably more usable at this point.

    This document shows you the source markdown side-by-side
    with the executed and rendered HTML.
    For more a more complex example, check out the "Examples" tab in the
    navbar, which links to the source markdown and rendered HTML, PDF, and
    docx versions of the document.
    ''')
    preamble = markdown(preamble)

    tpl = Template('''
    <html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
        <link rel="stylesheet" type="text/css" href="style.css">
        <link rel="stylesheet" type="text/css" href="default.css">
    </head>
    <body>

    <nav class="navbar navbar-default">
      <div class="container-fluid">
    <!-- Brand and toggle get grouped for better mobile display -->
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="https://github.com/pystitch/stitch">stitch</a>
    </div>

    <!-- Collect the nav links, forms, and other content for toggling -->
    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      <ul class="nav navbar-nav">
            <li ><a href="https://pystitch.github.io">Docs</a></li>
        <li class="dropdown">
          <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Examples<span class="caret"></span></a>
          <ul class="dropdown-menu">
        <li><a href="tidy.txt">Markdown</a></li>
        <li><a href="tidy.html">HTML</a></li>
        <li><a href="tidy.pdf">PDF</a></li>
        <li><a href="tidy.docx">docx</a></li>
          </ul>
        </li>
      </ul>
    </div><!-- /.navbar-collapse -->
      </div><!-- /.container-fluid -->
    </nav>


    {{ preamble|safe }}
    <div class="container">
    {% for pair in pairs %}
    <div class="area">
        {{ pair.rendered.head | safe }}

        <div class="source">
            <pre>
                {{ pair.source.rest|safe }}
            </pre>
        </div>
        <div class="rendered">
            {{ pair.rendered.rest|safe }}
        </div>

    </div>
    <hr>
    {% endfor %}
    </div>
    <script src="https://code.jquery.com/jquery-3.1.0.slim.min.js" integrity="sha256-cRpWjoSOw5KcyIOaZNo4i6fZ9tKPhYYb6i5T9RSVJG8=" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
    </body>
    </html>
    ''')
    result = tpl.render(pairs=pairs, preamble=preamble)
    with open('build/side_by_side.html', 'w') as f:
        f.write(result)


def main():
    source = source_pairs("src/usage.md")
    rendered = rendered_pairs("build/usage.html")
    render(source, rendered)


if __name__ == '__main__':
    main()
