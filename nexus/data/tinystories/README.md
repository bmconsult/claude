# TinyStories Dataset

## Status: DOWNLOAD BLOCKED
HuggingFace API is blocked by proxy (403 Forbidden).

## Alternative Sources to Try:
1. Direct link: https://huggingface.co/datasets/roneneldan/TinyStories/tree/main
2. GitHub mirror (if exists)
3. Manual download from HuggingFace website

## Dataset Info
- Source: https://arxiv.org/abs/2305.07759
- Size: ~2GB train, ~28MB validation
- Format: Plain text, stories separated by blank lines
- Vocab: Words a 3-4 year old would understand
- Purpose: Training small (<10M param) coherent language models

## For Now
Using Shakespeare (data/shakespeare.txt) for training.
When TinyStories becomes available, retrain with:
  cargo run --release --example train_nexus_bpe -- --data data/tinystories/train.txt
