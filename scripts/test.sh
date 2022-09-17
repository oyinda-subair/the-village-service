#! /usr/bin/env bash

export PYTHONPATH=$PWD
export TEST_FLAG=true

exec pytest
