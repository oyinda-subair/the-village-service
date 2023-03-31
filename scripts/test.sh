#! /usr/bin/env bash

export PYTHONPATH=$PWD

ENVIRONMENT=test pytest $1 $2
