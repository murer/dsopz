# Download and Backup

Here we show the ways DSOpz can download entities from [Google Cloud Datastore](https://cloud.google.com/datastore/)

Remeber, if you ***gzip*** the entity file you will save a lot of storage space

## Export

Export all entities from all kinds from default namespace

```shell
$ dsopz export -d projectname | gzip > entities.bak.gz
```

Export all entities from all kinds from other namespace

```shell
$ dsopz export -d projectname -n other | gzip > entities.bak.gz
```

Export all entities from specific kinds from default namespace

```shell
$ dsopz export -d projectname -k product user | gzip > entities.bak.gz
```

## Query

