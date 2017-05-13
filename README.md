# Minfin Funds Parser

[![Build Status](https://travis-ci.org/pryazhnikov/minfin-funds.svg?branch=master)](https://travis-ci.org/pryazhnikov/minfin-funds)

This repo contains scripts for loading data about Russian sovereign wealth funds from [official site of Russian Ministry of Finance](http://minfin.ru/) to machine readable CSV files.

## How to Use

You should install `Python 3` to use scripts from this repo.

```bash
# Python requirements installing
pip3 install -r requirements.txt

# Input Excel files loading (from minfin.ru into data/input/ directory)
./data_load.py --count 6

# Loaded funds data conversion into CSV files (see data/output/ directory)
./data_parse.py
```
