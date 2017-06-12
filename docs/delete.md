# Delete

That is how DSOpz delete entities from [Google Cloud Datastore](https://cloud.google.com/datastore/)

If you gzip, remeber to gunzip

DSOpz is implemented to delete in parallel

## Delete

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
                        entities based on "key".
```

***Delete ignore properties from entities file.
So you can use both (keys-only and regular) files to delete enities***

Samples:

```shell
$ # Delete all entities from "entities.bak.gz" from
$ # default namespace of the "myproject" Datastore
$ cat entities.bak.gz | gunzip | dsopz import -d myproject -o delete

$ # Delete "product" and "user" entities from "entities.bak.gz"
$ # from "other" namespace of the "myproject" Datastore  
$ cat entities.bak.gz | gunzip | dsopz import -d myproject -o delete -k product user -n other
```
