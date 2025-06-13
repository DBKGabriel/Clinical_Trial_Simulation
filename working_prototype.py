#!/usr/bin/env python3
"""
Clinical Trial Simulator - Working Prototype

Here I've validated some core concepts of the architecture outlined in my design sketch before modular extraction

I've combined my planned modules here with working imports for testing.
Next phase: Extract to planned modular structure.
"""

import numpy as np
import pandas as pd
import sys

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

# =============================================================================
# FINANCE MODULE (future: simulation/financial.py) 
# =============================================================================

def calculate_npv(cash_flow, time, discount_rate):
    """
    Calculate Net Present Value.
    
    Args:
        cash_flow: Future cash flow amount
        time: Delay to cash flow (years)
        discount_rate: Annual discount rate
        
    Returns:
        Present value of cash flow
    """
    if discount_rate < 0:
        raise ValueError("Discount rate can't be negative")
    if time < 0:
        raise ValueError("Time can't be negative")
        
    return cash_flow / ((1 + discount_rate) ** time)

def calculate_roi(revenue, cost):
    """
    Calculate Return on Investment.
    
    Args:
        revenue: Total revenue
        cost: Total cost
        
    Returns:
        ROI as decimal (e.g., 0.25 = 25% return)
    """
    if cost == 0:
        return 0 if revenue == 0 else float('inf')
    return (revenue - cost) / cost

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

# =============================================================================
# MAIN INTERFACE (future: main.py)
# =============================================================================

def main(n_simulations=None):
    """Main execution function for CLI usage."""
    
    # Get number of simulations from command line or default
    if n_simulations is None:
        if len(sys.argv) > 1:
            try:
                n_simulations = int(sys.argv[1])
            except ValueError:
                print("Error: Number of simulations must be an integer")
                print("Usage: python clinical_trial_simulator_prototype.py [n_simulations]")
                return
        else:
            n_simulations = 10000  # Default for main execution
    
    print("Clinical Trial Monte Carlo Simulator - Prototype")
    print("=" * 50)
    
    # Run simulation
    print(f"Running {n_simulations:,} trial simulation...")
    results = run_simulations(n_simulations, show_progress=True)
    
    # Analyze results
    analysis = analyze_results(results)
    
    # Display results
    print("\nSIMULATION RESULTS:")
    print("-" * 30)
    print(f"Total Simulations: {analysis['overall']['total_simulations']:,}")
    print(f"Success Rate: {analysis['overall']['success_rate']:.1%}")
    print(f"Mean Cost: ${analysis['costs']['mean_cost']:.1f}M")
    print(f"Mean NPV: ${analysis['financial']['mean_npv']:.1f}M")
    print(f"Mean ROI: {analysis['financial']['mean_roi']:.1%}")
    print(f"Positive NPV Rate: {analysis['financial']['positive_npv_rate']:.1%}")
    
    # Detailed statistics
    print(f"\nDETAILED STATISTICS:")
    print(results.describe())
    
    return results, analysis

if __name__ == '__main__':
    results, analysis = main()
    print(f"\nSimulation complete. To view results in more detail, rerun script with -i flag at CLI. Results will then be available in 'results' and 'analysis' variables.")
    print(f"To run with different parameters: python {sys.argv[0]} [number_of_simulations]")
