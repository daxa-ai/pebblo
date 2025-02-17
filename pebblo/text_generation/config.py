"""
Module to store Configuration parameters for the Pebblo topic classifier,
including model paths, confidence score, and minimum text length.
"""

import torch

# Minimum length of input text in characters
MAX_NEW_TOKENS = 3000

# Model paths
BASE_MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.3"
LOAD_IN_4BIT = True
BNB_4BIT_USE_DOUBLE_QUANT = True
BNB_4BIT_QUANT_TYPE = "nf4"
BNB_4BIT_COMPUTE_DTYPE = torch.bfloat16
