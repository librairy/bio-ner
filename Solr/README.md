# Solr Database Setup

## Solr database creation
In order to ease the creation of the proposed Solr along with its cores and configuration the following process is recommended to follow:
 1. `docker-compose up` on this folder for creating a Solr 8 instance along with the proposed cores.
 2. Execute the creation of schemas: `./create_schemas.sh`

This will create the proposed Solr system in *localhost*. For deploying it on a desired host some modifications will have to be done in these files for adapting the host.

## Retrieved terms - Download
The retrieved terms used for populating the Solr cores will be obtained through the execution of each of the *./data_processing/create_xxxx_database.ipynb* where xxxx is each of the entities which will be procesed.
Therefore, a processing of terms will be done for each of the entities the system will be focused on.
Results are directly offered for download through script [*download_data.sh*](https://github.com/alvaroalon2/bio-nlp/blob/master/Solr/download_data.sh)
Executin as follows will allow to obtain these results for further database population:
 * `./download_data.sh`

## Populate Solr Database
In order to populate the Solr database, the script [*index_docs.sh*](https://github.com/alvaroalon2/bio-nlp/blob/master/Solr/index_docs.sh) is proposed. Just the following command will be needed to populate the previously cretaed database with the former downloaded terms:
  * `./index_docs.sh`

Also the Notebook [*Solr_indexing*](https://github.com/alvaroalon2/bio-nlp/blob/master/Solr/data_processing/Solr_indexing.ipynb) is proposed.
Its complete execution will populate each of the cores for each of the entity classes.
pysolr library is required for the use of Solr through Python.


**Note**: if there were some execution permission problem: 
* Give execution permissions to *script.sh*: `sudo chmod +x ./script.sh`
