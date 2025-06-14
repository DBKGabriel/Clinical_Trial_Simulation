#!/usr/bin/env python3
"""
simulation/financial.py
extracted from Working Prototype
"""

import numpy as np
import pandas as pd

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
