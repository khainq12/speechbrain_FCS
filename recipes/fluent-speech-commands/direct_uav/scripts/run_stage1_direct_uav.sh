#!/usr/bin/env bash
set -e
cd recipes/fluent-speech-commands/direct_uav
python train_scpc.py hparams/train_scpc.yaml
