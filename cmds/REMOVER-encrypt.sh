#!/bin/bash -e

if [ "x$DSOPZ_SECRET" == "x" ]; then
	echo "export DSOPZ_SECRET to descrypt files";
	exit 1;
fi

openssl enc -aes-256-cbc -salt -in "$1" -out "$1.crypt" -pass "pass:$DSOPZ_SECRET";
