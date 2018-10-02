#!/bin/bash -ex

CLOSE_VERSION="$1"

if [ "x$CLOSE_VERSION" == "x" ]; then
	echo "Script usage: ./tag-version.sh 0.0.1"
  exit 1
fi;

if git status -s | grep ".\\+"; then
	exit 1
fi

#python -m dsopz.dsopz version

#echo "version=\"$CLOSE_VERSION\"" > dsopz/config.py
git commit -am "releasing $CLOSE_VERSION"
git tag "dsopz-$CLOSE_VERSION"
git push origin "dsopz-$CLOSE_VERSION"

#python -m dsopz.dsopz version

git push
