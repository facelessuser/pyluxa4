# Development

## Coding Standards

When writing code, the code should roughly conform to PEP8 and PEP257 suggestions.  The project utilizes the Flake8
linter (with some additional plugins) to ensure code conforms (give or take some of the rules).  When in doubt, follow
the formatting hints of existing code when adding files or modifying existing files.  Listed below are the modules used:

- @gitlab:pycqa/flake8
- @gitlab:pycqa/flake8-docstrings
- @gitlab:pycqa/pep8-naming
- @ebeweber/flake8-mutable
- @gforcada/flake8-builtins

Usually this can be automated with Tox (assuming it is installed): `tox -e lint`.

## Building and Editing Documents

Documents are in Markdown (with with some additional syntax provided by extensions) and are converted to HTML via Python
Markdown. If you would like to build and preview the documentation, you must have these packages installed:

- @Python-Markdown/markdown: the Markdown parser.
- @mkdocs/mkdocs: the document site generator.
- @squidfunk/mkdocs-material: a material theme for MkDocs.
- @facelessuser/pymdown-extensions: this Python Markdown extension bundle.

In order to build and preview the documents, just run the command below from the root of the project and you should be
able to view the documents at `localhost:8000` in your browser. After that, you should be able to update the documents
and have your browser preview update live.

```
mkdocs serve
```

## Spell Checking Documents

Spell checking is performed via @facelessuser/pyspelling.

During validation we build the docs and spell check various files in the project. [Aspell][aspell] must be installed and
in the path.  Currently this project uses one of the more recent versions of Aspell.  It is not expected that everyone
will install and run Aspell locally, but it will be run in CI tests for pull requests.

In order to perform the spell check locally, it is expected you are setup to build the documents, and that you have
Aspell installed in your system path (if needed you can use the `--binary` option to point to the location of your
Aspell binary). It is also expected that you have the `en` dictionary installed as well. To initiate the spell check,
run the following command from the root of the project.

You will need to make sure the documents are built first:

```
mkdocs build --clean
```

And then run the spell checker.

```
pyspelling
```

It should print out the files with the misspelled words if any are found.  If you find it prints words that are not
misspelled, you can add them in `docs/src/dictionary/en-custom.text`.

### Running Validation With Tox

Tox (@tox-dev/tox) is a great way to run the validation tests, spelling checks, and linting in virtual environments so
as not to mess with your current working environment. Tox will use the specified Python version for the given
environment and create a virtual environment and install all the needed requirements (minus Aspell).  You could also
setup your own virtual environments with the Virtualenv module without Tox, and manually do the same.

First, you need to have Tox installed:

```
pip install tox
```

By running Tox, it will walk through all the environments and create them (assuming you have all the python versions on
your machine) and run the related tests.  See `tox.ini` to learn more.

```
tox
```

To target linting:

```
tox -e lint
```

To select spell checking and document building:

```
tox -e documents
```

--8<-- "links.txt"
