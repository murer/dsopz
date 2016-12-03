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
cleanup

python -m dsopz.dsopz 'export' -d "$DS" -n "$NS" | wc -l | grep '^0$'

python -m dsopz.dsopz 'import' -d "$DS" -n "$NS" -o upsert < "test/entities.json"
python -m dsopz.dsopz 'export' -d "$DS" -n "$NS" -o false | diff - "test/entities.json"
python -m dsopz.dsopz 'export' -d "$DS" -n "$NS" | diff - "test/entities.json"
python -m dsopz.dsopz 'export' -d "$DS" -n "$NS" -o true | diff - "test/keys.json"

python -m dsopz.dsopz 'gql' -d "$DS" -n "$NS" -q "select * from dsopz_test order by c2" | wc -l | grep '^0$'

python -m dsopz.dsopz 'index' -k "dsopz_test" -c c2 -i true > "$EF/processed.json" < "test/entities.json"
python -m dsopz.dsopz 'import' -d "$DS" -n "$NS" -o upsert < "$EF/processed.json"
python -m dsopz.dsopz 'gql' -d "$DS" -n "$NS" -q "select * from dsopz_test order by c2" | wc -l | grep '^2$'
python -m dsopz.dsopz 'gql' -d "$DS" -n "$NS" -q "select * from dsopz_test order by c3" | wc -l | grep '^0$'

python -m dsopz.dsopz 'index' -k "dsopz_test" -c c3 -i true > "$EF/processed.json" < "test/entities.json"
python -m dsopz.dsopz 'import' -d "$DS" -n "$NS" -o upsert < "$EF/processed.json"
python -m dsopz.dsopz 'gql' -d "$DS" -n "$NS" -q "select * from dsopz_test where c3 = 'a1'" | wc -l | grep '^2$'
python -m dsopz.dsopz 'gql' -d "$DS" -n "$NS" -q "select * from dsopz_test where c3 = 'a2'" | wc -l | grep '^1$'
python -m dsopz.dsopz 'gql' -d "$DS" -n "$NS" -q "select * from dsopz_test where c3 = 'a3'" | wc -l | grep '^1$'

cat "test/entities.json" | python -m dsopz.dsopz csv -c c1 __key__ c2 | diff - "test/entities.csv"

cat "test/entities.json" | python -m dsopz.dsopz map > "$EF/mapped.json" 3<<-EOF
ent['properties']['c2'] = {'excludeFromIndexes':True, 'stringValue':'changed'}
emit(ent)
EOF
cat "$EF/mapped.json" | python -m dsopz.dsopz csv -c c1 __key__ c2 | grep ';"changed"$' | wc -l | grep '^2$'

echo "SUCCESS"
