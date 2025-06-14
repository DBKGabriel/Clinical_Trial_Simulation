#!/usr/bin/env python3
"""
main.py
extracted from Working Prototype
"""

import numpy as np
import pandas as pd
import sys
from prototype_extracted_modules.simulation.monte_carlo import run_simulations, analyze_results


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
