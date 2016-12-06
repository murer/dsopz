#!/bin/bash -xe

docker rm -f dsopz_test || true
docker run -it --rm=true --name dsopz_test python:2.7 /bin/bash
