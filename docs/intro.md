# Intro

DSOpz is a command line (and Python module) to manage entities into the 
[Google Cloud Datastore](https://cloud.google.com/datastore/) (from [Google Cloud Platform](https://cloud.google.com/)).

You can find Datastore docs [here](https://cloud.google.com/datastore/)

Basically speaking, DSOpz does two things on the datastore:

 1. Download entities and
 1. Upload entities
 
## Download Entities

The most basic way is exporting all entities from all kinds from default namespace:

```shell
$ dsopz export -d projectname > all_my_entities.bak
```

That is important (and simple) to understand how the data is stored into the ```all_my_entities.bak``` file.

Basically, we have a entity per line (```\n```). So, if you want to see the first entity retrieved you can:

```shell
$ head -n 1 all_my_entities.bak
```

***This entity is the exactly the same JSON we read from [Datastore API](https://cloud.google.com/datastore/docs/apis)***
(Without the ```namespace``` information)

```json
{
   "key" : { 
       "path" : [ { "kind" : "product",  "name" : "person"  } ] 
   },
   "properties" : {
      "name" : { "stringValue" : "Murer", "excludeFromIndexes" : false },
      "hasChildren" : { "booleanValue" : true, "excludeFromIndexes" : true },
   }
}
```

## Upload Entities

If you have that entity file, you can now save it back to datastore:

```shell
$ cat all_my_entities.bak | dsopz import -d projectname -o upsert
```

That `-o upsert` makes dsopz save all entities from the file into the datastore. 
Using each entity key, datastore will update existing entity and create the new ones.

That is the way you delete these entities:

```
$ cat all_my_entities.bak | dsopz import -d projectname -o remove
```








 
