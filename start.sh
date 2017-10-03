#!/bin/bash
# export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/models/research/slim
# export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/models/research


TENSORFLOW_OBJECT_DETECTION_DIR=models/research/object_detection
RESULTS_DIR=results/detection_1/

# From the tensorflow/models/research/ directory
PIPELINE_CONFIG_PATH=$RESULTS_DIR/model/ssd_inception_v2_coco_2018_01_28/pipeline.config
MODEL_DIR=$RESULTS_DIR/model/ssd_inception_v2_coco_2018_01_28/
NUM_TRAIN_STEPS=50000
SAMPLE_1_OF_N_EVAL_EXAMPLES=1

python $TENSORFLOW_OBJECT_DETECTION_DIR/model_main.py \
    --pipeline_config_path=${PIPELINE_CONFIG_PATH} \
    --model_dir=${MODEL_DIR} \
    --num_train_steps=${NUM_TRAIN_STEPS} \
    --sample_1_of_n_eval_examples=$SAMPLE_1_OF_N_EVAL_EXAMPLES \
    --alsologtostderr
#
# tensorboard --logdir=${MODEL_DIR}
