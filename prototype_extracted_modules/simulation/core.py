#!/usr/bin/env python3
"""
simulation/core.py
extracted from Working Prototype
"""

import numpy as np
import pandas as pd
from ..parameters.defaults import PHASES, DEFAULT_PARAMS
from ..parameters.distributions import sample_distribution
# =============================================================================
# SIMULATION MODULE (future: simulation/core.py)
# =============================================================================

def run_single_trial(params=None):
    """
    Simulates a single end-to-end lifecycle from Phase I clinical trials through approval.
    
    Args:
        params: Parameter dict (uses DEFAULT_PARAMS if None)
        
    Returns:
        Trial outcomes as dict
    """
    if params is None:
        params = DEFAULT_PARAMS
    
    success = True
    total_cost = 0
    total_time = 0
    failed_phase = None
    phase_results = {}
    
    for phase in PHASES:
        # Sample phase duration and cost
        phase_cost = sample_distribution(params[phase]['cost_dist'])
        phase_time = sample_distribution(params[phase]['time_dist'])
        
        # Update totals
        total_cost += phase_cost
        total_time += phase_time
        
        # Determine if phase succeeds
        phase_success = np.random.rand() < params[phase]['success_prob']
        
        # Store phase results
        phase_results[phase] = {
            'success': phase_success,
            'cost': phase_cost,
            'time': phase_time
        }
        
        if not phase_success:
            success = False
            failed_phase = phase
            break
    
    # Calculate revenue if successful
    revenue = 0
    if success:
        revenue = sample_distribution(params['Revenue']['dist'])
    
    return {
        'success': success,
        'failed_phase': failed_phase,
        'cost': total_cost,
        'time': total_time,
        'revenue': revenue,
        'phase_results': phase_results
    }
