#!/bin/bash -xe

DS=cloudcontainerz
NS=dsopz_test

EF=target/dsopz_test

rm -rf "$EF" || true
mkdir -p "$EF"    
python src/dsopz.py 'export' -d "$DS" -n "$NS" -o true | python src/dsopz.py 'import' -d "$DS" -n "$NS" -o remove

python src/dsopz.py 'import' -d "$DS" -n "$NS" -o upsert < "test/entities.json"
python src/dsopz.py 'export' -d "$DS" -n "$NS" > "$EF/bak.json"
diff test/entities.json "$EF/bak.json"

python src/dsopz.py 'index' -k "dsopz_test" -c c2 -i true > "$EF/processed.json" < "$EF/bak.json"
python src/dsopz.py 'import' -d "$DS" -n "$NS" -o upsert < "$EF/processed.json"
python src/dsopz.py 'gql' -d "$DS" -n "$NS" -q "select * from dsopz_test order by c2" > "$EF/other.json"
if [ "x$(wc -l test/entities.json | cut -d" " -f1)" != "x2" ]; then
    echo "FAIL"
    exit 1
fi

echo "SUCCESS"

python src/dsopz.py 'export' -d "$DS" -n "$NS" -o true | python src/dsopz.py 'import' -d "$DS" -n "$NS" -o remove