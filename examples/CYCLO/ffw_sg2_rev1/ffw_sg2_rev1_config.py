# SPDX-FileCopyrightText: Copyright (c) 2026 ROBOTIS CO., LTD.
# SPDX-License-Identifier: Apache-2.0

from gr00t.configs.data.embodiment_configs import register_modality_config
from gr00t.data.embodiment_tags import EmbodimentTag
from gr00t.data.types import (
    ActionConfig,
    ActionFormat,
    ActionRepresentation,
    ActionType,
    ModalityConfig,
)


_ACTION_KEYS = [
    "arm_left",
    "arm_right",
    "head",
    "lift",
    "odometry",
]


ffw_sg2_rev1_config = {
    "video": ModalityConfig(
        delta_indices=[0],
        modality_keys=[
            "cam_left_head",
            "cam_left_wrist",
            "cam_right_wrist",
        ],
    ),
    "state": ModalityConfig(
        delta_indices=[0],
        modality_keys=[
            "arm_left",
            "arm_right",
            "head",
            "lift",
            "odometry",
        ],
    ),
    "action": ModalityConfig(
        delta_indices=list(range(16)),
        modality_keys=_ACTION_KEYS,
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
        modality_keys=["annotation.human.primitive_instruction"],
    ),
}


register_modality_config(ffw_sg2_rev1_config, embodiment_tag=EmbodimentTag.NEW_EMBODIMENT)
