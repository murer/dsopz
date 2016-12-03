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
python -m dsopz.dsopz 'export' -d "$DS" -n "$NS" > "$EF/bak.json"
diff test/entities.json "$EF/bak.json"
python -m dsopz.dsopz 'gql' -d "$DS" -n "$NS" -q "select * from dsopz_test order by c2" | wc -l | grep '^0$'

python -m dsopz.dsopz 'index' -k "dsopz_test" -c c2 -i true > "$EF/processed.json" < "$EF/bak.json"
python -m dsopz.dsopz 'import' -d "$DS" -n "$NS" -o upsert < "$EF/processed.json"
python -m dsopz.dsopz 'gql' -d "$DS" -n "$NS" -q "select * from dsopz_test order by c2" | wc -l | grep '^2$'
python -m dsopz.dsopz 'gql' -d "$DS" -n "$NS" -q "select * from dsopz_test order by c3" | wc -l | grep '^0$'

python -m dsopz.dsopz 'index' -k "dsopz_test" -c c3 -i true > "$EF/processed.json" < "$EF/bak.json"
python -m dsopz.dsopz 'import' -d "$DS" -n "$NS" -o upsert < "$EF/processed.json"
python -m dsopz.dsopz 'gql' -d "$DS" -n "$NS" -q "select * from dsopz_test where c3 = 'a1'" | wc -l | grep '^2$'
python -m dsopz.dsopz 'gql' -d "$DS" -n "$NS" -q "select * from dsopz_test where c3 = 'a2'" | wc -l | grep '^1$'
python -m dsopz.dsopz 'gql' -d "$DS" -n "$NS" -q "select * from dsopz_test where c3 = 'a3'" | wc -l | grep '^1$'

echo "SUCCESS"
