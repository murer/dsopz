#!/bin/bash -xe

DS=${1:-cloudcontainerz}
NS=${2:-dsopz_test}

EF=target/dsopz_test

rm -rf "$EF" || true
mkdir -p "$EF"
python dsopz/dsopz.py 'export' -d "$DS" -n "$NS" -o true | python dsopz/dsopz.py 'import' -d "$DS" -n "$NS" -o remove

python dsopz/dsopz.py 'import' -d "$DS" -n "$NS" -o upsert < "test/entities.json"
python dsopz/dsopz.py 'export' -d "$DS" -n "$NS" > "$EF/bak.json"
diff test/entities.json "$EF/bak.json"

python dsopz/dsopz.py 'index' -k "dsopz_test" -c c2 -i true > "$EF/processed.json" < "$EF/bak.json"
python dsopz/dsopz.py 'import' -d "$DS" -n "$NS" -o upsert < "$EF/processed.json"
python dsopz/dsopz.py 'gql' -d "$DS" -n "$NS" -q "select * from dsopz_test order by c2" > "$EF/other.json"
if [ "x$(wc -l < $EF/other.json | tr -d ' ')" != "x2" ]; then
    echo "FAIL"
    exit 1
fi

echo "SUCCESS"

python dsopz/dsopz.py 'export' -d "$DS" -n "$NS" -o true | python dsopz/dsopz.py 'import' -d "$DS" -n "$NS" -o remove
