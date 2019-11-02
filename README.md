# NSF-DATA

> Download and analyze award data from the National Science Foundation.

## Installation

```sh
$ mkdir nsf-data
$ cd nsf-data
$ git clone "https://github.com/eddiechapman/nsf-data.git"
$ python3 -m venv venv
$ soure venv/bin/activate
$ python setup.py install
```

## Usage

### Downloading award data.

```sh
$ cd scripts
$ download.py [YEARS]
```

## TODO:

`filter.py`

- pulling in lots of results now. Don't need to save all fields to CSV.
- consider just outputting award IDs, or award IDs plus abstracts?
- or perhaps filtering by keywords during the script.
