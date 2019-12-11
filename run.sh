#!/bin/bash

 python run.py examples/basic/rbot_config.yaml \
        examples/basic/rbot_camera_positions2 \
        /media/willer/BackUp/datasets/rbot_models/ape/ape.obj \
        examples/basic/output/  && python show_h5py.py
