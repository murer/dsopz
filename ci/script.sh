#!/bin/bash -xe

python dsopz/dsopz.py login-serviceaccount -f test/dsopzit.secret.json

./test/test.sh
