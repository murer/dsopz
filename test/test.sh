#!/bin/bash -xe

gcloud beta emulators datastore start  --host-port 'localhost:8082' --no-store-on-disk &
