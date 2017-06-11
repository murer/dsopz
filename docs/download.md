# Download and Backup

Here we show the ways DSOpz can download entities from [Google Cloud Datastore](https://cloud.google.com/datastore/)

Remeber, if you ***gzip*** the entity file you will save a lot of storage space

## Export

```shell
$ dsopz export -d projectname | gzip > entities.bak.gz
```

## Query

