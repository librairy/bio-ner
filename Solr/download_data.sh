#!/bin/bash


wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1V4PUIW2LN6QjMOANEEt46LMuM7ktDZg6' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1V4PUIW2LN6QjMOANEEt46LMuM7ktDZg6" -O "solr_data.tar.gz" && rm -rf /tmp/cookies.txt
tar -xvzf solr_data.tar.gz -C ./data_processing/
rm "solr_data.tar.gz"

echo "Solr Data DOWNLOADED!!!"
