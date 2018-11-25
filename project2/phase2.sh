#!/bin/sh

# remove old txt files if exists
rm -f ./outputs/*.txt
# parse
python3 phase1.py $1
# remove old index files if exists
rm -f ./outputs/*.idx
# sort the .txt files, break the input, use given script break.pl to build .idx
sort --unique ./outputs/ads.txt | perl break.pl | db_load -c duplicates=1 -T -t hash ./outputs/ad.idx
sort --unique ./outputs/pdates.txt | perl break.pl | db_load -c duplicates=1 -T -t btree ./outputs/da.idx
sort --unique ./outputs/terms.txt | perl break.pl | db_load -c duplicates=1 -T -t btree ./outputs/te.idx
sort --unique ./outputs/prices.txt | perl break.pl | db_load -c duplicates=1 -T -t btree ./outputs/pr.idx
# get query inputs
python3 getQueryInput.py
