#!/usr/bin/env python3
"""
simulation/monte_carlo.py
extracted from Working Prototype
"""

import numpy as np
import pandas as pd
from ..parameters.defaults import DEFAULT_PARAMS
from .core import run_single_trial
from .financial import calculate_npv, calculate_roi

# =============================================================================
# MONTE CARLO MODULE (future: simulation/monte_carlo.py)
# =============================================================================

def run_simulations(n=1000, params=None, show_progress=False):
    """
    Runs Monte Carlo simulation of clinical trials.
    
    Args:
        n: Number of trial simulations to run
        params: Parameter dictionary (uses DEFAULT_PARAMS if None)
        show_progress: Whether to show progress updates
        
    Returns:
        DataFrame with simulation results
    """
    if params is None:
        params = DEFAULT_PARAMS
    
    if n <= 0:
        raise ValueError("You wanted to run... negative? simulations? I guess that has implications for answering 'What if we HADN'T done X'... But no.")
    
    results = []
    
    for i in range(n):
        if show_progress and (i + 1) % 1000 == 0:
            print(f"Completed {i + 1} / {n} simulations")
        
        trial = run_single_trial(params)
        
        # Calculate financial metrics
        npv = 0
        roi = 0
        if trial['success']:
            npv = calculate_npv(trial['revenue'], trial['time'], params['Discount Rate'])
            roi = calculate_roi(trial['revenue'], trial['cost'])
        
        results.append({
            'trial_id': i + 1,
            'success': trial['success'],
            'failed_phase': trial['failed_phase'],
            'cost': trial['cost'],
            'time': trial['time'],
            'revenue': trial['revenue'],
            'npv': npv,
            'roi': roi
        })
    
    return pd.DataFrame(results)

def analyze_results(results_df):
    """
    Generate summary statistics from simulation results.
    
    Args:
        results_df: DataFrame from run_simulations()
        
    Returns:
        Dictionary with analysis results
    """
    total_trials = len(results_df)
    successful_trials = results_df['success'].sum()
    success_rate = successful_trials / total_trials
    
    analysis = {
        'overall': {
            'total_simulations': total_trials,
            'successful_trials': int(successful_trials),
            'success_rate': success_rate,
            'failure_rate': 1 - success_rate
        },
        'costs': {
            'mean_cost': results_df['cost'].mean(),
            'median_cost': results_df['cost'].median(),
            'std_cost': results_df['cost'].std()
        },
        'financial': {
            'mean_npv': results_df['npv'].mean(),
            'median_npv': results_df['npv'].median(),
            'mean_roi': results_df['roi'].mean(),
            'positive_npv_rate': (results_df['npv'] > 0).mean()
        }
    }
    
    return analysis
