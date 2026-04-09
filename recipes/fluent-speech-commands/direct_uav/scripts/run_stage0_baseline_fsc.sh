#!/usr/bin/env bash
set -e
cd recipes/fluent-speech-commands/direct
python train.py hparams/train.yaml
