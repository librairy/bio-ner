echo "Initialazing Solr Indexing"

curl 'http://localhost:8983/solr/bioner-diseases/update/json?commit=true' --data-binary @data_processing/data/Disease/diseases.json -H 'Content-type:application/json'

echo "Disease Indexing finished!!"

curl 'http://localhost:8983/solr/bioner-drugs/update/json?commit=true' --data-binary @data_processing/data/Chemical/drugs.json -H 'Content-type:application/json'

echo "Chemical Indexing finished!!"

curl 'http://localhost:8983/solr/bioner-genetic/update/json?commit=true' --data-binary @data_processing/data/Genetic/genetic.json -H 'Content-type:application/json'

echo "Genetic Indexing finished!!"

curl 'http://localhost:8983/solr/bioner-covid/update/json?commit=true' --data-binary @data_processing/data/COVID/covid.json -H 'Content-type:application/json'

echo "COVID Indexing finished!!"
echo "Indexing Finished!!!"
