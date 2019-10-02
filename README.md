# WordWeaver

[![Coverage Status](https://codecov.io/gh/nrc-cnrc/wordweaver/branch/master/graph/badge.svg)](https://codecov.io/gh/nrc-cnrc/wordweaver)
[![Documentation Status](https://readthedocs.org/projects/wordweaver/badge/?version=latest)](https://wordweaver.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/nrc-cnrc/wordweaver.svg?branch=master)](https://travis-ci.org/nrc-cnrc/wordweaver)
[![PyPI package](https://img.shields.io/pypi/v/wordweaver.svg)](https://pypi.org/project/wordweaver/)
[![license](https://img.shields.io/github/license/nrc-cnrc/wordweaver.svg)](LICENSE)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/nrc-cnrc/wordweaver)

> Creating RESTful morphology web services for Iroquoian languages

:warning: :construction: This repo is currently **under construction** :construction: :warning:

Please visit the [docs](https://wordweaver.readthedocs.io/en/latest/?badge=latest) for more information!

## Table of Contents
- [WordWeaver](#wordweaver)
  - [Table of Contents](#table-of-contents)
  - [Background](#background)
  - [Install](#install)
  - [Usage](#usage)
  - [Maintainers](#maintainers)
  - [Contributing](#contributing)
  - [License](#license)

## Background

WordWeaver is a Python library for turning an FST made with [Foma](https://fomafst.github.io/morphtut.html) into a RESTful API. 
It combines with the WordWeaver GUI to create an interactive web application for the data as well. 
WordWeaver was initially built for [Kanyen’kéha](https://www.aclweb.org/anthology/W18-4806) but with all Iroquoian languages in mind. 
It will likely work for similar polysynthetic languages and Foma FSTs that model inflectional verbal morphology, 
but non-Iroquoian languages will likely have to modify the source in order to work.

## Install

The best thing to do is install with pip `pip install wordweaver`. 

Otherwise, clone the repo and pip install it locally.

```sh
$ git clone https://github.com/nrc-cnrc/wordweaver.git
$ cd wordweaver
$ pip install -e .
```

## Usage

Please visit the docs for more information.

## Maintainers

[@roedoejet](https://github.com/roedoejet).
[@anna-ka](https://github.com/anna-ka).


## Contributing

Feel free to dive in! [Open an issue](https://github.com/nrc-cnrc/wordweaver/issues/new) or submit PRs.

This repo follows the [Contributor Covenant](http://contributor-covenant.org/version/1/3/0/) Code of Conduct.


## License

[MIT](LICENSE)
