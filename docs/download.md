# Download and Backup

Here we show the ways DSOpz can download entities from [Google Cloud Datastore](https://cloud.google.com/datastore/)

Remeber, if you ***gzip*** the entity file you will save a lot of storage space

## Export

```shell
$ python -m dsopz.dsopz export --help
usage: dsopz.py export [-h] -d DATASET [-n NAMESPACE] [-k KINDS [KINDS ...]]
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

## Query

```shell
$ python -m dsopz.dsopz gql --help
usage: dsopz.py gql [-h] -d DATASET [-n NAMESPACE] -q GQL

optional arguments:
  -h, --help            show this help message and exit
  -d DATASET, --dataset DATASET
                        dataset (pojectname)
  -n NAMESPACE, --namespace NAMESPACE
                        namespace (default: datastore default namespace)
  -q GQL, --gql GQL     gql (sample: "select * from Product").
```

