# This is a prototype script.
# It doesn't run and it's not supposed to
#  I'm planning to break it out into modular architecture in the next steps
# 

# **This will become the parameters module**

## defaults.py will hold default parameter sets that can be used

### Define default parameters and distributions for each phase
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

## distributions.py will hold various options for distributions to be used by the simulation

import numpy as np
def sample_distribution(dist_tuple):
    dist_type = dist_tuple[0]
    if dist_type == 'normal':
        _, mean, std = dist_tuple
        return np.random.normal(mean, std)
    elif dist_type == 'triangular':
        _, left, mode, right = dist_tuple
        return np.random.triangular(left, mode, right)
    else:
        raise ValueError(f"Unsupported distribution type: {dist_type}")

# This will become the simulation module

## simulation.py will run single-trial simulations

from .defaults import PHASES, DEFAULT_PARAMS
from .distributions import sample_distribution

def run_single_trial(params=DEFAULT_PARAMS):
    success = True
    total_cost = 0
    total_time = 0
    for phase in PHASES:
        if np.random.rand() > params[phase]['success_prob']:
            success = False
            break
        total_cost += sample_distribution(params[phase]['cost_dist'])
        total_time += sample_distribution(params[phase]['time_dist'])

    if success:
        revenue = sample_distribution(params['Revenue']['dist'])
        return {'success': True, 'cost': total_cost, 'time': total_time, 'revenue': revenue}
    else:
        return {'success': False, 'cost': total_cost, 'time': total_time, 'revenue': 0}

##  monte_carlo.py will run the advanced simulation
import pandas as pd
from .simulation import run_single_trial
from .finance import calculate_npv, calculate_roi
from .parameters import DEFAULT_PARAMS

def run_simulations(n=1000, params=DEFAULT_PARAMS):
    results = []
    for _ in range(n):
        trial = run_single_trial(params)
        npv = calculate_npv(trial['revenue'], trial['time'], params['Discount Rate']) if trial['success'] else 0
        roi = calculate_roi(trial['revenue'], trial['cost']) if trial['success'] else 0
        results.append({
            'success': trial['success'],
            'cost': trial['cost'],
            'time': trial['time'],
            'revenue': trial['revenue'],
            'NPV': npv,
            'ROI': roi
        })
    return pd.DataFrame(results)


##  finance.py will provide financial analyses
def calculate_npv(cash_flow, time, discount_rate):
    return cash_flow / ((1 + discount_rate) ** time)

def calculate_roi(revenue, cost):
    return (revenue - cost) / cost if cost else 0

# This will be the central controller
## main.py runs the full code
from clinical_trial_simulator.monte_carlo import run_simulations

if __name__ == '__main__':
    df = run_simulations(10000)
    print(df.describe())
    print("Success Rate:", df['success'].mean())
    print("Mean NPV:", df['NPV'].mean())
