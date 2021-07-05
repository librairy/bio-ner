# bioNLP System for BioNER and BioNEN
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Website](https://img.shields.io/website?down_color=red&down_message=offline&up_color=green&up_message=online&url=https%3A%2F%2Falvaroalon2.github.io%2Fbio-nlp%2F)
![Docker](https://img.shields.io/badge/docker-v3+-blue.svg)
![Python](https://img.shields.io/badge/python-v3+-blue.svg)

## Basic Overview

Biomedical Named Entity Recognition and Normalization of Diseases, Chemicals and Genenetic entity classes through the use of state-of-the-art models.
The core piece in the modelling of the text entities recognition will be [BioBERT](https://github.com/dmis-lab/biobert-pytorch). Normalization step will be achived through inverse index search in a Solr database.

## System Set-up
Package bionlp is mainly proposed to be used as part of the webpage or the annotation of CORD-19. In its dockerized versions these requirements are already satisfied. If it was desired to use it separately, the following dependencies must be satisfied:
* transformers>=4.5.0
* spacy>=3
* pysolr~=3.9.0
* torch

bionlp package can be found on [bio-nlp/bionlp](https://github.com/alvaroalon2/bio-nlp/tree/master/bionlp)

## Solr Database for Normalization
Solr Database is available online at:
 * Diseases: http://librairy.linkeddata.es/solr/#/bioner-diseases/core-overview
 * Chemicals: http://librairy.linkeddata.es/solr/#/bioner-diseases/core-overview
 * Genetics: http://librairy.linkeddata.es/solr/#/bioner-diseases/core-overview
 * COVID: http://librairy.linkeddata.es/solr/#/bioner-diseases/core-overview

The endopoint for normalization 'http://librairy.linkeddata.es/solr/' will be later passed as environment variable if it is desired to leverage this database. If this endpoint is not passed, the system will looked for the database by default in localhost. Customize endopints could be passed as enviromental variables for a customize Solr Database but schemas must agree with the ones which were proposed.

If Solr database in localhost is desired to be used, this must be setup and populated in localhost before the following deployments since normalization step will need this database. Details about this configuration are found in [bio-nlp/Solr](https://github.com/alvaroalon2/bio-nlp/tree/master/Solr).

## Web Page
Available at: [https://alvaroalon2.github.io/bio-nlp/](https://alvaroalon2.github.io/bio-nlp/).

<p align="center">
<img src="https://user-images.githubusercontent.com/72864707/120455069-bab60800-c394-11eb-9c41-c2aeefc4f7cc.png" align="center" width="70%">
</p>

The webpage allows to easily use the system just pasting the text we want to process and clicking analyze button. This data will be sent through an AJAX call to the system which will return the data annotated and normalized in the following views:

### Results Annotation
Annotated results will be represented in coloured boxes where each box represents one entity class.

<p align="center">
<img src="https://user-images.githubusercontent.com/72864707/120455516-20a28f80-c395-11eb-97a8-fb54b017eaab.png" align="center" width="70%">
</p>

### Results Normalized
Normalized results will appear in a table for each of the entity classes. The found term will be retrieved along with the ids stored in a Solr Database. An extra Table will appear if COVID related terms appear in the processed text regarding to [drug target evidences](https://www.covid19dataportal.org/biochemistry?db=opentargets) or [related proteins.](https://proconsortium.org/cgi-bin/textsearch_pro?search=search&field0=ALLFLDS&query0=ncbitaxon%3A2697049)

<p align="center">
<img src="https://user-images.githubusercontent.com/72864707/120455588-3021d880-c395-11eb-965a-6c96bea89265.png" align="center">
</p>
	
### Results in JSON
In order to ease the later use of the retrieved information a Json text box is also established.

<p align="center">
<img src="https://user-images.githubusercontent.com/72864707/120455619-36b05000-c395-11eb-9522-14f3f4117017.png" align="center" width="70%">
</p>

### Web deployment
This web platform can be easily deployed thanks to its dockerization. Docker image can be found on Docker Hub: [https://hub.docker.com/r/alvaroalon2/webapp_bionlp](https://hub.docker.com/r/alvaroalon2/webapp_bionlp). Docker image includes the models within the image.
If it was not wanted to use the provided online Solr database endpoint 'http://librairy.linkeddata.es/solr/', then the environment variable should not be passed in docker run.

#### GPU Support
The [Docker Nvidia Toolkit](https://github.com/NVIDIA/nvidia-docker) is needed for GPU support inside Docker containers with NVIDIA GPUs. The deployment can be performed as follows:
1. `docker pull alvaroalon2/webapp_bionlp:gpu`
2. `docker run --name webapp -it --gpus all --network 'host' -e SOLR_URL="http://librairy.linkeddata.es/solr/" alvaroalon2/webapp_bionlp:gpu`

#### CPU Support
If a GPU is not available, deployment can be done also on CPU. If it is the case it is recommended to use the CPU dockerized version instead of GPU:
1. `docker pull alvaroalon2/webapp_bionlp:cpu`
2. `docker run --name webapp -it --network 'host' -e SOLR_URL="http://librairy.linkeddata.es/solr/" alvaroalon2/webapp_bionlp:cpu`

## CORD-19 Annotation
The proposed system will be used in a practical case: Annotation of CORD-19 corpus which contains thousands of COVID-19 related articles. For this purpose, the corpus will be previously pre-processed, to separate it on paragraphs, and loaded in a Solr database with the use of [https://github.com/librairy/cord-19](https://github.com/librairy/cord-19).
In order to ease the use of this annotation the use of the dockerized version is recommended. The repository on Docker Hub for this docker image can be found on:[https://hub.docker.com/r/alvaroalon2/bionlp_cord19_annotation](https://hub.docker.com/r/alvaroalon2/bionlp_cord19_annotation). Docker image includes the models within the image. If it was not wanted to use the provided online Solr database endpoint 'http://librairy.linkeddata.es/solr/', then the environment variable should not be passed in docker run.

### GPU Support
The [Docker Nvidia Toolkit](https://github.com/NVIDIA/nvidia-docker) is needed for GPU support inside Docker containers with NVIDIA GPUs. Steps for running the container and itialize its anotation and normalization are as follows:
1. `docker pull alvaroalon2/bionlp_cord19_annotation:gpu`
2. `docker run --name annotation -it --gpus all --network 'host' -e SOLR_URL="http://librairy.linkeddata.es/solr/" alvaroalon2/bionlp_cord19_annotation:gpu`

### CPU Support
If a GPU is not available, deployment can be done also on CPU. ANnotation will be substantially slower. If it is the case it is recommended to use the CPU dockerized version instead of GPU:
1. `docker pull alvaroalon2/bionlp_cord19_annotation:cpu`
2. `docker run --name annotation -it --network 'host' -e SOLR_URL="http://librairy.linkeddata.es/solr/" alvaroalon2/bionlp_cord19_annotation:cpu`

## Models 
One model was proposed for each of the entity classes: Diseases, Chemicals and Genenetic. Therefore, the final system is composed by three models in which each of them carries out the annnotation of its proper entity class. System will automatically check if models have been previously stored in its proper [folder](https://github.com/alvaroalon2/bio-nlp/tree/master/models). If the model is missing an automatical download of a cached version is download from its proper Huggingface repository where proposed models were uploaded. These are the repositories for the proposed models:
* Diseases: https://huggingface.co/alvaroalon2/biobert_diseases_ner
* Chemicals: https://huggingface.co/alvaroalon2/biobert_chemical_ner
* Genetic: https://huggingface.co/alvaroalon2/biobert_genetic_ner

Further details are described on: [bio-nlp/models](https://github.com/alvaroalon2/bio-nlp/tree/master/models). Models could be leveraged in other required systems if desired.

### Fine-tuning
Fine-tuning process was done in Google Collab using a TPU. For that purpose [Fine_tuning.ipynb](https://github.com/alvaroalon2/bio-nlp/blob/master/fine-tuning/NER4COVID.ipynb) Jupyter Notebook is proposed which make use of the scripts found on [bio-nlp/fine-tuning](https://github.com/alvaroalon2/bio-nlp/blob/master/fine-tuning/) which has been partially adapted from the originally proposed in [BioBERT repository](https://github.com/dmis-lab/biobert-pytorch) in order to allow TPU execution and the use of a newer version of huggingface-transformers.

## Embedding visualization
Details about visualization can be found on [bio-nlp/Embeddings](https://github.com/alvaroalon2/bio-nlp/tree/master/Embeddings) along with an example.

