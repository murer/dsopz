#!/bin/bash -xe

#python setup.py sdist register -r pypi
python3 setup.py sdist upload -r pypi
