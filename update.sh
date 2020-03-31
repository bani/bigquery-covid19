#!/bin/bash

export GOOGLE_APPLICATION_CREDENTIALS=/home/bani/code/bani-d3d2a5d2829e.json

git pull
python merge_files.py
#bq load --replace --source_format=CSV bani:covid19.daily_reports data.csv
python bq_load.py
#bq query --nouse_legacy_sql --flagfile=country.sql
python bq_country.py
