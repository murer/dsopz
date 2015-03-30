#!/bin/bash -e

DS=cloudcontainerz
NS=dsopz_test

EF=target/dsopz_test

rm -rf "$EF" || true
mkdir -p "$EF"    
python src/exporter.py -d "$DS" -n "$NS" -o true | python src/importer.py -d "$DS" -n "$NS" -o remove

python src/importer.py -d "$DS" -n "$NS" -o upsert < "test/entities.json"
python src/exporter.py -d "$DS" -n "$NS" > "$EF/bak.json"
diff test/entities.json "$EF/bak.json"

python src/processor_indexed.py -k "dsopz_test" -c c2 -i true > "$EF/processed.json" < "$EF/bak.json"
python src/importer.py -d "$DS" -n "$NS" -o upsert < "$EF/processed.json"
python src/reader.py -d "$DS" -n "$NS" -q "select * from dsopz_test order by c2" > "$EF/other.json"
diff test/entities.json "$EF/other.json"

echo "SUCCESS"

python src/exporter.py -d "$DS" -n "$NS" -o true | python src/importer.py -d "$DS" -n "$NS" -o remove