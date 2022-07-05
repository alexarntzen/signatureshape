#!/bin/sh
remote_path="/work/paalel/master/code/animation/db"
local_path="/home/paalel/dev/master/code/so3/clustering/data/"
db_path="$remote_path/mocap.db"

sql_path="$remote_path/create_similarity_csv.sql"
csv_path="$remote_path/similarity.csv"
cmd="sqlite3 $db_path < $sql_path"
ssh markov $cmd 
rm $local_path"similarity.csv"
scp markov:$csv_path $local_path

sql_path="$remote_path/create_names_csv.sql"
csv_path="$remote_path/names.csv"
cmd="sqlite3 $db_path < $sql_path"
rm $local_path"names.csv"
ssh markov $cmd 
scp markov:$csv_path $local_path
