curl -X POST -H 'Content-type:application/json' --data-binary '{
  "add-field":{
     "name":"section_s",
     "type":"string" },
  "add-field":{
     "name":"text_t",
     "type":"text_general" },
  "add-field":{
     "name":"article_id_s",
     "type":"string" },
  "add-field":{
     "name":"size_i",
     "type":"pint" },
  "add-field":{
     "name":"name_s",
     "type":"string" }
}' http://localhost:8984/solr/covid_paragraphs/schema
