# Download and Backup

Here we show the ways DSOpz can download entities from [Google Cloud Datastore](https://cloud.google.com/datastore/)

Remeber, if you ***gzip*** the entity file you will save a lot of storage space

## Export

```shell
$ dsopz export --help
usage: dsopz export [-h] -d DATASET [-n NAMESPACE] [-k KINDS [KINDS ...]]
                       [-o KEYS_ONLY]

optional arguments:
  -h, --help            show this help message and exit
  -d DATASET, --dataset DATASET
                        dataset (pojectname)
  -n NAMESPACE, --namespace NAMESPACE
                        namespace (default: datastore default namespace)
  -k KINDS [KINDS ...], --kinds KINDS [KINDS ...]
                        kinds (default: all kinds)
  -o KEYS_ONLY, --keys-only KEYS_ONLY
                        keys only (default: false)
```

Samples:

```shell
$ # Export all entities of all kinds from default namespace
$ dsopz export -d myproject | gzip > entities.bak.gz 

$ # Export all entities of 'produt' and 'user' kinds from 'other' namespace
$ dsopz export -d myproject -k product user -n other | gzip > entities.bak.gz 
```

## Query

```shell
$ dsopz gql --help
usage: dsopz gql [-h] -d DATASET [-n NAMESPACE] -q GQL

optional arguments:
  -h, --help            show this help message and exit
  -d DATASET, --dataset DATASET
                        dataset (pojectname)
  -n NAMESPACE, --namespace NAMESPACE
                        namespace (default: datastore default namespace)
  -q GQL, --gql GQL     gql (sample: "select * from Product").
```

Samples:

```shell
$ # Query for android product
$ dsopz gql -d myproject -q "select * from Product where name = 'Android'" | gzip > entities.bak.gz

$ # You can create a keys-only file
$ dsopz gql -d myproject -q "select __key__ from Product where name = 'Android'" | gzip > entities.bak.gz
```

