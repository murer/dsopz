#!/bin/bash -xe

#python -m dsopz.dsopz login-serviceaccount -f test/dsopzit.secret.json

#./test/test.sh cloudcontainerz "dsopz-it-$(($RANDOM % 100))-"

export PATH="$(pwd)/gen/google-cloud-sdk/bin/gcloud:$PATH"

python -m dsopztest
