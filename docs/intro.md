# Intro

DSOpz is a command line (and Python module) to manage entities into the 
[Google Cloud Datastore](https://cloud.google.com/datastore/) (from [Google Cloud Platform](https://cloud.google.com/)).

You can find Datastore docs [here](https://cloud.google.com/datastore/)

Basically speaking, DSOpz does two things on the datastore:

 1. Download entities and
 2. Upload entities
 
## Download Entities

The most basic way is exporting all entities from all kinds from default namespace:

```shell
dsopz export -d projectname > all_my_entities.bak
```

That is important (and simple) to understand how the data is stored into the ```all_my_entities.bak``` file.

Basically, we have entity per line (```\n```). So, if you want to see the first entity retrieved you can:

```shell
head -n 1 all_my_entities.bak
```

This entity is the exactly the same JSON we read from (Datastore API)[https://cloud.google.com/datastore/docs/apis]


 
