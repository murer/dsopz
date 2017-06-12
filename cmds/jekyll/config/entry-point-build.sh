#!/bin/bash -xe

source /opt/config/basics.sh

jekyll build --destination /opt/site

echo done
