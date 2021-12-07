# dsopz

DSOpz (Datastore Operationz) lets you manage your Google Cloud Datastore from command line.

[![CircleCI](https://circleci.com/gh/murer/dsopz/tree/master.svg?style=svg)](https://circleci.com/gh/murer/dsopz/tree/master)

## Dsopz 2 Beta

This documentation is all about dsopz-1.x.x. I'm woking on dspoz2 :)

## Features

 * Python API and command line
 * No dependencies (see [below](#devel))
 * Uses [Google Cloud Datastore](https://cloud.google.com/datastore/docs) JSON API 
 * Export, import and delete data
 * GQL query
 * CSV exporter
 * Entity processors
   * You can update entities
   * Manage indexed properties
 * OAuth2 integrated
   * Installed apps
   * Service account

## Gettings Started

 * Every command has `--help`
 * If `namespace` was not given, we will access your default one.
 * If `kinds` was not given, we will use all of them.

### Install

```shell
    # download from https://github.com/murer/dsopz/releases
    easy_install dsopz.egg
    dsopz version
```

# module method

    cd dsopz
    python -m dsopz.dsopz version

### Login

    dsopz login

If you can't open a browser automatically to login you can use this command:

    dsopz login-text

You can use [GCE Service Account](https://cloud.google.com/compute/docs/authentication).

    dsopz login-gce

Or regular [Service Account](https://developers.google.com/identity/protocols/OAuth2ServiceAccount)

    dsopz login-serviceaccount -f <json-file>

Scopes Required:

    https://www.googleapis.com/auth/cloud-platform
    https://www.googleapis.com/auth/datastore
    https://www.googleapis.com/auth/userinfo.email

### Console

    dsopz console -d gae-projet -n namespace

Here you can type your `gql` like `select *`. Results are limited to 10, you can do `-l 0` to turn it unlimited.

### Export data

    dsopz export -d gae-project -n namespace -k kind1 kind2 > entities.bak

### GQL exporter

    dsopz gql -d gae-project -n namespace -q 'select * from kind1' > entities.bak

### Import data

    cat entities.bak | dsopz import -d gae-project -n namespace -o upsert

You can import entities to another project or namespace.

### Delete data

You need just a keys-only file to delete, and you can extract it using `-o true` while exporting

    cat entities.bak | dsopz import -d gae-project -n namespace -o remove

### Set indexed true or false

    cat entities.bak | dsopz index -c col1 col2 -k kind2 kind2 -i true > processed.bak
    cat processed.bak | dsopz import -d gae-project -n namespace -o upsert

This will generate `processe.bak` file with all entities from `entities.bak` which have changed `col1` or `col2` to indexed `true`. And upload it back to datastore

### Updating, delete or create

We can process a entity file into another, incluiding, updating or removing entities.

    cat entities.bak | dsopz map > procesed.bak 3<mapper.py

or

```python
cat entities.bak | dsopz map > processed.bak 3<<-EOF
ent['properties']['desc'] = {'excludeFromIndexes': True, 'stringValue': 'changed'}
emit(ent)
EOF
```

`dsopz/dsopz.py map` reads entities file from stdin, and python code from custom pipe input 3. This python code is called for every entity witch can be accessed via `ent` variable. This code can call `emit` function multiple times with one or more entities to be printed to `processed.bak`.


### Extract CSV from entities file

    cat entities.bak | dsopz csv -k kind1 kind2 -c col1 col2 > entities.csv

As you can see, all commands use stdin or stdout to read/write entities. The file has one entity json per line. You can use ` | gzip` and `| gunzip` to manage large amount of entities.

### Entity File

This entity file used to pipe in or out these python commands has one json per file. Each json is a datastore entity just like [Google Cloud Datastore](https://cloud.google.com/datastore/docs) returns. These entities does not have the partionId (namespace) information.

## Processors

Processors is what you can do to manage your entities file before import (or delete) it back to datastore. You can actually write a processor to do whatever you want with a entities file, for example: send entities to somewhere, parse them into a csv, etc.

To write a processor, you will `import processor` and extend `processor.Processor`. Override `resolve` method to process `self.block` array of entities. Sample: [processor_csv.py](./dsopz/processor_csv.py), [processor_indexed.py](./dsopz/processor_indexed.py)  

## Devel

 * It is pure python 2.7
 * It does not need any dependency
   * Except by ```login-serviceaccount``` which requires [pycryto](https://pypi.python.org/pypi/pycrypto) to sign [JWT](https://developers.google.com/identity/protocols/OAuth2ServiceAccount)
   
### Running tests

You need to login

```shell
python -m dsopz.dsopz login
```

Now, you can start the tests on your project (required) and namespace (optional).

```shell
./test/test.sh your-project your-namespace
```

This test tries to clean up in the end.
