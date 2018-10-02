#!/bin/bash -xe

#python setup.py sdist register -r pypitest
python3 setup.py sdist upload -r pypitest 
