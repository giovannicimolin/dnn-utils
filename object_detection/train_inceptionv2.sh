#!/bin/bash

FOLDER=results/inceptionv2
mkdir $FOLDER

python3 train.py --logtostderr --train_dir=$FOLDER/train --pipeline_config_path=ssd_inception_v2_coco.config >  $FOLDER/train.txt &2>1
python3 eval.py --logtostderr --eval_dir=$FOLDER/eval --pipeline_config_path=ssd_inception_v2_coco.config --checkpoint_dir=$FOLDER/train > $FOLDER/eval.txt &2>1
tensorboard --logdir=$FOLDER --port=6006 $FOLDER/tensorboard.txt &2>1

tail -f $FOLDER/train.txt
