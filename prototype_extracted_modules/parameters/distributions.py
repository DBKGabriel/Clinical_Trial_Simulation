#!/usr/bin/env python3
"""
parameters/distributions.py
extracted from Working Prototype
"""

import numpy as np
import pandas as pd

# =============================================================================
# DISTRIBUTIONS MODULE (future: parameters/distributions.py)
# =============================================================================

def sample_distribution(dist_tuple):
    """
    Samples a probability distribution based on the tuple arg.
    
    Args:
        dist_tuple: Tuple of (dist_type, *params)
        
    Returns:
        Random sample from the distribution
    """
    if len(dist_tuple) < 2:
        raise ValueError("Distribution tuple must have at least 2 elements")
    
    dist_type = dist_tuple[0]
    
    if dist_type == 'normal':
        if len(dist_tuple) != 3:
            raise ValueError("Normal distribution requires (type, mean, std)")
        _, mean, std = dist_tuple
        if std <= 0:
            raise ValueError("Standard deviation must be positive")
        return np.random.normal(mean, std)
        
    elif dist_type == 'triangular':
        if len(dist_tuple) != 4:
            raise ValueError("Triangular distribution requires (type, left, mode, right)")
        _, left, mode, right = dist_tuple
        if not (left <= mode <= right):
            raise ValueError(f"Triangular distribution requires left <= mode <= right, got {left}, {mode}, {right}")
        return np.random.triangular(left, mode, right)
        
    else:
        raise ValueError(f"Unsupported distribution type: {dist_type}")
