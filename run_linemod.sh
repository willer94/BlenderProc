#!/bin/bash

export WORKDIR=experiments/linemod

# python run.py $WORKDIR/config.yaml \
#    $WORKDIR/camera_position \
#    /media/willer/software/dataset/YCB/models/$i/textured.obj \
#    $WORKDIR/output/$i/ #\
#    # && python show_h5py.py

MODEL_DIR=/media/willer/BackUp/datasets/LINEMOD
dir=$(ls -l $MODEL_DIR |awk '/^d/ {print $NF}')
for i in $dir
do
	echo $i
	sleep 2
    python run.py $WORKDIR/config.yaml \
       $WORKDIR/camera_position \
       $MODEL_DIR/$i/$i.ply \
       $WORKDIR/output/$i/ #\
       # && python show_h5py.py

done 