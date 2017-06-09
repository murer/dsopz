# Intro

DSOpz is a command line (and Python module) to manage entities into the 
[Google Cloud Datastore](https://cloud.google.com/datastore/) (from [Google Cloud Platform](https://cloud.google.com/)).

You can find Datastore docs [here](https://cloud.google.com/datastore/)

Basically speaking, DSOpz does two things on the datastore:

 1. Download entities and
 2. Upload entities
 
## Download Entities

The most basic way is exporting all entities from all kinds from default namespace:

```bash
dsopz export -d projectname
```

This command will export all the entities, 
one per line ```\n``` into the ```stdout```. 
So, usually, you want to gzip and write it into a file:

```bash
dsopz export -d projectname | gzip > all_my_entities.gz
```



 
