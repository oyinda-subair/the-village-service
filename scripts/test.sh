#! /usr/bin/env bash

export PYTHONPATH=$PWD
export TEST_FLAG=true

### For coverage run
exec poetry run coverage run -m pytest && poetry run coverage report -m
# exec pytest
