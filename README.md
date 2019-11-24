# Python projects

[![](https://github.com/cytopia/python-projects/workflows/Files/badge.svg)](https://github.com/cytopia/python-projects/actions?workflow=Files)
[![](https://github.com/cytopia/python-projects/workflows/Python/badge.svg)](https://github.com/cytopia/python-projects/actions?workflow=Python)
[![](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)



## Help
```bash
$ make help

autoformat                  Autoformat Python files according to black
lint-all                    Lint all targets below
lint-files                  Lint and test all files
lint-json                   Lint JSON files
lint-python-pycodestyle     Lint Python files against pycodestyleodestyle
lint-python-pydocstyle      Lint Python files against pydocstyleocstyle
lint-python-black           Lint Python files against black (code formatter)
create-project-flask-mongo  Creates a new project based on Flask and Mongo
```


## Autoformat code
```bash
make autoformat
```


## Check style
```bash
make python-pycodestyle
make python-pydocstyle
make python-black
```
