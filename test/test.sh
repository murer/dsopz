#!/bin/bash -xe

DS=${1:-cloudcontainerz}
NS=${2:-dsopz_test}

EF=target/dsopz_test
rm -rf "$EF" || true
mkdir -p "$EF"

cleanup() {
python -m dsopz.dsopz 'export' -d "$DS" -n "$NS$1" -o true | python -m dsopz.dsopz 'import' -d "$DS" -n "$NS$1" -o remove
}

cleanup_all() {
cleanup 1 &
cleanup 2 &
cleanup 3 &
cleanup 4 &
cleanup 5 &
cleanup 6 &
wait
}
trap cleanup_all EXIT

import_export_test() {
cleanup "$1"
python -m dsopz.dsopz 'export' -d "$DS" -n "$NS$1" | wc -l | grep '^0$'
python -m dsopz.dsopz 'import' -d "$DS" -n "$NS$1" -o upsert < "test/entities.json"
python -m dsopz.dsopz 'export' -d "$DS" -n "$NS$1" -o false | diff - "test/entities.json"
python -m dsopz.dsopz 'export' -d "$DS" -n "$NS$1" | diff - "test/entities.json"
}

import_export_keys_test() {
cleanup "$1"
python -m dsopz.dsopz 'import' -d "$DS" -n "$NS$1" -o upsert < "test/entities.json"
python -m dsopz.dsopz 'export' -d "$DS" -n "$NS$1" -o true | diff - "test/keys.json"
}

gql_test() {
cleanup "$1"
python -m dsopz.dsopz 'gql' -d "$DS" -n "$NS$1" -q "select * from dsopz_test order by c2" | wc -l | grep '^0$'
}

index_test() {
cleanup "$1"
python -m dsopz.dsopz 'index' -k "dsopz_test" -c c2 -i true > "$EF/processed$1.json" < "test/entities.json"
python -m dsopz.dsopz 'import' -d "$DS" -n "$NS$1" -o upsert < "$EF/processed$1.json"
sleep 1
python -m dsopz.dsopz 'gql' -d "$DS" -n "$NS$1" -q "select * from dsopz_test order by c2" | wc -l | grep '^2$'
python -m dsopz.dsopz 'gql' -d "$DS" -n "$NS$1" -q "select * from dsopz_test order by c3" | wc -l | grep '^0$'
}

index_list_test() {
cleanup "$1"
python -m dsopz.dsopz 'index' -k "dsopz_test" -c c3 -i true > "$EF/processed$1.json" < "test/entities.json"
python -m dsopz.dsopz 'import' -d "$DS" -n "$NS$1" -o upsert < "$EF/processed$1.json"
sleep 1
python -m dsopz.dsopz 'gql' -d "$DS" -n "$NS$1" -q "select * from dsopz_test where c3 = 'a1'" | wc -l | grep '^2$'
python -m dsopz.dsopz 'gql' -d "$DS" -n "$NS$1" -q "select * from dsopz_test where c3 = 'a2'" | wc -l | grep '^1$'
python -m dsopz.dsopz 'gql' -d "$DS" -n "$NS$1" -q "select * from dsopz_test where c3 = 'a3'" | wc -l | grep '^1$'
}

import_block_test() {
cleanup "$1"
for k in $(seq 1 7); do cat test/template.json | sed "s/COUNTER/n$k/g"; done | python -m dsopz.dsopz 'import' -d "$DS" -n "$NS$1" -p 2 -b 2 -o upsert
python -m dsopz.dsopz 'export' -d "$DS" -n "$NS$1" | wc -l | grep '^7$'
}

offline_test() {
cat "test/entities.json" | python -m dsopz.dsopz csv -c c1 __key__ c2 | diff - "test/entities.csv"
cat "test/entities.json" | python -m dsopz.dsopz sql -c c1 __key__ c2 | diff - "test/entities.sql"

cat "test/entities.json" | python -m dsopz.dsopz map > "$EF/mapped.json" 3<<-EOF
ent['properties']['c2'] = {'excludeFromIndexes':True, 'stringValue':'changed'}
emit(ent)
EOF
cat "$EF/mapped.json" | python -m dsopz.dsopz csv -c c1 __key__ c2 | grep 'changed' | wc -l | grep '^2$'
}

import_export_test 1 &
import_export_keys_test 2 &
gql_test 3 &
index_test 4 &
index_list_test 5 &
import_block_test 6 &

offline_test

wait %1
wait %2
wait %3
wait %4
wait %5
wait %6

echo "SUCCESS"
