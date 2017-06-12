#!/bin/bash -xe

OPERATION=${1:-build}

cd cmds/jekyll
docker build -t dsopz-jekyll .
cd -

docker rm -f dsopz-jekyll || true
docker run -it -v "$(pwd):/opt/dsopz" -p 4000:4000 --name dsopz-jekyll dsopz-jekyll "/opt/config/entry-point-$OPERATION.sh"

docker cp dsopz-jekyll:/opt/site docs/site || true
