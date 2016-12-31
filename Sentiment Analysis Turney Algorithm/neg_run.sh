#!/bin/bash
echo "starting the run"
while read data_file
do
echo "current run is $data_file"
./tagchunk.i686 -predict . w-5 ./data/imdb1/neg/"$data_file" resources > /home/richadeo/nlp_ass4/neg_files5/"$data_file".out

done < neg_dat.txt
