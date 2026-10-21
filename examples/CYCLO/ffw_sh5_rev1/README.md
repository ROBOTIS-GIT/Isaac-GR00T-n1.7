# Cyclo FFW SH5 Rev1 Modality

This example configures the existing GR00T N1.7 model for the SH5 arms and hands,
with optional tactile input. It contains the same three file types as the SG2
example: a Python training config, dataset `modality.json`, and this guide.

## Dataset requirements

Use a LeRobot v2.x dataset with the Task000650 SH5 recording layout. The supplied
`modality.json` maps the recorded arrays as follows (end indices are exclusive):

| Policy group | State slice in `observation.state` | Action slice in `action` | Width |
| --- | --- | --- | --- |
| `left_arm` | `[0, 7)` | `[0, 7)` | 7 |
| `right_arm` | `[27, 34)` | `[7, 14)` | 7 |
| `left_hand` | `[7, 27)` | `[14, 34)` | 20 |
| `right_hand` | `[34, 54)` | `[34, 54)` | 20 |

The policy consumes 54 joints in table order and predicts 40 steps of absolute
joint actions. Recorded head, lift, and base fields are excluded. State and action
arrays have different recorded ordering; do not apply the action slices to state.

The three image columns are:

- `observation.images.rgb.cam_left_head`
- `observation.images.rgb.cam_left_wrist`
- `observation.images.rgb.cam_right_wrist`

Language uses `annotation.human.task_description`, resolved from `task_index`.
For tactile training, `observation.tactile.left` and `observation.tactile.right`
must each contain 45 raw pressure values in the recorded sensor/taxel order.
Each observation contains two hands, five sensors per hand, nine taxels per sensor.
Baseline columns are not subtracted. The default `finger_mlp` encodes the 90
normalized values into 32 features inside the model.

## Prepare dataset

After confirming that the dataset matches the slices and names above, copy:

```bash
cp examples/CYCLO/ffw_sh5_rev1/modality.json <dataset_path>/meta/modality.json
```

This JSON describes dataset columns/slices. It is not the Python training config
and must not be passed to `--modality-config-path`.

## Fine-tune

```bash
CUDA_VISIBLE_DEVICES=0 python -m gr00t.experiment.launch_finetune \
  --base-model-path nvidia/GR00T-N1.7-3B \
  --dataset-path <dataset_path> \
  --embodiment-tag NEW_EMBODIMENT \
  --modality-config-path examples/CYCLO/ffw_sh5_rev1/ffw_sh5_rev1_config.py \
  --use-tactile \
  --letter-box-transform False \
  --num-gpus 1 \
  --output-dir <output_dir> \
  --max-steps 1 \
  --global-batch-size 1 \
  --dataloader-num-workers 0
```

This is a one-step startup check; select a suitable training duration and batch
size for an actual run. Omit `--use-tactile` for joint-only state input.
`--tactile-encoder` and `--tactile-embed-dim` can override the Python tactile
settings when tactile is enabled.

The Python file exports `MODALITY_CONFIG`, `EMBODIMENT_TAG`, and `TACTILE_CONFIG`.
The launcher copies these into the selected run, and appends tactile state keys
only when requested. It does not register SH5 globally because SG2 also uses
`NEW_EMBODIMENT`. The original SG2 import-time registration remains supported.
`--modality-config-path` accepts Python files only.

Camera definitions do not specify transforms. The training/processor config
controls resizing, cropping and letterboxing, and those settings are saved for
inference. Task000650 tactile training used 256x256 resizing, a 230x230 crop, and
no letterboxing. Preserve that recipe when using its checkpoint. For older
company checkpoints trained with letterboxing, correct the saved processor's
`letter_box_transform` to `true`; do not change Task000650's saved `false`.

## Inference

Load the complete checkpoint directory, including `processor_config.json`,
`statistics.json`, and `embodiment_id.json`. No example config path is needed:
the saved processor defines the modalities and image transforms.

```bash
python gr00t/eval/run_gr00t_server.py \
  --model-path <checkpoint_path> \
  --embodiment-tag NEW_EMBODIMENT \
  --use-tactile
```

Omit `--use-tactile` for a checkpoint trained without tactile. The encoder,
latent width, camera names, and joint/taxel order must match the saved checkpoint.
