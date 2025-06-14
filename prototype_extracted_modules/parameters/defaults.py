#!/usr/bin/env python3
"""
parameters/defaults.py
extracted from Working Prototype
"""

import numpy as np
import pandas as pd

# =============================================================================
# PARAMETERS MODULE (future: parameters/defaults.py)
# =============================================================================

# Define default parameters and distributions for each phase
PHASES = ['Phase I', 'Phase II', 'Phase III', 'Approval']

DEFAULT_PARAMS = {
    'Phase I': {
        'success_prob': 0.63,
        'cost_dist': ('triangular', 5, 10, 15),  # in $M
        'time_dist': ('normal', 1, 0.2),         # in years
    },
    'Phase II': {
        'success_prob': 0.31,
        'cost_dist': ('triangular', 15, 20, 30),
        'time_dist': ('normal', 2, 0.3),
    },
    'Phase III': {
        'success_prob': 0.58,
        'cost_dist': ('triangular', 50, 100, 150),
        'time_dist': ('normal', 3, 0.5),
    },
    'Approval': {
        'success_prob': 0.85,
        'cost_dist': ('triangular', 10, 20, 30),
        'time_dist': ('normal', 1, 0.2),
    },
    'Revenue': {
        'dist': ('triangular', 1000, 1500, 2500)  # in $M
    },
    'Discount Rate': 0.1
}