#!/bin/bash -xe

echo "branch: $TRAVIS_BRANCH"

./cmds/decrypt.sh

if ! ./gen/google-cloud-sdk/bin/gcloud --version; then
  rm -rf gen/google-cloud-sdk || true
  rm google-cloud-sdk.tar.gz || true
  mkdir gen || true
  wget 'https://repoz.dextra.com.br/repoz/r/pub/google-cloud/google-cloud-sdk-114.0.0-linux-x86_64.tar.gz' -O gen/google-cloud-sdk.tar.gz
  cd gen
  tar xzf google-cloud-sdk.tar.gz
  cd -
fi

./gen/google-cloud-sdk/bin/gcloud components update -q
./gen/google-cloud-sdk/bin/gcloud components install beta cloud-datastore-emulator -q

./gen/google-cloud-sdk/bin/gcloud auth activate-service-account --key-file ./cmds/keys/dsopzit.secret.json
