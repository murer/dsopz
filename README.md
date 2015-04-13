# dsopz

DSOpz (Datastore Operationz) is a project where you manage your datastore from command line.

## Features

 * Python API and command line
 * Uses [Google Cloud Datastore](https://cloud.google.com/datastore/docs) json API
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

### Login

    python dsopz.py login

If you can't open a browser automatically to login you can use this command:

    python dsopz.py login-text

You can use [GCE Service Account](https://cloud.google.com/compute/docs/authentication).

    python dsopz.py login-gce
    
Scopes Required:

    https://www.googleapis.com/auth/cloud-platform
    https://www.googleapis.com/auth/datastore
    https://www.googleapis.com/auth/userinfo.email

### Console

    python src/console.py -d gae-projet -n namespace

Here you can type your `gql` like `select *`. Results are limited to 10, you can do `-l 0` to turn it unlimited.

### Export data

    python src/exporter.py -d gae-project -n namespace -k kind1 kind2 > entities.bak

### GQL exporter

    python src/reader.py -d gae-project -n namespace -q 'select * from kind1' > entities.bak

### Import data

    cat entities.bak | pyhton src/importer.py -d gae-project -n namespace -o upsert

You can import entities to another project or namespace.

### Delete data

You need just a keys-only file to delete, and you can extract it using `-o true` while exporting

    cat entities.bak | pyhton src/importer.py -d gae-project -n namespace -o delete

### Set indexed true or false

    cat entities.bak | python src/processor_indexed.py -c col1 col2 -k kind2 kind2 -i true > processed.bak
    cat processed.bak | python src/importer.py -d gae-project -n namespace -o upsert

This will generate `processe.bak` file with all entities from `entities.bak` which have changed `col1` or `col2` to indexed `true`. And upload it back to datastore

### Updating, delete or create

We can process a entity file into another, incluiding, updating or removing entities.

    cat entities.bak | python src/processor_mapper.py > procesed.bak 3<mapper.py

or

    cat entities.bak | python src/processor_mapper.py > processed.bak 3<<-EOF
    ent['properties']['desc'] = {'indexed':False, 'stringValue': 'changed'}
    emit(ent)
    EOF

`processor_mapper.py` reads entities file from stdin, and python code from custom pipe input 3. This python code is called for every entity witch can be accessed via `ent` variable. This code can call `emit` function multiple times with one or more entities to be printed to `processed.bak`.


### Extract CSV from entities file

    cat entities.bak | python src/processor_csv.py -k kind1 kind2 -c col1 col2 > entities.csv

As you can see, all commands use stdin or stdout to read/write entities. The file has one entity json per line. You will want to use ` | gzip` and `| gunzip` to manage large amount of entities.

### Entity File

This entity file used to pipe in or out these python commands has one json per file. Each json is a datastore entity just like [Google Cloud Datastore](https://cloud.google.com/datastore/docs) returns. These entities does not have the partionId (namespace) information.

## Processors

Processors is what you can do to manage your entities file before import (or delete) it back do datastore. You can actually write a processor to do whatever you want with a entities file, for example: send entities to somewhere, parse them into a csv, etc.

To write a processor, you will `import processor` and extend `processor.Processor`. Override `resolve` method to process `self.block` array of entities. Sample: [processor_csv.py](./src/processor_csv.py), [processor_indexed.py](./src/processor_indexed.py)  



