#!/bin/bash -e

if [ "x$DSOPZ_SECRET" == "x" ]; then
	echo "export DSOPZ_SECRET to descrypt files";
	exit 1;
fi

find  . -name "*.crypt" | while read k; do
	echo "decrypt: $k";
	openssl enc -aes-256-cbc -salt -in "$k" -out "$(echo "$k" | sed "s/\.crypt$//g")" -d -pass "pass:$DSOPZ_SECRET";
done
