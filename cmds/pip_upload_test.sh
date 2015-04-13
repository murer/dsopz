#!/bin/bash -xe

#python setup.py sdist register -r pypitest 
python setup.py sdist upload -r pypitest 
