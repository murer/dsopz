#!/bin/bash -xe

DS=${1:-cloudcontainerz}
NS=${2:-dsopz_test}

EF=target/dsopz_test
rm -rf "$EF" || true
mkdir -p "$EF"

cleanup() {
python -m dsopz.dsopz 'export' -d "$DS" -n "$NS" -o true | python -m dsopz.dsopz 'import' -d "$DS" -n "$NS" -o remove
}

trap cleanup EXIT

kind_test() {
  cleanup
  python -m dsopz.dsopz 'import' -d "$DS" -n "$NS" -o upsert < "test/entities.json"
  python -m dsopz.dsopz 'kind' -d "$DS" -n "$NS" | grep '^dsopz_test$'
}

import_export_test() {
cleanup
python -m dsopz.dsopz 'export' -d "$DS" -n "$NS" | wc -l | grep '^0$'
python -m dsopz.dsopz 'import' -d "$DS" -n "$NS" -o upsert < "test/entities.json"
python -m dsopz.dsopz 'export' -d "$DS" -n "$NS" -o false | diff - "test/entities.json"
python -m dsopz.dsopz 'export' -d "$DS" -n "$NS" | diff - "test/entities.json"
}

import_export_keys_test() {
cleanup
python -m dsopz.dsopz 'import' -d "$DS" -n "$NS" -o upsert < "test/entities.json"
python -m dsopz.dsopz 'export' -d "$DS" -n "$NS" -o true | diff - "test/keys.json"
}

gql_test() {
cleanup
python -m dsopz.dsopz 'gql' -d "$DS" -n "$NS" -q "select * from dsopz_test order by c2" | wc -l | grep '^0$'
}

index_test() {
cleanup
python -m dsopz.dsopz 'index' -k "dsopz_test" -c c2 -i true > "$EF/processed$1.json" < "test/entities.json"
python -m dsopz.dsopz 'import' -d "$DS" -n "$NS" -o upsert < "$EF/processed$1.json"
sleep 1
python -m dsopz.dsopz 'gql' -d "$DS" -n "$NS" -q "select * from dsopz_test order by c2" | wc -l | grep '^2$'
python -m dsopz.dsopz 'gql' -d "$DS" -n "$NS" -q "select * from dsopz_test order by c3" | wc -l | grep '^0$'
}

index_list_test() {
cleanup
python -m dsopz.dsopz 'index' -k "dsopz_test" -c c3 -i true > "$EF/processed$1.json" < "test/entities.json"
python -m dsopz.dsopz 'import' -d "$DS" -n "$NS" -o upsert < "$EF/processed$1.json"
sleep 1
python -m dsopz.dsopz 'gql' -d "$DS" -n "$NS" -q "select * from dsopz_test where c3 = 'a1'" | wc -l | grep '^2$'
python -m dsopz.dsopz 'gql' -d "$DS" -n "$NS" -q "select * from dsopz_test where c3 = 'a2'" | wc -l | grep '^1$'
python -m dsopz.dsopz 'gql' -d "$DS" -n "$NS" -q "select * from dsopz_test where c3 = 'a3'" | wc -l | grep '^1$'
}

import_block_test() {
cleanup
for k in $(seq 1 7); do cat test/template.json | sed "s/COUNTER/n$k/g"; done | python -m dsopz.dsopz 'import' -d "$DS" -n "$NS" -p 2 -b 2 -o upsert
python -m dsopz.dsopz 'export' -d "$DS" -n "$NS" | wc -l | grep '^7$'
}

offline_test() {
cat "test/entities.json" | python -m dsopz.dsopz csv -c c1 __key__ c2 c4 | diff - "test/entities.csv"
cat "test/entities.json" | python -m dsopz.dsopz sql -c c1 __key__ c2 c4 | diff - "test/entities.sql"

cat "test/entities.json" | python -m dsopz.dsopz map > "$EF/mapped.json" 3<<-EOF
ent['properties']['c2'] = {'excludeFromIndexes':True, 'stringValue':'changed'}
emit(ent)
EOF
cat "$EF/mapped.json" | python -m dsopz.dsopz csv -c c1 __key__ c2 c4 | grep 'changed' | wc -l | grep '^2$'
}

kind_test
import_export_test
import_export_keys_test
gql_test
index_test
index_list_test
import_block_test

offline_test

echo "SUCCESS"
