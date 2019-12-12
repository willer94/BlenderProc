#!/bin/bash

export WORKDIR=/media/willer/data/BlenderProc/experiments/ycb

# python run.py $WORKDIR/config.yaml \
#    $WORKDIR/camera_position \
#    /media/willer/software/dataset/YCB/models/$i/textured.obj \
#    $WORKDIR/output/$i/ #\
#    # && python show_h5py.py

MODEL_DIR=/media/willer/software/dataset/YCB/models_normalized
dir=$(ls -l $MODEL_DIR |awk '/^d/ {print $NF}')
for i in $dir
do
	echo $i
	sleep 2
    python run.py $WORKDIR/config.yaml \
       $WORKDIR/camera_position \
       /media/willer/software/dataset/YCB/models_normalized/$i/textured.obj \
       $WORKDIR/output/$i/ #\
       # && python show_h5py.py

done 