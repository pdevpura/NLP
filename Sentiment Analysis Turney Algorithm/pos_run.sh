#!/bin/bash
echo "starting the run"
while read data_file
do
echo "current run is $data_file"
./tagchunk.i686 -predict . w-5 ./data/imdb1/pos/"$data_file" resources > /home/richadeo/nlp_ass4/pos_files5/"$data_file".out

done < pos_dat.txt
