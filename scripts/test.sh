#! /usr/bin/env bash

export PYTHONPATH=$PWD
export TEST_FLAG=true

exec TEST_FLAG=true pytest app/tests
