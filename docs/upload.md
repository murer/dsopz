# Upload and Restore

That is how DSOpz upload entities to [Google Cloud Datastore](https://cloud.google.com/datastore/)

If you gzip, remeber to gunzip

DSOpz is implemented to upload in parallel

## Export

```shell
$ dsopz import --help
usage: dsopz import [-h] -d DATASET [-n NAMESPACE] [-k KINDS [KINDS ...]]
                       [-b BLOCK] [-p PARALLEL] -o {upsert,remove}

optional arguments:
  -h, --help            show this help message and exit
  -d DATASET, --dataset DATASET
                        dataset
  -n NAMESPACE, --namespace NAMESPACE
                        namespace (default: default namespace)
  -k KINDS [KINDS ...], --kinds KINDS [KINDS ...]
                        kinds (default: all kinds)
  -b BLOCK, --block BLOCK
                        block size (default: 500)
  -p PARALLEL, --parallel PARALLEL
                        parallel (defaut: 10)
  -o {upsert,remove}, --operation {upsert,remove}
                        Use "upsert" to create entities and update entitiy
                        properties based on "key". Use "delete" to delete
                        entities based on "key". You can use "keys-only"
                        entity file to delete')

```

***If you upsert a keys-only file you will delete all properties from existing entities 
and create all new entities without properties***

Samples:

```shell
$ # Create and update (upsert) all entities from "entities.bak.gz" into the default namespace of the "myproject" Datastore
$ cat entities.bak.gz | gunzip | dsopz import -d myproject -o upsert

$ # "Upsert" "product" and "user" entities into the "other" namespace of the "myproject" Datastore  
$ cat entities.bak.gz | gunzip | dsopz import -d myproject -o upsert -k product user -n other
```
