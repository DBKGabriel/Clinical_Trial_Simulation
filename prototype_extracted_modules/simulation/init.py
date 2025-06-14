"""
Clinical Trial Decision Simulator

A comprehensive Monte Carlo simulation framework for pharmaceutical
drug development decision support, financial modeling, and risk analysis.

This package provides tools for:
- Simulating clinical trial progression through all phases
- Modeling financial outcomes with uncertainty quantification
- Performing risk analysis and scenario planning
- Supporting go/no-go decision making with data-driven insights

Main Components:
    ClinicalTrialSimulator: Core simulation engine
    parameters: Parameter definition and management
    simulation: Monte Carlo simulation utilities  
    analysis: Statistical analysis and reporting
    utils: Helper functions and utilities

Quick Start Example:
    >>> from clinical_trial_simulator import ClinicalTrialSimulator
    >>> from clinical_trial_simulator.parameters import create_default_parameters
    >>> from clinical_trial_simulator.simulation import run_monte_carlo_simulation
    >>> from clinical_trial_simulator.analysis import analyze_simulation_results
    >>> 
    >>> # Create simulator with default industry parameters
    >>> params = create_default_parameters()
    >>> simulator = ClinicalTrialSimulator(params)
    >>> 
    >>> # Run Monte Carlo simulation
    >>> results = run_monte_carlo_simulation(simulator, n_simulations=10000)
    >>> 
    >>> # Analyze results
    >>> analysis = analyze_simulation_results(results)
    >>> print(f"Success rate: {analysis['overall']['overall_success_rate']:.1%}")
    >>> print(f"Expected NPV: ${analysis['expected_value']['expected_npv']:.1f}M")

Advanced Usage:
    >>> # Create custom parameters
    >>> from clinical_trial_simulator.parameters import (
    ...     DistributionParams, PhaseParams, MarketParams, SimulationParameters
    ... )
    >>> 
    >>> # Define custom Phase II parameters
    >>> phase_2 = PhaseParams(
    ...     name="Phase_2_Custom",
    ...     success_probability=0.45,
    ...     duration_months=DistributionParams('triangular', {'low': 15, 'mode': 20, 'high': 30}),
    ...     cost_millions=DistributionParams('triangular', {'low': 20, 'mode': 35, 'high': 70})
    ... )
"""

# Core imports for main API
from .simulation.core import ClinicalTrialSimulator

# Convenient imports for common workflows
from .parameters import (
    create_default_parameters,
    create_conservative_parameters,
    create_optimistic_parameters,
    DistributionParams,
    PhaseParams,
    MarketParams,
    SimulationParameters
)

from .simulation import (
    run_monte_carlo_simulation,
    calculate_npv,
    calculate_roi
)

from .analysis import (
    analyze_simulation_results,
    generate_summary_statistics
)

# Package metadata
__version__ = '1.0.0'
__title__ = 'Clinical Trial Decision Simulator'
__description__ = 'Monte Carlo simulation framework for pharmaceutical drug development decision support'
__author__ = 'Clinical Trial Simulator Team'
__email__ = 'contact@example.com'
__license__ = 'MIT'

# Define main public API - these are the most commonly used components
__all__ = [
    # Core simulator
    'ClinicalTrialSimulator',
    
    # Parameter creators
    'create_default_parameters',
    'create_conservative_parameters', 
    'create_optimistic_parameters',
    
    # Parameter classes
    'DistributionParams',
    'PhaseParams',
    'MarketParams', 
    'SimulationParameters',
    
    # Simulation functions
    'run_monte_carlo_simulation',
    'calculate_npv',
    'calculate_roi',
    
    # Analysis functions
    'analyze_simulation_results',
    'generate_summary_statistics'
]

# Package-level configuration
import warnings
import numpy as np

# Configure numpy to handle warnings appropriately
np.seterr(divide='ignore', invalid='ignore')

# Filter specific warnings that are common but not critical
warnings.filterwarnings('ignore', category=UserWarning, module='scipy')
warnings.filterwarnings('ignore', category=RuntimeWarning, message='invalid value encountered')

def get_package_info() -> dict:
    """
    Get comprehensive package information.
    
    Returns:
        Dictionary with package metadata and system information
    """
    import sys
    import platform
    
    return {
        'package': {
            'name': __title__,
            'version': __version__,
            'description': __description__,
            'author': __author__
        },
        'system': {
            'python_version': sys.version,
            'platform': platform.platform(),
            'numpy_version': np.__version__
        },
        'modules': {
            'parameters': 'Parameter definition and management',
            'simulation': 'Monte Carlo simulation engine',
            'analysis': 'Statistical analysis and reporting', 
            'utils': 'Helper functions and utilities'
        }
    }

def print_welcome_message():
    """Print package welcome message with basic usage information."""
    print("=" * 60)
    print(f"  {__title__} v{__version__}")
    print("=" * 60)
    print(__description__)
    print()
    print("Quick start:")
    print("  from clinical_trial_simulator import *")
    print("  params = create_default_parameters()")
    print("  simulator = ClinicalTrialSimulator(params)")
    print("  results = run_monte_carlo_simulation(simulator)")
    print("  analysis = analyze_simulation_results(results)")
    print()
    print("For documentation and examples, see:")
    print("  - README.md")
    print("  - examples/ directory") 
    print("  - help(clinical_trial_simulator)")
    print("=" * 60)

# Optional: Print welcome message on import (can be disabled)
_SHOW_WELCOME = False  # Set to True for development, False for production

if _SHOW_WELCOME:
    print_welcome_message()