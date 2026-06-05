# Cyclo FFW SG2 Rev1 Modality

This example provides the GR00T modality files for Cyclo Intelligence datasets
recorded with the FFW SG2 Rev1 robot.

## Dataset Requirement

Use a LeRobot v2.x dataset whose `observation.state` and `action` arrays are
both 22-dimensional and ordered as:

1. `arm_left`: indices `[0, 8)`
2. `arm_right`: indices `[8, 16)`
3. `head`: indices `[16, 18)`
4. `lift`: indices `[18, 19)`
5. `odometry`: indices `[19, 22)`

The included modality uses three camera streams:

- `observation.images.rgb.cam_left_head`
- `observation.images.rgb.cam_left_wrist`
- `observation.images.rgb.cam_right_wrist`

## Prepare Dataset

Copy the dataset modality file into the LeRobot dataset metadata directory:

```bash
cp examples/CYCLO/ffw_sg2_rev1/modality.json \
  <dataset_path>/meta/modality.json
```

## Fine-Tune

Run GR00T N1.7 fine-tuning with the Cyclo modality config:

```bash
CUDA_VISIBLE_DEVICES=0 python gr00t/experiment/launch_finetune.py \
  --base_model_path nvidia/GR00T-N1.7-3B \
  --dataset_path <dataset_path> \
  --embodiment_tag NEW_EMBODIMENT \
  --modality_config_path examples/CYCLO/ffw_sg2_rev1/ffw_sg2_rev1_config.py \
  --num_gpus 1 \
  --output_dir <output_dir> \
  --max_steps 1 \
  --global_batch_size 1 \
  --dataloader_num_workers 0
```

Use more steps and a larger batch size for real fine-tuning after the smoke test
passes.
