#!/bin/bash -xe

install_gcloud() {
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

  ./gen/google-cloud-sdk/bin/gcloud config set project dsopzproj
}

install_pycrypto() {
  pip install pycrypto
}

install_gcloud &
install_pycrypto &

wait %1
wait %2
