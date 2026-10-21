# SPDX-License-Identifier: Apache-2.0

from gr00t.data.embodiment_tags import EmbodimentTag
from gr00t.data.types import (
    ActionConfig,
    ActionFormat,
    ActionRepresentation,
    ActionType,
    ModalityConfig,
)


_ACTION_KEYS = ["left_arm", "right_arm", "left_hand", "right_hand"]

ffw_sh5_rev1_config = {
    "video": ModalityConfig(
        delta_indices=[0],
        modality_keys=["cam_left_head", "cam_left_wrist", "cam_right_wrist"],
    ),
    "state": ModalityConfig(delta_indices=[0], modality_keys=list(_ACTION_KEYS)),
    "action": ModalityConfig(
        delta_indices=list(range(40)),
        modality_keys=list(_ACTION_KEYS),
        action_configs=[
            ActionConfig(
                rep=ActionRepresentation.ABSOLUTE,
                type=ActionType.NON_EEF,
                format=ActionFormat.DEFAULT,
            )
            for _ in _ACTION_KEYS
        ],
    ),
    "language": ModalityConfig(
        delta_indices=[0],
        modality_keys=["annotation.human.task_description"],
    ),
}

# The launcher copies these exports into the selected run. Do not register SH5
# globally: SG2 also uses NEW_EMBODIMENT, with different joint/action layouts.
EMBODIMENT_TAG = EmbodimentTag.NEW_EMBODIMENT.value
MODALITY_CONFIG = ffw_sh5_rev1_config
TACTILE_CONFIG = {
    "state_keys": ["tactile_left", "tactile_right"],
    "input_shape": [2, 5, 9],
    "encoder": "finger_mlp",
    "embed_dim": 32,
}
