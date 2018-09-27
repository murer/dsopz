#!/bin/bash -xe

dataset="aaa"
namespace="bbb"

setUp() {
  python3 -m dsopz query -d "$dataset" -n "$namespace" -g 'select __key__' -fgz target/sandbox/all.keys.json.gz
}

#python3 -m dsopz.dsopz query -d "$dataset" -n "$namespace" -g 'select __key__'  > target/sandbox/all.keys.json

#python3 -m dsopz.dsopz upsert -d "$dataset" -n "$namespace" -g 'select *' -f 'gen/testsh/sample.json'

#python3 -m dsopz.dsopz query -d "$dataset" -n "$namespace" -g 'select *'

setUp
