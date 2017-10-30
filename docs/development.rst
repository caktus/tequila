Development
===========

You will need to have a checkout of the repo on your machine ::

    $ git clone git@github.com:caktus/tequila.git
    $ cd tequila/

In order to build the documentation, you need to have `Sphinx
<http://www.sphinx-doc.org/en/stable/>`_ and its dependencies
installed ::

    $ mkvirtualenv tequila -p $(which python3)
    (tequila)$ pip install Sphinx

In the docs/ directory, you can now build the html version of the docs
using the provided Makefile ::

    (tequila)$ cd docs/
    (tequila)$ make html

This will create or update the html files in docs/_build/html/.  The
easiest way to then view the updated documentation is by using Python
as a simple webserver ::

    (tequila)$ python -m http.server 8000

While this is running, you can point your browser at
`http://localhost:8000/_build/html/
<http://localhost:8000/_build/html/>`_ to browse the docs.
