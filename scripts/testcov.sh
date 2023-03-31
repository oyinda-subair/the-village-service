#! /usr/bin/env bash

export PYTHONPATH=$PWD

### For coverage run
ENVIRONMENT=test poetry run coverage run -m pytest && poetry run coverage report -m
