#!/bin/bash

INPUT_TYPE=$1
CONFIG_NAME=$(echo $2 | cut -d "." -f1)
STEP=$(ls results/$INPUT_TYPE/$CONFIG_NAME/train | grep ckpt- | cut -d "-" -f2 | cut -d "." -f1 | sort -nr | head -1)
echo "Found step $STEP"

python3 export_inference_graph.py \
    --input_type image_tensor \
    --pipeline_config_path $CONFIG_NAME.config \
    --trained_checkpoint_prefix results/$INPUT_TYPE/$CONFIG_NAME/train/model.ckpt-$STEP \
    --output_directory results/$INPUT_TYPE/$CONFIG_NAME/inference_graph/
